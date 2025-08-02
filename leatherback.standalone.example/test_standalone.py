from isaacsim import SimulationApp

# Start the application
simulation_app = SimulationApp({"headless": False})

from isaacsim.core.utils.extensions import enable_extension
enable_extension("leatherback.policy.example")
# simulation_app.update()

import carb
import numpy as np
import omni.appwindow  # Contains handle to keyboard
from isaacsim.core.api import World
from isaacsim.core.utils.prims import define_prim, get_prim_at_path

from leatherback.policy.example.leatherback import LeatherbackPolicy

from isaacsim.storage.native import get_assets_root_path

import os
from isaacsim.core.api.objects import VisualSphere

import omni.usd
from pxr import Usd, UsdGeom, UsdLux, Sdf, Gf

from isaacsim.core.prims import XFormPrim # XFormPrimView

script_dir = os.path.dirname(__file__)
relative_path = os.path.join("..", "leatherback")
full_path = os.path.abspath(os.path.join(script_dir, relative_path))
usd_path = os.path.abspath(os.path.join(full_path, "leatherback_simple_better.usd"))
butter_path = os.path.abspath(os.path.join(full_path, "butterbot_v01.usd"))

first_step = True
reset_needed = False

def is_goal_reached(current_position, command, tolerance=0.15):
    """
    Checks if a current XYZ position is within a specified tolerance of a target XYZ position.

    Args:
        current_position (np.ndarray): A 1D NumPy array representing the current XYZ coordinates (e.g., [x, y, z]).
        command (np.ndarray): A 1D NumPy array representing the target XYZ coordinates.
        tolerance (float, optional): The maximum allowed difference between the current and target coordinates
                                    for them to be considered "reached". Defaults to 0.01.

    Returns:
        bool: True if the current_position is within the tolerance of the command position, False otherwise.
    """
    return np.all(np.isclose(current_position, command, atol=tolerance))

# initialize robot on first step, run robot advance
def on_physics_step(step_size) -> None:
    global first_step
    global reset_needed
    if first_step:
        # spot.initialize()
        leatherback.robot.initialize()
        first_step = False
    elif reset_needed:
        my_world.reset(True)
        reset_needed = False
        first_step = True
    else:
        # print(f"Current base command:{base_command}")
        leatherback.forward(step_size, base_command)
        VisualSphere(
            prim_path="/new_cube_2",
            name="cube_1",
            position=base_command, #np.array([0, 0, 1.0]),
            # scale=np.array([0.6, 0.5, 0.2]),
            # size=1.0,
            radius = 0.1,
            color=np.array([255, 0, 0]),
            )


# spawn world
# leatherback is configure for physics_dt = 1/60 the spot seems to be physics_dt=1 / 500,
my_world = World(stage_units_in_meters=1.0, physics_dt=1 / 60, rendering_dt=1 / 50)
assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets folder")

# spawn warehouse scene
prim = define_prim("/World/Ground", "Xform")
asset_path = assets_root_path + "/Isaac/Environments/Grid/default_environment.usd"
prim.GetReferences().AddReference(asset_path)

# Add Lights
stage = omni.usd.get_context().get_stage()
light_prim_path="/World/DomeLight"
intensity=1000
exposure=0.0
dome_light = UsdLux.DomeLight.Define(stage, light_prim_path)
dome_light.GetIntensityAttr().Set(intensity)
dome_light.GetExposureAttr().Set(exposure)

leatherback = LeatherbackPolicy(
    prim_path="/World/leatherback",
    name="leatherback",
    policy_path = full_path,
    usd_path = usd_path,
    position=np.array([-1, 0, 0.05]),
)

my_world.reset()
my_world.add_physics_callback("physics_step", callback_fn=on_physics_step)

# robot command
# The position of the waypoint in X , Y , Z
base_command = np.zeros(3)

# Testing visibility
'''
This will turn the prim invisible and add the butterbot.
'''
prim_path = "/World/leatherback" 
prim_path02 = "/World/butterbot"

prim = stage.GetPrimAtPath(prim_path)
prim02 = define_prim(prim_path02, "Xform")

# Check if the prim is valid
if prim.IsValid():
    # Get the UsdGeom.Imageable schema for the prim
    imageable = UsdGeom.Imageable(prim)
    # Set the visibility attribute to "invisible"
    imageable.GetVisibilityAttr().Set(UsdGeom.Tokens.invisible)
    prim02.GetReferences().AddReference(butter_path) 
else:
    print(f"Error: Prim at path '{prim_path}' not found.")



i = 0
idx = 0
while simulation_app.is_running():
    my_world.step(render=True)
    if my_world.is_stopped():
        reset_needed = True
    if my_world.is_playing():
        position, orientation = leatherback.robot.get_world_pose() 
        # print(f"Get the current position: {position}")
        goal_reached = is_goal_reached(position, base_command)
        # print(f"Is the goal reached: {goal_reached}")
        # base_command = np.array([6, 0, 0])
        commands = np.array([[1, 0, 0],[3, 2, 0],[2, 4, 0],[0, 4, 0],[-1, 2, 0]])
        # commands = np.array([[1, 0, 0],[10, 2, 0],[3, 6, 0],[0, 4, 0],[-1, 2, 0]])
        robot1 = XFormPrim(prim_path)
        positions = np.zeros((1, 3))
        positions[0] = position
        orientations = np.zeros((1, 4))
        orientations[0] = orientation
        butterbot = XFormPrim(prim_path02)
        butterbot.set_world_poses(positions,orientations)

        # ----------------------------------------
        # iterating over array
        # ----------------------------------------
        if goal_reached:
            base_command = commands[idx]
            idx += 1
        elif idx == 5:
            idx = 0


simulation_app.close()

