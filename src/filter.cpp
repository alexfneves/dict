#include "filter.hpp"

std::pair<Component, Ref<Component>> filter(std::string &input_text) {
  auto input = Input(&input_text, "Enter text...");
  Ref<Component> input_ref = input; // Ref to keep focus control

  auto focused_input = Renderer(input, [&] { return input->Render(); });

  std::vector<std::pair<std::string, std::string>> languages = {
      {"en", "en"}, {"en", "pt_br"}, {"en", "dk"},    {"dk", "en"},
      {"dk", ""},   {"dk", "pt_br"}, {"pt_br", "en"}, {"pt_br", "pt_br"},
  };

  std::vector<Element> languages_elements;
  languages_elements.push_back(focused_input->Render());

  for (const auto &language : languages) {
    languages_elements.push_back(
        text(language.first + " -> " + language.second));
  }

  auto modal_component = Renderer([=] {
    return window(text("Languages"), vbox(languages_elements) | center);
  });

  return {modal_component, input_ref};
}
