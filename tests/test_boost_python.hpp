/*
 * test_symcell_basic.hpp
 *
 * Copyright (c) Thomas - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Thomas <tkchen@gmail.com>, Oct 11, 2015
 */

#ifndef TESTS_TEST_BOOST_PYTHON_HPP_
#define TESTS_TEST_BOOST_PYTHON_HPP_

#include "boost/python.hpp"
#include "Engine/all.hpp"
#include "gtest/gtest.h"

namespace Quantum{
namespace bp = boost::python;

struct Boost
{
    static void declare_io(const CellSockets& p, CellSockets& in, CellSockets& out)
    {
        out.declare<std::string>("a", "Put string here.");
    }
    ReturnCode process(const CellSockets& i, const CellSockets& o)
    {
        bp::object module(bp::handle<>(bp::borrowed(PyImport_AddModule("__main__"))));
        PyRun_SimpleString("result = 'Hello'");
        bp::object dictionary = module.attr("__dict__");
        bp::object result = dictionary["result"];
        std::string result_value = std::string(bp::extract<const char*>(result));
        o["a"] << result_value;
        return OK;
    }
};

TEST(PyCell, Boost_Python)
{
    cell_ptr m1 = std::shared_ptr<Cell>(new Cell_<Boost>());
    m1->process();
    EXPECT_TRUE(m1->outputs["a"]->get<std::string>() == "Hello");
}
}//namespace Quantum
#endif /* TESTS_TEST_BOOST_PYTHON_HPP_ */
