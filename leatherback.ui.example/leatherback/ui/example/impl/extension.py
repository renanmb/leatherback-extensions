import carb
import omni.ext
import omni.kit.app
import omni.ui as ui
from .ui_builder import UIBuilder

from omni.kit.viewport.utility import get_active_viewport_window, get_active_viewport


class Extension(omni.ext.IExt):
    """The Extension class"""

    def on_startup(self, ext_id):
        """Method called when the extension is loaded/enabled"""
        # UI handler
        # self.ui_builder = UIBuilder(window_title="Leatherback Ui Example", menu_path="Window/Leatherback Ui Example")
        
        self.input = carb.input.acquire_input_interface()
        self.mouse = omni.appwindow.get_default_app_window().get_mouse()
        val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MIDDLE_BUTTON)
        if val: print(f"MIDDLE_BUTTON : {val}")
        val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.COUNT)
        if val: print(f"COUNT : {val}")

        app = omni.kit.app.get_app()
        self.update_subscription = app.get_update_event_stream().create_subscription_to_add_remove_callbacks(
            self._on_update_event, None
        )

        viewport_window = get_active_viewport_window()
        
        
        self._window = ui.Window("My Window", width=300, height=300)
        with self._window.frame:
            with ui.VStack():
                ui.Label("Some Label")
                def on_click():
                    print(viewport_window)
                ui.Button("Click Me", clicked_fn=lambda: on_click())

    def on_shutdown(self):
        """Method called when the extension is disabled"""
        carb.log_info(f"on_shutdown")
        print("[RaycastExtension] Shutting down extension.")

        # clean up UI
        self.ui_builder.cleanup()
        
    def _on_update_event(self, arg):
        # Get pixel coordinates
        x_pixel, y_pixel = self.input_interface.get_mouse_coords_pixel(self.mouse)
        print(f"Pixel Coordinates: ({x_pixel}, {y_pixel})")

        # Get normalized coordinates (0 to 1)
        x_normalized, y_normalized = self.input_interface.get_mouse_coords_normalized(self.mouse)
        print(f"Normalized Coordinates: ({x_normalized}, {y_normalized})")

        return True
    # def get_mouse_position(self):
    #     # val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MIDDLE_BUTTON)
    #     if self.val: print(f"MIDDLE_BUTTON : {self.val}")

    #     # self.input = carb.input.acquire_input_interface()
    #     # self.mouse = omni.appwindow.get_default_app_window().get_mouse()

    #     (x,y) = self.input.get_mouse_coords_pixel(self.mouse)
    #     print(f"get_mouse_coords_pixel : {x,y}")

    #     (x, y) = self.input.get_mouse_coords_normalized(self.mouse)
    #     print(f"get_mouse_coords_normalized : {x, y}")




