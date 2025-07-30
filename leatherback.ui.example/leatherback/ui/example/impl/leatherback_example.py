import carb
import numpy as np
import omni
import omni.appwindow  # Contains handle to keyboard
# from isaacsim.examples.interactive.base_sample import BaseSample # change
from .base_ui import BaseSample
# from isaacsim.robot.policy.examples.robots import SpotFlatTerrainPolicy # change
from leatherback.policy.example.leatherback import LeatherbackPolicy

import os
from isaacsim.core.api.objects import VisualSphere

class LeatherbackExample(BaseSample):
    def __init__(self) -> None:
        super().__init__()
        # my_world = World(stage_units_in_meters=1.0, physics_dt=1 / 60, rendering_dt=1 / 50)
        self._world_settings["stage_units_in_meters"] = 1.0
        self._world_settings["physics_dt"] = 1 / 60 # 1.0 / 500.0 # change
        self._world_settings["rendering_dt"] = 1 / 50 # 10.0 / 500.0 # change
        self._base_command = [0.0, 0.0, 0.0]
        self.base_command = [0.0, 0.0, 0.0]

        # Modify this to get commands as waypoints
        # bindings for keyboard to command
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
        # TODO: make a file importer
        script_dir = os.path.dirname(__file__)
        relative_path = os.path.join("../../../../../", "leatherback")
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
        # Change
        # self.spot = SpotFlatTerrainPolicy(
        #     prim_path="/World/Spot",
        #     name="Spot",
        #     position=np.array([0, 0, 0.8]),
        # )
        timeline = omni.timeline.get_timeline_interface()
        self._event_timer_callback = timeline.get_timeline_event_stream().create_subscription_to_pop_by_type(
            int(omni.timeline.TimelineEventType.STOP), self._timeline_timer_callback_fn
        )
    # region Command input
    # change this to take the mouse stuff
    async def setup_post_load(self) -> None:
        self._appwindow = omni.appwindow.get_default_app_window()
        self._input = carb.input.acquire_input_interface() 
        self._keyboard = self._appwindow.get_keyboard()
        self.mouse = self._appwindow.get_mouse()

        self._sub_keyboard = self._input.subscribe_to_keyboard_events(self._keyboard, self._sub_keyboard_event)
        self._sub_mouse = self._input.subscribe_to_mouse_events(self.mouse, self._sub_mouse_event)
        # there is no subscribe_to_mouse_events
        self.val = self._input.get_mouse_value(self.mouse, carb.input.MouseInput.MIDDLE_BUTTON)
        if self.val: print(f"MIDDLE_BUTTON : {self.val}")
        

        self._physics_ready = False
        self.get_world().add_physics_callback("physics_step", callback_fn=self.on_physics_step)
        await self.get_world().play_async()

    async def setup_post_reset(self) -> None:
        self._physics_ready = False
        await self._world.play_async()

    def on_physics_step(self, step_size) -> None:
        if self._physics_ready:
            self.leatherback.forward(step_size, self._base_command)
            # self.spot.forward(step_size, self._base_command) # change
            VisualSphere(
                prim_path="/new_cube_2",
                name="cube_1",
                position=self._base_command, #np.array([0, 0, 1.0]),
                # scale=np.array([0.6, 0.5, 0.2]),
                # size=1.0,
                radius = 0.1,
                color=np.array([255, 0, 0]),
                )
        else:
            self._physics_ready = True
            self.leatherback.robot.initialize()
            # Need to review the code and implement
            # self.spot.initialize() # change
            # self.spot.post_reset() # change
            # self.spot.robot.set_joints_default_state(self.spot.default_pos) # change
    
    # ---------------------------------------------------
    # From the leatherback_standalone.py
    # ---------------------------------------------------
    # initialize robot on first step, run robot advance
    # def on_physics_step(step_size) -> None:
    #     global first_step
    #     global reset_needed
    #     if first_step:
    #         # spot.initialize()
    #         spot.robot.initialize()
    #         first_step = False
    #     elif reset_needed:
    #         my_world.reset(True)
    #         reset_needed = False
    #         first_step = True
    #     else:
    #         print(f"Current base command:{base_command}")
    #         spot.forward(step_size, base_command)
    #         VisualSphere(
    #             prim_path="/new_cube_2",
    #             name="cube_1",
    #             position=base_command, #np.array([0, 0, 1.0]),
    #             # scale=np.array([0.6, 0.5, 0.2]),
    #             # size=1.0,
    #             radius = 0.1,
    #             color=np.array([255, 0, 0]),
    #             )
    # ---------------------------------------------------
    # ---------------------------------------------------
    # ---------------------------------------------------

    # region Command input
    # change this to mouse stuff
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
    
    # region _sub_mouse_event
    def _sub_mouse_event(self, event, *args, **kwargs) -> bool:
        """Subscriber callback to when kit is updated."""

        # when a key is pressed or released  the command is adjusted w.r.t the key-mapping
        if event.type == carb.input.MouseEventType.MIDDLE_BUTTON_DOWN:
            # self._base_command += np.array(self._input_keyboard_mapping[event.input.name])
            (x,y) = self._input.get_mouse_coords_pixel(self.mouse)
            print(f"get_mouse_coords_pixel : {x,y}")
        
        # The waypoint must be updated on release otherwise it gonna send a constant stream
        elif event.type == carb.input.MouseEventType.MIDDLE_BUTTON_UP:
            (x,y) = self._input.get_mouse_coords_pixel(self.mouse)
            print(f"get_mouse_coords_pixel : {x,y}")
        #     # on release, the command is decremented
        #     if event.input.name in self._input_keyboard_mapping:
        #         self._base_command -= np.array(self._input_keyboard_mapping[event.input.name])
        return True

    def _timeline_timer_callback_fn(self, event) -> None:
        if self.spot:
            self._physics_ready = False

    def world_cleanup(self):
        self._event_timer_callback = None
        if self._world.physics_callback_exists("physics_step"):
            self._world.remove_physics_callback("physics_step")
