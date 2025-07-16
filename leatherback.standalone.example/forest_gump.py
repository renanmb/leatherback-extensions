import os
import numpy as np
from isaacsim import SimulationApp

simulation_app = SimulationApp({"headless": False})

from isaacsim.core.utils.extensions import enable_extension
import carb
import omni.appwindow  # Contains handle to keyboard
from isaacsim.core.api import World
from isaacsim.core.utils.prims import define_prim, get_prim_at_path
from leatherback.policy.example.leatherback import LeatherbackPolicy
from isaacsim.storage.native import get_assets_root_path

import onnxruntime as rt


script_dir = os.path.dirname(__file__)
relative_path = os.path.join("..", "leatherback")
full_path = os.path.abspath(os.path.join(script_dir, relative_path))
usd_path = os.path.abspath(os.path.join(full_path, "leatherback_simple_better.usd"))
policy_path = os.path.join(script_dir, "../leatherback/policy_agent.onnx")
session = rt.InferenceSession(policy_path)
input_names = session.get_inputs()[0].name
output_names = [output.name for output in session.get_outputs()]

"""Multiplier for the throttle velocity. The action is in the range [-1, 1] and the radius of the wheel is 0.06m"""
throttle_scale = 1 # when set to 2 it trains but the cars are flying, 3 you get NaNs
throttle_max = 50.0 # throttle_max = 60.0
"""Multiplier for the steering position. The action is in the range [-1, 1]"""
steering_scale = 0.1 # steering_scale = math.pi / 4.0
steering_max = 0.75

step_angle = np.pi / 180 * 30  # 5 degrees
phys_i = 0
def on_physics_step(step_size) -> None:
    global phys_i
    global step_angle
    # [ 2.3575e+00, -9.0684e-01,  4.2147e-01, -2.9318e+00, -2.9587e-01, -1.7440e+00, -5.6743e+01,  2.4131e-01]
    # obs = np.array([[6, 0, 0, 0, 0, 0, 0, 0]])
    # obs = np.array([[ 2.3575e+00, -9.0684e-01,  4.2147e-01, -2.9318e+00, -2.9587e-01, -1.7440e+00, -5.6743e+01,  2.4131e-01]])
    obs = np.array([[6.5314e-01, 9.9956e-01, 2.9601e-02, 2.4474e+00, 9.9785e-02, 6.4766e-01, 4.8411e+01, 6.8837e-02]])
    outputs = session.run(output_names, {input_names: obs.astype(np.float32)})
    action = outputs[0].reshape(-1)
    print(action)
    # phys_i += 1
    # if phys_i % 100 == 0:
    #     action = -action
    #     step_angle = -step_angle  # reverse direction every 10 steps
    # robot_art.set_joint_positions([[0, 0, step_angle, -step_angle, 0, 0]])
    _throttle = np.clip(action[0]*throttle_scale, -throttle_max, throttle_max*1)
    _steering = np.clip(action[1]*steering_scale, -steering_max, steering_max)
    robot_art.set_joint_positions([[0, 0, _steering, -_steering, 0, 0]])
    wheel_vel = _throttle
    robot_art.set_joint_velocities([[wheel_vel, wheel_vel, 0, 0, wheel_vel, wheel_vel]])
    


my_world = World(stage_units_in_meters=1.0, physics_dt=1 / 60, rendering_dt=1 / 50)
assets_root_path = get_assets_root_path()

prim = define_prim("/World/Ground", "Xform")
asset_path = assets_root_path + "/Isaac/Environments/Grid/default_environment.usd"
prim.GetReferences().AddReference(asset_path)


lb_prim_path = "/World/Leatherback"
from isaacsim.core.utils.stage import add_reference_to_stage
add_reference_to_stage(usd_path, lb_prim_path)

from isaacsim.core.prims import Articulation
robot_art = Articulation(prim_paths_expr=lb_prim_path, name="Leatherback")

robot_art.set_world_poses(positions=np.array([[0,0,0.5]]))
my_world.reset() # required to have joints available

#print("joint names: ", robot_art.joint_names)
# just for ordering reference
wheel_rr = 'Wheel__Upright__Rear_Right'
wheel_rl = 'Wheel__Upright__Rear_Left'
knuckle_fr = 'Knuckle__Upright__Front_Right'
knuckle_fl = 'Knuckle__Upright__Front_Left'
wheel_knuckle_fr = 'Wheel__Knuckle__Front_Right'
wheel_knuckle_fl = 'Wheel__Knuckle__Front_Left'

# wheel_vel = 6
# robot_art.set_joint_velocities([[wheel_vel, wheel_vel, 0, 0, wheel_vel, wheel_vel]])

my_world.add_physics_callback("physics_step", callback_fn=on_physics_step)

while simulation_app.is_running():
    my_world.step(render=True)

simulation_app.close()