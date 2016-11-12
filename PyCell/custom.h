/*
 * Copyright (c) Thomas Chen - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Thomas Chen <tkchen@gmail.com>, August 2015
 *
 * PyCellPlugin.hpp
 */

#ifndef CUSTOM_H_
#define CUSTOM_H_

#include <boost/python.hpp>
#include "Engine/kernel.h"
#include "pycell_config.h"
#include <atomic>

namespace Quantum {
namespace PyCell {
namespace bp = boost::python;
class PYCELL_API Custom
{
private:
    bp::object __name__;
    bp::object self;
    std::string return_msg_;
    bp::dict in;
    bp::dict out;
    bp::list required;
    bp::list inflow;
    bp::dict outflow;
    bp::list internal_use;
    bp::object py_id;
    static std::atomic<int> id_counter;
public:
    static void declare_params(CellSockets&);
    void declare_io_inst(const CellSockets&, CellSockets&, CellSockets&);
    void configure(const CellSockets&, const CellSockets&, const CellSockets&);
    //void reset(CellSockets&, CellSockets&, CellSockets&);
    void start();
    void stop();
    void activate();
    void deactivate();
    ReturnCode process(const CellSockets&, const CellSockets&);
    std::string return_msg() const;
};
} //namespace PyCell
} //namespace Quantum

#endif /* CUSTOM_H_ */
