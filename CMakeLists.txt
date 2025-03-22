cmake_minimum_required(VERSION 3.10)
project(dict)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Find FTXUI
find_package(ftxui REQUIRED)

# Add the main source file
add_executable(dict include/filter.hpp src/main.cpp src/filter.cpp)
target_include_directories(dict PRIVATE include)

# Link with FTXUI components
target_link_libraries(dict PRIVATE ftxui::screen ftxui::dom ftxui::component)
