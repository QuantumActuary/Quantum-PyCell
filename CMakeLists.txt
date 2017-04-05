cmake_minimum_required (VERSION 3.6)
project (PyCell)
set(CMAKE_INSTALL_PREFIX /Applications/Quantum.app/contents/resources/.kivy)
set(CMAKE_CXX_COMPILER /usr/local/llvm/bin/clang++)
set(CMAKE_CC_COMPILER /usr/local/llvm/bin/clang)
set(PYTHON_INCLUDE_DIRS /Applications/Quantum.app/Contents/Frameworks/python/3.6.1/include/python3.6m)
set(PYTHON_LIBRARIES /Applications/Quantum.app/Contents/Frameworks/python/3.6.1/lib)

add_definitions(-std=c++1y)

# Find Python and set PYTHON_INCLUDE_DIRS
# find_package( PythonLibs 3.6 REQUIRED )

include_directories(
    .
    ${CMAKE_INSTALL_PREFIX}/include
    ${PYTHON_INCLUDE_DIRS}
    /usr/local/gtest/include
    /usr/local/cellar/boost/1.63.0/include
)

LINK_DIRECTORIES(
    ${PYTHON_LIBRARIES}
    ${CMAKE_INSTALL_PREFIX}/lib
    /usr/local/gtest/lib
)

add_library(${PROJECT_NAME} SHARED
    pycell.cpp
    PyCell/custom.cpp
)

TARGET_LINK_LIBRARIES(${PROJECT_NAME}
    boost_python3-mt
    python3.6m
    QuantumCell
    gtest
)

install(FILES pycell.h DESTINATION ${CMAKE_INSTALL_PREFIX}/include/${PROJECT_NAME})
install(FILES pycell_config.h DESTINATION ${CMAKE_INSTALL_PREFIX}/include/${PROJECT_NAME})
install(FILES PyCell/custom.h DESTINATION ${CMAKE_INSTALL_PREFIX}/include/${PROJECT_NAME})
# The post-build.sh file will actually do the installation of build artifacts
add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD COMMAND ../post-build.sh . lib${PROJECT_NAME}.dylib)
