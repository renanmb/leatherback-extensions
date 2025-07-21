import io
from typing import Optional

import carb
import numpy as np
import omni
import torch
from isaacsim.core.api.controllers.base_controller import BaseController
# from omni.isaac.wheeled_robots.controllers import AckermannController # use this instead of BaseController
from isaacsim.robot.wheeled_robots.controllers.ackermann_controller import AckermannController

from leatherback.policy.example.ackermann_robot import AckermannRobot

from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.prims import define_prim, get_prim_at_path

# must experiment with the config_loader - general vs bespoke
# if general must add a way to configure it through the python API
from .config_loader import get_articulation_props, get_physics_properties, get_robot_joint_properties, parse_env_config

# Adding the ONNX runtime
import os
import onnxruntime as ort

# NOTE: May be best to inherit the AckermannController and add the necessary logic to run the Policy
class PolicyController(BaseController):
# class PolicyController(AckermannController):

    """
    A controller that loads and executes a policy from a file.

    Args:
        name (str): The name of the controller.
        prim_path (str): The path to the prim in the stage.
        root_path (Optional[str], None): The path to the articulation root of the robot
        usd_path (Optional[str], optional): The path to the USD file. Defaults to None.
        position (Optional[np.ndarray], optional): The initial position of the robot. Defaults to None.
        orientation (Optional[np.ndarray], optional): The initial orientation of the robot. Defaults to None.

    Attributes:
        robot (SingleArticulation): The robot articulation.
    """

    def __init__(
        self,
        name: str,
        prim_path: str,
        root_path: Optional[str] = None,
        usd_path: Optional[str] = None,
        policy_path: Optional[str] = None,
        position: Optional[np.ndarray] = None,
        orientation: Optional[np.ndarray] = None,
    ) -> None:

        prim = get_prim_at_path(prim_path)
        """
        AckermannController uses a bicycle model for Ackermann steering. The controller computes the left turning angle, right turning angle, and the rotation velocity of each wheel of a robot with no slip angle. The controller can be used to find the appropriate joint values of a wheeled robot with an Ackermann steering mechanism.

        Args:

            name (str):                          [description]
            wheel_base (float):                  0.32   Distance between front and rear axles in m
            track_width (float):                 0.24   Distance between left and right wheels of the robot in m
            front_wheel_radius (float):          0.052  Radius of the front wheels of the robot in m. Defaults to 0.0 m but will equal back_wheel_radius if no value is inputted.
            back_wheel_radius (float):           0.052  Radius of the back wheels of the robot in m. Defaults to 0.0 m but will equal front_wheel_radius if no value is inputted.
            max_wheel_velocity (float):          20     Maximum angular velocity of the robot wheel in rad/s. Parameter is ignored if set to 0.0.
            invert_steering (bool):              Set to true for rear wheel steering
            max_wheel_rotation_angle (float):    0.7854 The maximum wheel steering angle for the steering wheels. Defaults to 6.28 rad. Parameter is ignored if set to 0.0.
            max_acceleration (float):            1.0    The maximum magnitude of acceleration for the robot in m/s^2. Parameter is ignored if set to 0.0.
            max_steering_angle_velocity (float): 1.0    The maximum magnitude of desired rate of change for steering angle in rad/s. Parameter is ignored if set to 0.0.
        """

        wheel_base = 0.32
        track_width = 0.24
        front_wheel_radius = 0.052
        back_wheel_radius = 0.052
        max_wheel_velocity = 20.0
        # invert_steering: bool = False,
        max_wheel_rotation_angle = 0.7854
        max_acceleration = 1.0
        max_steering_angle_velocity = 1.0

        self.wheel_base = wheel_base # np.fabs(wheel_base)
        self.track_width = track_width # np.fabs(track_width)
        self.front_wheel_radius = front_wheel_radius # np.fabs(front_wheel_radius)
        self.back_wheel_radius = back_wheel_radius # np.fabs(back_wheel_radius)
        self.max_wheel_velocity = max_wheel_velocity # np.fabs(max_wheel_velocity)
        # self.invert_steering = invert_steering
        self.max_wheel_rotation_angle = max_wheel_rotation_angle # np.fabs(max_wheel_rotation_angle)
        self.max_acceleration = max_acceleration # np.fabs(max_acceleration)
        self.max_steering_angle_velocity = max_steering_angle_velocity # np.fabs(max_steering_angle_velocity)

        self.controller = AckermannController(
            name = name,
            wheel_base =                  self.wheel_base,
            track_width =                 self.track_width,
            front_wheel_radius =          self.front_wheel_radius,
            # back_wheel_radius =           self.back_wheel_radius,
            max_wheel_velocity =          self.max_wheel_velocity,
            # invert_steering =             self.invert_steering,
            max_wheel_rotation_angle =    self.max_wheel_rotation_angle,
            max_acceleration =            self.max_acceleration,
            max_steering_angle_velocity = self.max_steering_angle_velocity,
        )

        if not prim.IsValid():
            prim = define_prim(prim_path, "Xform")
            if usd_path:
                prim.GetReferences().AddReference(usd_path)
            else:
                carb.log_error("unable to add robot usd, usd_path not provided")

        if root_path == None:
            # self.robot = SingleArticulation(prim_path=prim_path, name=name, position=position, orientation=orientation)
            self.robot = AckermannRobot(
                            prim_path=prim_path,
                            name=name,
                            position=position,
                            throttle_dof_names=[
                                "Wheel__Knuckle__Front_Left", 
                                "Wheel__Knuckle__Front_Right",
                                "Wheel__Upright__Rear_Right",
                                "Wheel__Upright__Rear_Left"
                            ],
                            steering_dof_names=[
                                "Knuckle__Upright__Front_Right",
                                "Knuckle__Upright__Front_Left"
                            ]
                        )
        else:
            # self.robot = SingleArticulation(prim_path=root_path, name=name, position=position, orientation=orientation)
            self.robot = AckermannRobot(
                            prim_path=root_path,
                            name=name,
                            position=position,
                            throttle_dof_names=[
                                "Wheel__Knuckle__Front_Left", 
                                "Wheel__Knuckle__Front_Right",
                                "Wheel__Upright__Rear_Right",
                                "Wheel__Upright__Rear_Left"
                            ],
                            steering_dof_names=[
                                "Knuckle__Upright__Front_Right",
                                "Knuckle__Upright__Front_Left"
                            ]
                        )

    def load_policy(self, policy_file_path, policy_env_path) -> None:
        """
        Loads a policy from a file.

        Args:
            policy_file_path (str): The path to the policy file. Example: spot_policy.pt
            policy_env_path (str): The path to the environment configuration file. Example: spot_env.yaml
        """
        if policy_file_path.endswith('.pt') or policy_file_path.endswith('.pth'):
            file_content = omni.client.read_file(policy_file_path)[2]
            file = io.BytesIO(memoryview(file_content).tobytes())
            # Loading a Torch JIT file for Inference
            self.policy = torch.jit.load(file)
            self._isJIT = 1
        # region ONNX
        # Add here an option for ONNX inference
        elif policy_file_path.endswith('.onnx'):
            # Unnecessary Byte stream for now
            file_content = omni.client.read_file(policy_file_path)[2]
            file = io.BytesIO(memoryview(file_content).tobytes())
            # Load ONNX model 
            self.session = ort.InferenceSession(policy_file_path)
            self._isJIT = 0
        # end of region ONNX
        self.policy_env_params = parse_env_config(policy_env_path)

        self._decimation, self._dt, self.render_interval = get_physics_properties(self.policy_env_params)
    
    # This is general, it is getting the Observations and returning the inference output
    def _compute_action(self, obs: np.ndarray) -> np.ndarray:
        """
        Computes the action from the observation using the loaded policy.

        Args:
            obs (np.ndarray): The observation.

        Returns:
            np.ndarray: The action.
        """
        if self._isJIT == 1:
            with torch.no_grad():
                obs = torch.from_numpy(obs).view(1, -1).float()
                action = self.policy(obs).detach().view(-1).numpy()
        # region ONNX
        # Add support to compute actions using the ONNX runtime   
        # Need to fix the Tensor giving output and input need o match     
        elif self._isJIT == 0:
            # Prepare inputs assuming input_tensor is a single input
            obs = torch.from_numpy(obs).view(1, -1).float() # seems reduntant but I thought I had to mess with data types so left here
            ort_inputs = {self.session.get_inputs()[0].name: obs.numpy()}
            output_names = [output.name for output in self.session.get_outputs()]
            # print("ONNX output names:", output_names) # output_names = actions
            outputs = self.session.run(output_names, ort_inputs)
            # Get output and flatten to 1D array like .view(-1).numpy()
            action = outputs[0].reshape(-1)
        # end region ONNX
        # return the action from the Ackermann controller
        """Calculate right and left wheel angles and angular velocity of each wheel given steering angle and desired forward velocity.

        Args:
            command (np.ndarray): [desired steering angle (rad), steering_angle_velocity (rad/s), desired velocity of robot (m/s), acceleration (m/s^2), delta time (s)]

        Returns:
            ArticulationAction: joint_velocities = [front left wheel, front right wheel, back left wheel, back right wheel]; joint_positions = [left wheel angle, right wheel angle]
        """
        # Setting acceleration, steering velocity, and dt to 0 to instantly reach the target steering and velocity
        acceleration = 0.0  # m/s^2
        steering_velocity = 0.0  # rad/s
        dt = 0.0  # secs
        
        """Multiplier for the throttle velocity. The action is in the range [-1, 1] and the radius of the wheel is 0.06m"""
        throttle_scale = 1 # when set to 2 it trains but the cars are flying, 3 you get NaNs
        throttle_max = 1 #50.0 # throttle_max = 60.0
        
        """Multiplier for the steering position. The action is in the range [-1, 1]"""
        steering_scale = 0.1 # steering_scale = math.pi / 4.0
        steering_max = 1 #0.75
        
        _throttle = np.clip(action[0]*throttle_scale, -throttle_max, throttle_max*1)
        _steering = np.clip(action[1]*steering_scale, -steering_max, steering_max)
        
        desired_forward_vel = _throttle # action[0]
        desired_steering_angle = _steering  # action[1]

        actions = self.controller.forward([desired_steering_angle, steering_velocity, desired_forward_vel, acceleration, dt])
        # Seems to have numerical stability issues with the model
        # action = [ throttle, steering ]
        # print(action)
        # [ 1.5507218e+38 -9.5658446e+37]
        # [-1.0059319e+38 -3.7394159e+37] 
        # [ 1.8587413e+38 -1.1465905e+38]
        # print(actions) 
        # {'joint_positions': (-0.6287975571457335, -0.7854), 'joint_velocities': (20.0, 20.0, 20.0, 12.499972450911129), 'joint_efforts': None}
        # {'joint_positions': (-0.6287975571457335, -0.7854), 'joint_velocities': (-20.0, -20.0, -20.0, -12.499972450911129), 'joint_efforts': None}
        # {'joint_positions': (-0.6287975571457335, -0.7854), 'joint_velocities': (20.0, 20.0, 20.0, 12.499972450911129), 'joint_efforts': None}
        return action, actions

    # These are implemented in the leatherback/leatherback.py
    def _compute_observation(self) -> NotImplementedError:
        """
        Computes the observation. Not implemented.
        """

        raise NotImplementedError(
            "Compute observation need to be implemented, expects np.ndarray in the structure specified by env yaml"
        )

    # These are implemented in the leatherback/leatherback.py
    def forward(self) -> NotImplementedError:
        """
        Forwards the controller. Not implemented.
        """
        raise NotImplementedError(
            "Forward needs to be implemented to compute and apply robot control from observations"
        )

    def post_reset(self) -> None:
        """
        Called after the controller is reset.
        """
        self.robot.post_reset()

