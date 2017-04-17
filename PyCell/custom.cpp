/*
 * Copyright (c) Thomas Chen - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Thomas Chen <tkchen@gmail.com>, August 2015
 *
 * PyCellPlugin.hpp
 */

#include "PyCell/custom.h"
#include "Engine/gil_management.hpp"

#define DEBUG_MODE 0
namespace Quantum{
namespace PyCell{

std::atomic<int> Custom::id_counter{0};

void Custom::pass()
{
    //https://misspent.wordpress.com/2009/10/11/boost-python-and-handling-python-exceptions/
    PyObject *e, *v, *t;
    PyErr_Fetch(&e, &v, &t);
    PyErr_Restore(e, v, t);
    PyRun_SimpleString("raise");
}

void Custom::declare_params(CellSockets &p)
{
    p.declare<std::string>("py_import", "Module import name.", "PyCell");
    p["py_import"]->str = [&p](){return p.get<std::string>("py_import");};
    p.declare<std::string>("py_object", "Object import name.", "HelloPyCell");
    p["py_object"]->str = [&p](){return p.get<std::string>("py_object");};

    p.declare<std::string>("py_inflows",
            "Name of Python variable containing list of inflows", "inflows");

    p.declare<std::string>("py_outflows",
            "Name of Python variable containing list of outflows", "outflows");

    p.declare<std::string>("py_required",
            "Name of Python variable containing list of required inputs",
            "required");

    p.declare<std::string>("py_inputs",
            "Name of Python variable containing dict of inputs", "inputs");

    p.declare<std::string>("py_outputs",
            "Name of Python variable containing dict of outputs", "outputs");

    p.declare<std::string>("py_internal_use",
            "Name of Python variable containing list of internal use"
            " variables", "internal_use");

    p.declare<std::string>("py_threadsafe",
            "Name of Python boolean indicating if the cell is threadsafe",
            "threadsafe");
}

void Custom::declare_io_inst(const CellSockets& p, CellSockets& i, CellSockets& o)
{
    AcquireGIL lock = AcquireGIL();
    bp::object pymodule = bp::import(bp::str(p.get<std::string>("py_import")));
    __name__ = pymodule.attr(p.get<std::string>("py_object").c_str());
    self = __name__();

    in = bp::extract<bp::dict>(self.attr(
            p.get<std::string>("py_inputs").c_str()));

    out = bp::extract<bp::dict>(self.attr(
            p.get<std::string>("py_outputs").c_str()));

    required = bp::extract<bp::list>(self.attr(
            p.get<std::string>("py_required").c_str()));

    inflow = bp::extract<bp::list>(self.attr(
            p.get<std::string>("py_inflows").c_str()));

    outflow = bp::extract<bp::dict>(self.attr(
            p.get<std::string>("py_outflows").c_str()));

    internal_use = bp::extract<bp::list>(self.attr(
            p.get<std::string>("py_internal_use").c_str()));


    if(PyObject_HasAttrString(self.ptr(), "threadsafe"))
    {
        threadsafe_ = bp::extract<bool>(self.attr(
                p.get<std::string>("py_threadsafe").c_str()));
        (*metadata)["threadsafe"] << threadsafe_;
    }

    py_id = bp::object(++id_counter);
    self.attr("py_id") = py_id;
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" declare_io_inst"<<std::endl;
#endif

    //declare each input socket to mirror underlying python dict
    bp::list ik = in.keys();
    for(int j=0; j<len(ik); j++)
    {
        std::string key = std::string(bp::extract<const char*>(ik[j]));
        i.declare<bp::object>(key, "A python object.", in[ik[j]]);
        //setup the string printer for the input sockets
        i[key]->str = [=, &i](){
                bp::str pystr(i[key]->get<bp::object>());
                return std::string(bp::extract<const char*>(pystr));
        };
    }

    //declare the inflow triggers
    for(int j=0; j<len(inflow); j++)
    {
        const char* key = bp::extract<const char*>(inflow[j]);
        i.declare<ReturnCode>(key);
        i[key]->str = [=, &i](){return std::to_string(
                i.get<ReturnCode>(key));};
    }

    //setup the required inputs
    for(int n=0; n<len(required); n++)
    {
        const char* socket = bp::extract<const char*>(required[n]);
        i[socket]->required(true);
    }

    //set internal_use flags
    for(int m=0; m<len(internal_use); m++)
    {
        const char* socket = bp::extract<const char*>(internal_use[m]);
        i[socket]->internal_use(bp::extract<bool>(
                                internal_use.contains<std::string>(socket)));
    }

    //declare each output socket to mirror underlying python dict
    bp::list ok = out.keys();
    for(int k=0; k<len(ok); k++)
    {
        std::string key = std::string(bp::extract<const char*>(ok[k]));
        o.declare<bp::object>(std::string(bp::extract<const char*>(ok[k])),
                "A python object", out[ok[k]]);
        //setup the string printer for the output sockets
        o[key]->str = [=, &o](){
                bp::str pystr(o[key]->get<bp::object>());
                return std::string(bp::extract<const char*>(pystr));
        };
    }
    //declare the outflow triggers
    bp::list ofk = outflow.keys();
    for(int k=0; k<len(ofk); k++)
    {
        const char* key = bp::extract<const char*>(ofk[k]);
        o.declare<ReturnCode>(key, "Outgoing execution", UNKNOWN);
        o[key]->str = [=, &o](){return std::to_string(
                o.get<ReturnCode>(key));};
    }
}

void Custom::declare_metadata(CellSockets &m)
{
    metadata = &m;
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" declare_metadata"<<std::endl;
#endif
}

void Custom::configure(const CellSockets& p, const CellSockets& i, const CellSockets& o)
{
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" configure"<<std::endl;
#endif
    AcquireGIL lock = AcquireGIL();
    //set all inputs
    bp::list ik = in.keys();
    for(int j=0; j<len(ik); j++)
    {
        std::string key = std::string(bp::extract<const char*>(ik[j]));
        (self.attr("inputs"))[key] = i.get<bp::object>(key);
    }

    //run the underlying python configure function
    if(PyObject_HasAttrString(self.ptr(), "configure"))
    {
        self.attr("configure")();
    }

    //set the default metadata values
    if(PyObject_HasAttrString(self.ptr(), "return_msg_"))
    {
        return_msg_ = std::string(bp::extract<const char*>(
                      self.attr("return_msg_")));
        (*metadata)["return_msg"] << return_msg_;
    }
    if(PyObject_HasAttrString(self.ptr(), "return_code"))
    {
        int ret = bp::extract<int>(self.attr("return_code").attr("returncode"));
        (*metadata)["status"] << static_cast<ReturnCode>(ret);
    }
}

void Custom::start()
{
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" start"<<std::endl;
#endif
    AcquireGIL lock = AcquireGIL();
    //run the underlying python configure function
    if(PyObject_HasAttrString(self.ptr(), "start"))
    {
        self.attr("start")();
    }
}

void Custom::stop()
{
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" stop"<<std::endl;
#endif
    AcquireGIL lock = AcquireGIL();
    //run the underlying python configure function
    if(PyObject_HasAttrString(self.ptr(), "stop"))
    {
        self.attr("stop")();
    }
}

void Custom::activate()
{
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" activate"<<std::endl;
#endif
    AcquireGIL lock = AcquireGIL();
    //run the underlying python configure function
    if(PyObject_HasAttrString(self.ptr(), "activate"))
    {
        self.attr("activate")();
    }
}

void Custom::deactivate()
{
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" deactivate"<<std::endl;
#endif
    AcquireGIL lock = AcquireGIL();
    //run the underlying python configure function
    if(PyObject_HasAttrString(self.ptr(), "deactivate"))
    {
        self.attr("deactivate")();
    }
}

ReturnCode Custom::process(const CellSockets& i, const CellSockets& o)
{
    AcquireGIL lock = AcquireGIL();
    int result = static_cast<int>(UNKNOWN);
    //set all inputs
    bp::list ik = in.keys();
    for(int j=0; j<len(ik); j++)
    {
        std::string key = std::string(bp::extract<const char*>(ik[j]));
        (self.attr("inputs"))[key] = i.get<bp::object>(key);
    }
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" process"<<std::endl;
#endif
    //run the underlying python process function
    if(PyObject_HasAttrString(self.ptr(), "process"))
    {
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" found process()"<<std::endl;
#endif
        try
        {
            result = bp::extract<int>(self.attr("process")());
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" called process()"<<std::endl;
#endif
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" process success, result="<<result<<std::endl;
#endif
        }
        catch(const std::exception& e)
        {
#if DEBUG_MODE > 0
    std::cout<<metadata->get<std::string>("name")<<" process error="<<e.what()<<std::endl;
#endif
            //TODO: do not catch all.
            result = static_cast<int>(UNKNOWN);
        }
        catch(const bp::error_already_set&)
        {
            pass();
        }
        if(PyObject_HasAttrString(self.ptr(), "return_msg_"))
        {
            return_msg_ = std::string(bp::extract<const char*>(
                          self.attr("return_msg_")));
            (*metadata)["return_msg"] << return_msg_;
        }

        //save results to outputs
        if(result>=static_cast<int>(OK))
        {
            bp::list ok = out.keys();
            for(int k=0; k<len(ok); k++)
            {
                const char* key = bp::extract<const char*>(ok[k]);
                bp::object val = out[key];
                if(!val.is_none())
                {
                    //creates a new token on socket
                    ReleaseGIL unlock = ReleaseGIL();
                    o[key] << val;
                }
                else
                {
                    o[key]->get<bp::object>() = val;
                }
            }

            //set the outflows according to python process() results
            for(int k=0; k<len(outflow); k++)
            {
                const char* key = bp::extract<const char*>(outflow.keys()[k]);
                int val = bp::extract<int>(outflow[key]);
                if(val==static_cast<int>(OK))
                {
                    ReleaseGIL unlock = ReleaseGIL();
                    o[key] << static_cast<ReturnCode>(val);
                }
                else
                {
                    o[key]->get<ReturnCode>() = static_cast<ReturnCode>(val);
                }
            }
        }
    }
    else
    {
        return_msg_ = "This cell has no process() function!";
        result = static_cast<int>(UNKNOWN);
    }

    ReleaseGIL unlock = ReleaseGIL();
    return static_cast<ReturnCode>(result);
}

std::string Custom::return_msg() const
{
    return return_msg_;
}

} //namespace PyCell
} //namespace Quantum
#undef DEBUG_MODE
