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
from omni.physx.scripts import deformableUtils, physicsUtils  
# the camera stuff ??
from isaacsim.core.utils.viewports import set_camera_view

script_dir = os.path.dirname(__file__)
relative_path = os.path.join("..", "leatherback")
full_path = os.path.abspath(os.path.join(script_dir, relative_path))
usd_path = os.path.abspath(os.path.join(full_path, "leatherback_simple_better.usd"))
butterbot_path = os.path.abspath(os.path.join(full_path, "butterbot_v02.usd"))
butter_path = os.path.abspath(os.path.join(full_path, "butter_tub.usdz"))

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
        positions = np.zeros((1, 3))
        positions[0] = base_command
        # orientations = np.zeros((1, 4))
        # orientations[0] = orientation
        butter = XFormPrim(prim_path03)
        butter.set_world_poses(positions)


# spawn world
# leatherback is configure for physics_dt = 1/60 the spot seems to be physics_dt=1 / 500,
my_world = World(stage_units_in_meters=1.0, physics_dt=1 / 60, rendering_dt=1 / 50)
assets_root_path = get_assets_root_path()
if assets_root_path is None:
    carb.log_error("Could not find Isaac Sim assets folder")

# spawn Default Grid Environment
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
This will turn the leatherback prim invisible and add the butterbot.
'''
prim_path = "/World/leatherback" 
prim_path02 = "/World/butterbot"
prim_path03 = "/World/butter_tub"

prim = stage.GetPrimAtPath(prim_path)
prim02 = define_prim(prim_path02, "Xform")
prim03 = define_prim(prim_path03, "Xform")

# Check if the prim is valid
if prim.IsValid():
    # Get the UsdGeom.Imageable schema for the prim
    imageable = UsdGeom.Imageable(prim)
    # Set the visibility attribute to "invisible"
    imageable.GetVisibilityAttr().Set(UsdGeom.Tokens.invisible)
    # Add the ButterBot and the Butter
    prim02.GetReferences().AddReference(butterbot_path)
    prim03.GetReferences().AddReference(butter_path)
    butter_mesh = UsdGeom.Mesh.Get(stage, prim_path03)
    physicsUtils.set_or_add_scale_op(butter_mesh, scale=Gf.Vec3f(0.03, 0.03, 0.03))
    physicsUtils.set_or_add_orient_op(butter_mesh, orient=Gf.Quatf(0, 0, 0.70710678118, 0.70710678118))
else:
    print(f"Error: Prim at path '{prim_path}' not found.")


# Example: Setting the camera to a specific position and target
camera_position = (5.0, 5.0, 3.0)  # X, Y, Z coordinates of the camera
camera_target = (0.0, 0.0, 0.0)    # X, Y, Z coordinates of the point the camera is looking at
camera_prim_path = "/OmniverseKit_Persp" # Default perspective camera prim path

set_camera_view(eye=camera_position, target=camera_target, camera_prim_path=camera_prim_path)

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
        # commands = np.array([[1, 0, 0],[3, 2, 0],[2, 4, 0],[0, 4, 0],[-1, 2, 0]])
        # This takes roughly 10s to complete
        commands = np.array([[1, 0, 0],[3, 0, 0],[5, 0.2, 0],[7, 0.5, 0],[9, 0.2, 0],[11, 0, 0],[13, 0.2, 0],[15, 0.5, 0]])
        robot1 = XFormPrim(prim_path)
        positions = np.zeros((1, 3))
        positions[0] = position
        orientations = np.zeros((1, 4))
        orientations[0] = orientation
        butterbot = XFormPrim(prim_path02)
        butterbot.set_world_poses(positions,orientations)
        # Makes the camera Chase the Butter Bot
        set_camera_view(eye=camera_position, target=position, camera_prim_path=camera_prim_path)

        # ----------------------------------------
        # iterating over array
        # ----------------------------------------
        if goal_reached:
            base_command = commands[idx]
            idx += 1
        elif idx == 8:
            idx = 0


simulation_app.close()

