#pragma once
#include <ftxui/component/component.hpp>
#include <ftxui/dom/elements.hpp>

using namespace ftxui;

std::pair<Component, Ref<Component>> filter(std::string &input_text);
