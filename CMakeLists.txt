cmake_minimum_required(VERSION 3.10)
project(FTXUIProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Find FTXUI
find_package(ftxui REQUIRED)

# Add the main source file
add_executable(ftxui_app src/main.cpp)

# Link with FTXUI components
target_link_libraries(ftxui_app PRIVATE ftxui::screen ftxui::dom ftxui::component)
