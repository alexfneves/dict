#include <ftxui/component/component.hpp>
#include <ftxui/component/screen_interactive.hpp>
#include <ftxui/dom/elements.hpp>
#include <iostream>

int main() {
  std::cout << "ggg" << std::endl;
  using namespace ftxui;
  auto screen = ScreenInteractive::FitComponent();
  auto button = Button("Press Me", [] { std::cout << "Button Pressed!\n"; });

  auto layout = Renderer(
      button, [&] { return vbox({text("Hello, FTXUI!"), button->Render()}); });

  screen.Loop(layout);
  return 0;
}
