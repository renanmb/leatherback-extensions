# https://forums.developer.nvidia.com/t/import-usd-assets-with-a-button-in-a-custom-extension/239739
# Import USD-Assets with a button in a custom extension
# just an example
def build_settings_ui(self, frame):
        with frame:
            with ui.VStack(spacing=5):
                # Update the Frame Title
                frame.title = "Settings"
                frame.visible = True
                dict = {
                    "label": "Filepath",
                    "type": "stringfield",
                    "default_val" : "/home/",
                    "tooltip": "Choose the box to let parts fall into",
                    "use_folder_picker" : True,
                }
                self.settings_elements["Filepath"] = str_builder(**dict)

                dict = {
                    "label" : "Load Box",
                    "type" : "button",
                    "text" : "Load Box Sample",
                    "tooltip" : "",
                    "on_clicked_fn" : self._on_load_box_event
                }
                self.settings_elements["Load Box"] = btn_builder(**dict)
                self.settings_elements["Load Box"] = True

    def _on_load_box_event(self):
        _filepath = self.settings_elements["Filepath"].get_value_as_string()
        self.sample._on_load_box_event(_filepath)