# TODO
# Experiment with bindings, iostreams and better logic for the ONNX vs JIT
    # # Create an ONNX Runtime session with the provided model
    # def create_session(model: str) -> onnxruntime.InferenceSession:
    #     providers = ['CPUExecutionProvider']
    #     if torch.cuda.is_available():
    #         providers.insert(0, 'CUDAExecutionProvider')
    #     return onnxruntime.InferenceSession(model, providers=providers)

# Example of Action output infered in the IsaacLab
# tensor([[-0.3962, -1.3037],
#         [-0.1407, -0.9968],
#         [-0.8244, -1.1522],
#         [-0.1197, -0.9371],
#         [-1.1394, -0.9273],
#         [-0.0451, -0.3066],
#         [-1.2442, -0.8159],
#         [-0.1452, -0.0019],
#         [ 0.3477, -1.4767],
#         [-0.8584, -0.9580],
#         [-1.1288, -1.0830],
#         [-0.3721, -1.1228],
#         [-0.4400, -0.7223],
#         [-0.7136, -1.2011],
#         [ 0.1095, -1.0040],
#         [-0.2148, -1.2605],
#         [ 0.0581, -1.2969],
#         [-0.0325, -1.1484],
#         [-0.4180, -1.0050],
#         [-0.9198,  0.8618],
#         [-0.7571, -0.3145],
#         [-0.4018, -1.0053],
#         [-0.2364, -1.2836],
#         [ 0.2598, -0.0577],
#         [-0.1385, -1.2557],
#         [-0.5968, -1.0217],
#         [-1.3275, -0.5586],
#         [-0.9985, -0.8774],
#         [-0.9310, -0.4613],
#         [ 0.3163, -1.3126],
#         [ 0.3497, -0.9634],
#         [-1.0368, -0.8549]], device='cuda:0')