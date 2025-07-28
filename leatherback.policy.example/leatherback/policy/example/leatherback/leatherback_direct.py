# --------------------------------------------
# from leatherback.py 
# --------------------------------------------
from typing import Optional

import numpy as np
import omni
import omni.kit.commands
from isaacsim.core.utils.rotations import quat_to_rot_matrix
from isaacsim.core.utils.types import ArticulationAction
# from isaacsim.core.prims import Articulation

# must experiment with the policy controller - general vs bespoke
# from leatherback.policy.example.controllers import PolicyController

from isaacsim.storage.native import get_assets_root_path

# --------------------------------------------
# From policy_controller.py
# --------------------------------------------
import io
# from typing import Optional

import carb
# import numpy as np
# import omni
import torch
from isaacsim.core.api.controllers.base_controller import BaseController

from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.prims import define_prim, get_prim_at_path


# Adding the ONNX runtime
import os
import onnxruntime as ort

class LeatherbackDirect(BaseController):
    """The Leatherback racer"""
    """
        Initialize robot and load RL policy.

        Args:
            prim_path (str) -- prim path of the robot on the stage
            root_path (Optional[str]): The path to the articulation root of the robot
            name (str) -- name of the quadruped
            usd_path (str) -- robot usd filepath in the directory
            policy_path (str) -- 
            position (np.ndarray) -- position of the robot
            orientation (np.ndarray) -- orientation of the robot

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
        # --------------------------------------------
        # From policy_controller.py
        # --------------------------------------------  
        if not prim.IsValid():
            prim = define_prim(prim_path, "Xform")
            if usd_path:
                prim.GetReferences().AddReference(usd_path)
            else:
                carb.log_error("unable to add robot usd, usd_path not provided")

        assets_root_path = get_assets_root_path()
        if usd_path == None:
            # Later might be able to add an Asset to show it doesnt exist - easter egg
            # usd_path = assets_root_path + "/Isaac/Robots/BostonDynamics/spot/spot.usd"
            print("File not found")
        
        # super().__init__(name, prim_path, root_path, usd_path, policy_path, position, orientation)
        
        # Given the Joint Names the Initialize will find the Joint Indices
        throttle_dof_names=[
            "Wheel__Knuckle__Front_Left", 
            "Wheel__Knuckle__Front_Right",
            "Wheel__Upright__Rear_Right",
            "Wheel__Upright__Rear_Left"
            ]
        steering_dof_names=[
            "Knuckle__Upright__Front_Right",
            "Knuckle__Upright__Front_Left"
            ]
        self._throttle_dof_names = throttle_dof_names
        self._steering_dof_names = steering_dof_names
        # self._throttle_dof_indices = throttle_dof_indices
        # self._steering_dof_indices = steering_dof_indices

        if policy_path == None:
            # self.load_policy(
            #     assets_root_path + "/Isaac/Samples/Policies/Spot_Policies/spot_policy.pt",
            #     assets_root_path + "/Isaac/Samples/Policies/Spot_Policies/spot_env.yaml",
            # )
            print("Policy not found")
        else:
            self.load_policy(
                    policy_path + "/policy.onnx", # policy_path + "/spot_policy.pt",
                    # policy_path + "/env.yaml",  # policy_path + "/spot_env.yaml",
                ) 
    
        self._action_scale = 1 # 0.2
        # Leatherback has action space = 2
        self._previous_action = np.zeros(2)
        self._policy_counter = 0
        # From the env.yaml
        self._decimation = 4
        self._dt = 0.016666666666666666

        # Need to initialize the articulations here for the throttle and for the velocities.
        if root_path == None:
            self.robot = SingleArticulation(prim_path=prim_path, name=name, position=position, orientation=orientation)
        else:
            self.robot = SingleArticulation(prim_path=root_path, name=name, position=position, orientation=orientation)
            
    def load_policy(self, policy_file_path) -> None:
        """
        Loads a policy from a file.

        Args:
            policy_file_path (str): The path to the policy file. Example: spot_policy.pt or onnx
        """
        if policy_file_path.endswith('.pt') or policy_file_path.endswith('.pth'):
            # Loading a Torch JIT file for Inference
            self.policy = torch.jit.load(policy_file_path)
            self._isJIT = 1
        # region ONNX
        elif policy_file_path.endswith('.onnx'):
            # Load ONNX model 
            self.session = ort.InferenceSession(policy_file_path)
            self._isJIT = 0
        # end of region ONNX

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
        
        # action = [ throttle, steering ]
        return action
    # --------------------------------------------
    # From leatherback.py
    # --------------------------------------------
    def _compute_observation(self, command):
        """
        Compute the observations numpy array to be given for the policy

        Argument:
        command (np.ndarray) -- the waypoint goal (x, y, z)

        Returns:
        np.ndarray -- The observation vector.
        """
        
        lin_vel_I = self.robot.get_linear_velocity()
        ang_vel_I = self.robot.get_angular_velocity()

        # position, orientation = prim.get_world_pose()
        pos_IB, q_IB = self.robot.get_world_pose() 

        R_IB = quat_to_rot_matrix(q_IB)
        R_BI = R_IB.transpose()
        lin_vel_b = np.matmul(R_BI, lin_vel_I)
        ang_vel_b = np.matmul(R_BI, ang_vel_I)
        # gravity_b = np.matmul(R_BI, np.array([0.0, 0.0, -1.0])) # Wonder if gravity can add any benefit
        # Calcualting the position error
        _position_error_vector = command - pos_IB
        _position_error = np.linalg.norm(_position_error_vector) # , axis=-1
        
        # Calculating the Heading Error
        FORWARD_VEC_B = np.array([1.0, 0.0, 0.0]) # Do I need _root_physx_view ?
        quat = q_IB.reshape(-1, 4)
        vec = FORWARD_VEC_B.reshape(-1, 3)
        xyz = quat[:, 1:]
        t = 2 * np.cross(xyz, vec)
        w = quat[:, 0:1]  # shape (N, 1)
        forward_w = vec + w * t + np.cross(xyz, t)

        heading_w = np.arctan2(forward_w[:, 1], forward_w[:, 0])  # shape (N,)

        target_heading_w = np.arctan2(command[1]-pos_IB[1], command[0]-pos_IB[0])
        _heading_error = target_heading_w - heading_w

        obs = np.zeros(8)
        # Position Error
        obs[0] = _position_error
        # Heading error
        obs[1] = np.cos(_heading_error)[:, np.newaxis]
        obs[2] = np.sin(_heading_error)[:, np.newaxis]
        # Linear Velocity X and Y
        obs[3] = lin_vel_b[0]
        obs[4] = lin_vel_b[1]
        # Angular Velocity vZ
        obs[5] = ang_vel_b[2]
        # _throttle_state
        obs[6] = self._previous_action[0] # _throttle_state # self._previous_action[0]
        # _steering_state
        obs[7] = self._previous_action[1] # _steering_state # self._previous_action[1]

        return obs

    def forward(self, dt, command):
        """
        Compute the desired torques and apply them to the articulation

        Argument:
        dt (float) -- Timestep update in the world.
        command (np.ndarray) -- the robot command (v_x, v_y, w_z)

        """
        throttle_scale = 5 # when set to 2 it trains but the cars are flying, 3 you get NaNs
        throttle_max = 50.0 #50.0 # throttle_max = 60.0
        steering_scale = 0.01 # steering_scale = math.pi / 4.0
        steering_max = 0.75

        if self._policy_counter % self._decimation == 0:
            obs = self._compute_observation(command)
            self.action = self._compute_action(obs)
            self._action = self.action.copy()
            # throttle_action and steering_action
            throttle_action = self.action[0]*throttle_scale
            self._action[0] = np.clip(throttle_action, -throttle_max, throttle_max*0.1)
            steering_action = self.action[1]*steering_scale
            self._action[1] = np.clip(steering_action, -steering_max, steering_max)

            self.repeated_arr = np.repeat(self._action, [4, 2])
            self._previous_action = self._action.copy()

        # The ackermann_robot.py is getting the joint indices to generate the proper actions objects for steering and throttle
        steering_action = ArticulationAction(
                joint_positions=self.repeated_arr[-2:],
                joint_indices=self._steering_dof_indices,
            )
        throttle_action = ArticulationAction(
                joint_velocities=self.repeated_arr[:4],
                joint_indices=self._throttle_dof_indices,
            )
        # self.robot.apply_action(action)

        # self.robot.apply_wheel_actions(self.actions) 
        self.robot.apply_action(control_actions=steering_action)
        self.robot.apply_action(control_actions=throttle_action)

        self._policy_counter += 1

    def post_reset(self) -> None:
        """
        Called after the controller is reset.
        """
        self.robot.post_reset()

    # --------------------------------------------
    # From ackermann_robot.py
    # --------------------------------------------
    def initialize(self, physics_sim_view=None) -> None:
        """
        _wheel_dof_indices replaced by _throttle_dof_indices and _steering_dof_indices
        _throttle_dof_indices the joint indices related to the _throttle_dof_names
        
        """
        # super().initialize(physics_sim_view=physics_sim_view)
        self.robot.initialize(physics_sim_view=physics_sim_view)
        if self._throttle_dof_names is not None:
            self._throttle_dof_indices = [
                self.robot.get_dof_index(self._throttle_dof_names[i]) for i in range(len(self._throttle_dof_names))
            ]
        if self._steering_dof_names is not None:
            self._steering_dof_indices = [
                self.robot.get_dof_index(self._steering_dof_names[i]) for i in range(len(self._steering_dof_names))
            ]
        elif self._throttle_dof_indices or self._steering_dof_indices is None:
            carb.log_error("need to have either joint names or joint indices")

        self._num_wheel_dof = len(self._throttle_dof_indices)
        self._num_steering_dof = len(self._steering_dof_indices)

        return