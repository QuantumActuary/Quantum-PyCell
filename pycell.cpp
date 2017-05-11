/*
 * PyCell.cpp
 * This registers the plugin with the runtime kernel.
 *
 *  Created on: Jan 3, 2016
 *      Author: tkchen
 */

#include <boost/python.hpp>
#include "pycell.h"
#include "PyCell/custom.h"

extern "C" PYCELL_API int getEngineVersion()
{
    return 2; //New API: Added metadata socket
              //         No more manual calls to declare_params, etc.
}

extern "C" PYCELL_API void registerPlugin(Quantum::Kernel &kernel)
{
    using namespace Quantum;
    namespace bp = boost::python;

    Cell_<PyCell::Custom>::SHORT_DOC = "PyCell is a plugin allowing you to create cells in Python.";
    Cell_<PyCell::Custom>::MODULE_NAME = "PyCellPlugin";
    Cell_<PyCell::Custom>::CELL_NAME = "Custom";

    try
    {
        PyRun_SimpleString("import sys, os");
        PyRun_SimpleString(std::string("ins_path = os.path.join('"
                + kernel.getRootDirectory() + "','mods','PyCell')").c_str());
        PyRun_SimpleString("sys.path.insert(1, ins_path)");
        PyRun_SimpleString(std::string("ins_path = os.path.join('"
                + kernel.getRootDirectory() + "','mods','PyCell','tests')").c_str());
        PyRun_SimpleString("sys.path.insert(1, ins_path)");
        bp::object py_registry = bp::import(bp::str("PyCell"));
        PyRun_SimpleString("from PyCell import *");
        PyRun_SimpleString("from UDPyCell import *");
        bp::list py_cells = bp::extract<bp::list>(py_registry.attr("registry"));

        bp::object main_module = bp::import("__main__");
        bp::object main_namespace = main_module.attr("__dict__");
        bp::object builtins = main_namespace["__builtins__"];
        bp::object help = builtins.attr("help");
        for(int i=0; i<len(py_cells); i++)
        {
            //get an instance of our custom cell
            cell_ptr add_this = std::shared_ptr<Cell>(new Cell_<PyCell::Custom>());

            //get our cell name from registry in python
            std::string name = std::string(bp::extract<const char*>(
                    (py_cells[i])["name"]));

            //set the user defined module in our cell parameter by getting from python
            std::string module = std::string(bp::extract<const char*>((py_cells[i])["module"]));
            add_this->parameters.get<std::string>("py_import") = module;
            //set it
            add_this->parameters["py_object"] << name;
            add_this->metadata["name"] << "Quantum::PyCell::" + name;
            add_this->declare_io_inst();

            std::string cell_doc = "";
            bp::object mod = bp::import(bp::str(module));
            bp::object obj = mod.attr(name.c_str());
            bp::object doc = obj.attr("__doc__");
            bool always_process;
            always_process = bp::extract<bool>(obj.attr("always_reprocess"));
            if(always_process)
            {
                add_this->acknowledge_process(!always_process);
            }

            //std::cout<<module<<"."<<name<<std::endl;
            if(doc.ptr() == bp::object().ptr())
            {
                //no doctext
                cell_doc = "";
            }
            else
            {
                cell_doc = bp::extract<std::string>(doc);
            }
            add_this->metadata["short_doc"] << cell_doc;
            bp::list categories = bp::extract<bp::list>((py_cells[i])["categories"]);
            for(int j=0; j < len(categories); j++)
            {
                add_this->categories.push_back(bp::extract<std::string>(categories[j]));
            }

            kernel.getCellRegistry().addCell(add_this, name);
        }
        PyRun_SimpleString("import test_pycell");
    }
    catch (bp::error_already_set)
    {
        PyErr_Print();
    }
}
