import carb
import numpy as np
import omni
import omni.appwindow  # Contains handle to keyboard

from .base_ui import BaseSample
from leatherback.example.ackermann.leatherback import LeatherbackPolicy

import os
from isaacsim.core.api.objects import VisualSphere
from isaacsim.sensors.camera import Camera

import omni.kit.viewport.utility as vp_utils
import omni.ui as ui
# import carb.input

class LeatherbackExample(BaseSample):
    def __init__(self) -> None:
        super().__init__()
        self._world_settings["stage_units_in_meters"] = 1.0
        self._world_settings["physics_dt"] = 1 / 60 # 1.0 / 500.0 # change
        self._world_settings["rendering_dt"] = 1 / 50 # 10.0 / 500.0 # change
        self._base_command = [0.0, 0.0, 0.0]
        self.base_command = [0.0, 0.0, 0.0]

        # bindings for keyboard to send a command
        self._input_keyboard_mapping = {
            # forward command
            "NUMPAD_8": [2.0, 0.0, 0.0],
            "UP": [2.0, 0.0, 0.0],
            # back command
            "NUMPAD_2": [-2.0, 0.0, 0.0],
            "DOWN": [-2.0, 0.0, 0.0],
            # left command
            "NUMPAD_6": [0.0, -2.0, 0.0],
            "RIGHT": [0.0, -2.0, 0.0],
            # right command
            "NUMPAD_4": [0.0, 2.0, 0.0],
            "LEFT": [0.0, 2.0, 0.0],
            # yaw command (positive)
            "NUMPAD_7": [0.0, 0.0, 2.0],
            "N": [0.0, 0.0, 2.0],
            # yaw command (negative)
            "NUMPAD_9": [0.0, 0.0, -2.0],
            "M": [0.0, 0.0, -2.0],
        }

    def setup_scene(self) -> None:
        self._world.scene.add_default_ground_plane(
            z_position=0,
            name="default_ground_plane",
            prim_path="/World/defaultGroundPlane",
            static_friction=0.2,
            dynamic_friction=0.2,
            restitution=0.01,
        )
        script_dir = os.path.dirname(__file__)
        # The ui-component-library has no function so it only gets the stringfield on change: so its set to "/home/"
        if self._relative_path == "/home/":
            relative_path = os.path.join("../../../../", "assets")
            full_path = os.path.abspath(os.path.join(script_dir, relative_path))
            usd_path = os.path.abspath(os.path.join(full_path, "leatherback_simple_better.usd"))
        else:
            relative_path = self._relative_path
            full_path = os.path.abspath(os.path.join(script_dir, relative_path))
            usd_path = os.path.abspath(os.path.join(full_path, "leatherback_simple_better.usd"))
        # setup the robot
        self.leatherback = LeatherbackPolicy(
            prim_path="/World/leatherback", 
            name="leatherback", 
            policy_path = full_path, 
            usd_path = usd_path, 
            position=np.array([-1, 0, 0.05]), 
            )
        camera_prim_path = "/OmniverseKit_Persp" # Default perspective camera prim path
        self.camera = Camera(
                prim_path = camera_prim_path,
                # name="camera",
                # position=np.array([0.0, 0.0, 25.0]),
                # frequency=20,
                # resolution=(256, 256),
                # orientation=rot_utils.euler_angles_to_quats(np.array([0, 90, 0]), degrees=True),
            )
        self.camera.initialize()
        self.camera.add_distance_to_image_plane_to_frame()
        self.camera.add_distance_to_camera_to_frame()
        self.camera.get_current_frame()["distance_to_camera"]

        timeline = omni.timeline.get_timeline_interface()
        self._event_timer_callback = timeline.get_timeline_event_stream().create_subscription_to_pop_by_type(
            int(omni.timeline.TimelineEventType.STOP), self._timeline_timer_callback_fn
        )
    # Example on how to subscribe to Mouse and Keyboard
    async def setup_post_load(self) -> None:
        self._appwindow = omni.appwindow.get_default_app_window()
        self._input = carb.input.acquire_input_interface() 
        self._keyboard = self._appwindow.get_keyboard()
        self.mouse = self._appwindow.get_mouse()

        self._sub_keyboard = self._input.subscribe_to_keyboard_events(self._keyboard, self._sub_keyboard_event)
        self._input_sub_id = self._input.subscribe_to_input_events(self._on_input_event, order=-10000)
        
        self._physics_ready = False
        self.get_world().add_physics_callback("physics_step", callback_fn=self.on_physics_step)
        await self.get_world().play_async()

    async def setup_post_reset(self) -> None:
        self._physics_ready = False
        await self._world.play_async()

    def on_physics_step(self, step_size) -> None:
        if self._physics_ready:
            self.leatherback.forward(step_size, self._base_command)
            # print(f"Base Command: {self._base_command}")
            VisualSphere(
                prim_path="/new_sphere",
                name="sphere_1",
                position=self._base_command,
                # scale=np.array([0.6, 0.5, 0.2]),
                # size=1.0,
                radius = 0.1,
                color=np.array([255, 0, 0]),
                )
        else:
            self._physics_ready = True
            self.leatherback.robot.initialize()
            self.leatherback.robot.post_reset()
    
    # Example on Subscribing to Keyboard Events
    def _sub_keyboard_event(self, event, *args, **kwargs) -> bool:
        """Subscriber callback to when kit is updated."""

        # when a key is pressed or released  the command is adjusted w.r.t the key-mapping
        if event.type == carb.input.KeyboardEventType.KEY_PRESS:
            # on pressing, the command is incremented
            if event.input.name in self._input_keyboard_mapping:
                self._base_command += np.array(self._input_keyboard_mapping[event.input.name])

        elif event.type == carb.input.KeyboardEventType.KEY_RELEASE:
            # on release, the command is decremented
            if event.input.name in self._input_keyboard_mapping:
                self._base_command -= np.array(self._input_keyboard_mapping[event.input.name])
        return True
        
    # Example on Subscribing to Mouse Events
    def _on_input_event(self, event, *_):
        if event.deviceType == carb.input.DeviceType.MOUSE:
            return self._on_global_mouse_event(event.event)
        else:
            return True

    def _on_global_mouse_event(self, event, *_):
        # Get Viewport dimensions
        viewport = ui.Workspace.get_window("Viewport")
        # Get the position (x, y) and size (width, height) of the viewport
        vp_x, vp_y, vp_width, vp_height = viewport.position_x, viewport.position_y, viewport.width, viewport.height
        # Get camera resolution
        width, height = self.camera.get_resolution()
        
        # We care only mouse down
        while True:
            if event.type == carb.input.MouseEventType.MIDDLE_BUTTON_DOWN:
                break
            return True
        # Get mouse coords 
        # (x, y) = self._input.get_mouse_coords_normalized(self.mouse) # None
        mx, my = self._input.get_mouse_coords_pixel(self.mouse)
        
        # 3. Get main window size - For later, check if inside viewport and which viewport
        win_w = ui.Workspace.get_main_window_width()
        win_h = ui.Workspace.get_main_window_height()

        # Map Viewport into camera pixel coords
        nw = width / vp_width
        nh = height / vp_height
        w = vp_x + vp_width
        h = vp_y + vp_height
        # Clamp coords into valid range
        vx = np.clip(mx, vp_x, w - 1)
        vy = np.clip(my, vp_y, h - 1)
        # Find mouse pixel coords in reference to camera pixel coords
        x = vx * nw
        y = vy * nh
        
        depth_img = self.camera.get_depth() # shape: (width, height, 1)
        depth_value = depth_img[int(y), int(x)]
        points_2d = np.array([[x, y]], dtype=np.float32)
        depths    = np.array([depth_value], dtype=np.float32)
        points_3d = self.camera.get_world_points_from_image_coords(points_2d, depths)
        # Generate base command
        flat_points_3d = points_3d.flatten().tolist()
        self._base_command = flat_points_3d
        # --------------------------------------------
        # For debugging - close but not accurate, work needed
        # --------------------------------------------
        # print(f"Viewport Location (x, y): ({vp_x}, {vp_y})")
        # print(f"Viewport Size (width, height): ({vp_width}, {vp_height})")
        # print(f"Camera Size (width, height): ({width}, {height})")
        # print(f"get_mouse_coords_normalized : {x,y}")
        # print(f"get_mouse_coords_pixel : {mx,my}")
        # print(f"Mapped coordinates: {x , y}")
        # print("3D:", self._base_command)
    # End of Example: Subscribing to Mouse Events

    def _timeline_timer_callback_fn(self, event) -> None:
        if self.leatherback:
            self._physics_ready = False

    def world_cleanup(self):
        self._event_timer_callback = None
        if self._world.physics_callback_exists("physics_step"):
            self._world.remove_physics_callback("physics_step")
