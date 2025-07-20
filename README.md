# Example of Extensions to run Inference in IsaacSim

This is a prototype project for developing more complex extensions for IsaacSim focused on running Inference for Neural Networks.

The main idea is to create an workflow to validate models in IsaacSim with more fine control and without all the abstractions in IsaacLab for closing the Sim2Real gap.

By no means this is a stable extension project but it can serve as a great reference for those that want to develop something similar.

Big issues:
matching the actions to the right scale
Do not know if in IsaacLab it is using the Mean Actions 

test simulator runs:

Inside where you put the IsaacSim

```bash
./python.sh ./standalone_examples/api/isaacsim.core.api/add_cubes.py 
```

## Installation

**Step 1** - Go to the isaacsim root installation, (a.k.a where the python.sh is)

**Step 2**- Add the extension path to the ```setup_python_env.sh```

At the very end of the script for the following line 

```bash
export PYTHONPATH=$PYTHONPATH ................ 
```

add the path to your awesome extension, as example:

```bash
:/home/user/Documents/GitHub/renanmb/leatherback-extensions/leatherback.policy.example
```

This is important so the extension manager can locate the extension.

**Step 3** - Install the dependencies

IsaacSim has its own python binaries so you must install dependencies like onnxruntime and onnx.

```bash
~/isaacsim ./python.sh -m pip install onnxruntime onnx
```

This requires further work and automation, IsaacLab has a great example on this.

## Running the Standalone Scripts

Once the extension has been installed and the dependencies satisfied you should be able to run the Standalone Scripts.

For the examples in this repo you must go into the isaacsim root folder (aka where the python.sh is) and run the following command and provide the full path to your standalone script.

For the Leatherback:
```bash
./python.sh /home/goat/Documents/GitHub/renanmb/leatherback-extensions/leatherback.standalone.example/leatherback_standalone.py
```

For the Spot example:
```bash
./python.sh /home/goat/Documents/GitHub/renanmb/leatherback-extensions/leatherback.standalone.example/spot_standalone.py
```

## Design notes

The example with the quadrupeds and humanoids are using the ```BaseController``` in the ```policy_controller.py ```to build a policy controller for the articulations from scratch.

```python
from isaacsim.core.api.controllers.base_controller import BaseController
```

Commanding the robot should be done prior to the physics step using an ```ArticulationAction```, a type provided by ```omni.isaac.core``` to facilitate things like mixed command modes (effort, velocity, and position) and complex robots with multiple types of actions that could be taken. 

This is being done on the ```leatherback.py``` or ```spot.py```

```python
from isaacsim.core.utils.types import ArticulationAction

# for the spot.py
action = ArticulationAction(joint_positions=self.default_pos + (self.action * self._action_scale))
self.robot.apply_action(action)

# for the leatherback.py -- this dont work
action = ArticulationAction(joint_velocities=(self.repeated_arr[:4],),joint_positions=(self.repeated_arr[-2:],),)
self.robot.apply_action(action)

```

However, this seems to be a bad design choice, the complexity does not outweight the advantages also the user will rarely want to command a robot by directly manipulating the joints. So the best way might be to provide a suite of controllers to convert various types of general commands that are inferenced from the Neural Network into specific joint actions. This might create a standard, increase productivity and makes the learning curve easier.

For example, you may want to control your differential or Ackermann base using only throttle and steering commands … without having to worry about convert the values to directly manipulating the joints.

Take the Jetbot as example:

```python
# Assuming a stage context containing a Jetbot at /World/Jetbot
from omni.isaac.wheeled_robots.robots import WheeledRobot
jetbot_prim_path = "/World/Jetbot"
from omni.isaac.wheeled_robots.controllers import DifferentialController

#wrap the articulation in the interface class
jetbot = WheeledRobot(prim_path=jetbot_prim_path,
                      name="Joan",
                      wheel_dof_names=["left_wheel_joint", "right_wheel_joint"]
                     )

throttle = 1.0
steering = 0.5
controller = DifferentialController(name="simple_control", wheel_radius=0.035, wheel_base=0.1)
jetbot.apply_wheel_actions(controller.forward(throttle, steering))
```

The ackermann example found at https://docs.isaacsim.omniverse.nvidia.com/4.5.0/robot_simulation/mobile_robot_controllers.html#ackermann-controller

```python
from isaacsim.robot.wheeled_robots.controllers.ackermann_controller import AckermannController
from leatherback.policy.example.ackermann_robot import AckermannRobot

robot_prim_path = "/World/Leatherback"
robot = AckermannRobot(prim_path=robot_prim_path,
                        name="leatherback",
                        wheel_dof_names=[
                              "Wheel_Upright_Rear_Right", 
                              "Wheel_Upright_Rear_Left",
                              "Knuckle_Upright_Front_Right",
                              "Knuckle_Upright_Front_Left",
                              "Wheel_Knuckle_Front_Right",
                              "Wheel_Knuckle_Front_Left",
                        ]
                      )

wheel_base = 1.65
track_width = 1.25
wheel_radius = 0.25
desired_forward_vel = 1.1  # rad/s
desired_steering_angle = 0.1  # rad

# Setting acceleration, steering velocity, and dt to 0 to instantly reach the target steering and velocity
acceleration = 0.0  # m/s^2
steering_velocity = 0.0  # rad/s
dt = 0.0  # secs

controller = AckermannController(
   "test_controller", wheel_base=wheel_base, track_width=track_width, front_wheel_radius=wheel_radius
)

actions = controller.forward(
      [desired_steering_angle, steering_velocity, desired_forward_vel, acceleration, dt]
)

robot.apply_wheel_actions(actions)
```

Could use the config_loader.py to parse the joint names and their properties as they are located in the env.yaml

```yaml
throttle_dof_name:
- Wheel__Knuckle__Front_Left
- Wheel__Knuckle__Front_Right
- Wheel__Upright__Rear_Right
- Wheel__Upright__Rear_Left
steering_dof_name:
- Knuckle__Upright__Front_Right
- Knuckle__Upright__Front_Left
```

Must design an interface class for the Articulation