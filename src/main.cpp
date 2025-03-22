#include "filter.hpp"
#include <ftxui/component/component.hpp>
#include <ftxui/component/component_base.hpp>
#include <ftxui/component/component_options.hpp>
#include <ftxui/component/screen_interactive.hpp>
#include <ftxui/dom/elements.hpp>

using namespace ftxui;

int main() {
  auto screen = ScreenInteractive::Fullscreen();

  int selected_window = 0; // To track which window to display
  bool show_modal = false;
  bool show_shortcuts = false;
  bool show_languages = false;

  // Content for each window
  auto home_content = text("Welcome to the Home tab") | center;
  auto settings_content = text("Settings Page") | center;
  auto about_content = text("About this Application") | center;
  auto footer = hbox({
      text("asdf") | flex,
      text(" | "),
      text("source -> translated"),
      text(" | "),
      text("locale"),
      text(" | ? "),
  });

  std::string asdf;
  auto input_component = Input(&asdf, "gggg");

  // Renderer to ensure focus on the input field
  auto focused_input = Renderer(input_component, [&] {
    input_component->TakeFocus(); // Ensure input gets focus
    return input_component->Render();
  });

  // Layout with a vbox for windows
  auto main_renderer = Renderer([&] {
    return vbox({
               selected_window == 0
                   ? window(text("Meaning"), Input(&asdf, "gggg")->Render()) |
                         flex
                   : window(text("Meaning"), vbox({})) | xflex_grow,
               selected_window == 1
                   ? window(text("Translate"), settings_content) | flex
                   : window(text("Translate"), vbox({})) | xflex,
               selected_window == 2
                   ? window(text("Settings"), about_content) | flex
                   : window(text("Settings"), vbox({})) | xflex_grow,
               footer | xflex_grow,
           }) |
           xflex_grow;
  });

  auto modal_shortcuts = Renderer([&] {
    return window(text(" Shortcuts "), vbox({
                                           text("[1] - Meaning"),
                                           text("[2] - Translate"),
                                           text("[3] - Settings"),
                                           text("[?] - Show this help"),
                                           text("[Esc] - Close modal"),
                                           text("[Q] - Quit"),
                                       }) | center);
  });

  std::string filter_text;
  auto [modal_languages, filter_input] =
      filter(filter_text); // Get both modal and input reference

  auto modal_renderer = Modal(
      main_renderer, Renderer([&] {
        if (show_shortcuts)
          return modal_shortcuts->Render();
        if (show_languages)
          return modal_languages->Render();
        return vbox({}); // Empty content if no modal is active
      }),
      &show_modal // This will handle both modals based on their own states
  );

  // Event handler for switching windows using 1, 2, 3 and modal controls
  auto event_handler = CatchEvent(modal_renderer, [&](Event event) {
    if (event == Event::Character('?')) {
      show_modal = true;
      show_shortcuts = true;
      show_languages = false;
      return true;
    }
    if (event == Event::Character('l')) {
      show_modal = true;
      show_shortcuts = false;
      show_languages = true;

      // Ensure focus is applied to the input component
      (*filter_input)->TakeFocus(); // Now call TakeFocus on the Component
                                    // itself, not the shared_ptr

      return true;
    }
    if (event == Event::Escape && show_modal) {
      show_modal = false;
      show_shortcuts = false;
      show_languages = false;
      return true;
    }
    if (event == Event::Character('q')) {
      screen.Exit();
      return true;
    }
    if (event == Event::Character('1')) {
      selected_window = 0; // Show Home window
      show_modal = false;
      show_shortcuts = false;
      show_languages = false;
      return true;
    }
    if (event == Event::Character('2')) {
      selected_window = 1; // Show Settings window
      show_modal = false;
      show_shortcuts = false;
      show_languages = false;
      return true;
    }
    if (event == Event::Character('3')) {
      selected_window = 2; // Show About window
      show_modal = false;
      show_shortcuts = false;
      show_languages = false;
      return true;
    }
    return false;
  });

  screen.Loop(event_handler);
  return 0;
}
