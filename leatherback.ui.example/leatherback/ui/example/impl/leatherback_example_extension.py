import os

import omni.ext
from isaacsim.examples.browser import get_instance as get_browser_instance
# from isaacsim.examples.interactive.base_sample import BaseSampleUITemplate # change
from .base_ui_extension import BaseSampleUITemplate
# from isaacsim.examples.interactive.quadruped import QuadrupedExample # change
from .leatherback_example import LeatherbackExample

'''
This code is basically adding the extension as an example the 
isaacsim.examples.browser 

Just like the other robots
'''
class LeatherbackExampleExtension(omni.ext.IExt):
    def on_startup(self, ext_id: str):
        self.example_name = "Leatherback"
        self.category = "Policy"

        overview = "This Example shows a F1Tenth car based on the project Leatherback"
        # overview += "\n\tKeybord Input:"
        # overview += "\n\t\tup arrow / numpad 8: Move Forward"
        # overview += "\n\t\tdown arrow/ numpad 2: Move Reverse"
        # overview += "\n\t\tleft arrow/ numpad 4: Move Left"
        # overview += "\n\t\tright arrow / numpad 6: Move Right"
        # overview += "\n\t\tN / numpad 7: Spin Counterclockwise"
        # overview += "\n\t\tM / numpad 9: Spin Clockwise"

        overview += "\n\nPress the 'Open in IDE' button to view the source code."

        ui_kwargs = {
            "ext_id": ext_id,
            "file_path": os.path.abspath(__file__),
            "title": "Leatherback",
            "doc_link": "https://github.com/renanmb", # change
            "overview": overview,
            "sample": LeatherbackExample(), # change
        }

        ui_handle = BaseSampleUITemplate(**ui_kwargs)

        # register the example with examples browser
        get_browser_instance().register_example(
            name=self.example_name,
            execute_entrypoint=ui_handle.build_window,
            ui_hook=ui_handle.build_ui,
            category=self.category,
        )

        return

    def on_shutdown(self):
        get_browser_instance().deregister_example(name=self.example_name, category=self.category)

        return
