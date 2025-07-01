from typing import Optional

import numpy as np
import omni
import omni.kit.commands
from isaacsim.core.utils.rotations import quat_to_rot_matrix
from isaacsim.core.utils.types import ArticulationAction

# must experiment with the policy controller - general vs bespoke
from leatherback.policy.example.controllers import PolicyController

from isaacsim.storage.native import get_assets_root_path

class LeatherbackPolicy(PolicyController):
    """The Spot quadruped"""

    def __init__(
        self,
        prim_path: str,
        root_path: Optional[str] = None,
        name: str = "spot",
        usd_path: Optional[str] = None,
        policy_path: Optional[str] = None,
        position: Optional[np.ndarray] = None,
        orientation: Optional[np.ndarray] = None,
    ) -> None:
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
        assets_root_path = get_assets_root_path()
        if usd_path == None:
            # Later might be able to add an Asset to show it doesnt exist - easter egg
            # usd_path = assets_root_path + "/Isaac/Robots/BostonDynamics/spot/spot.usd"
            print("File not found")
        

        super().__init__(name, prim_path, root_path, usd_path, policy_path, position, orientation)
        if policy_path == None:
            # self.load_policy(
            #     assets_root_path + "/Isaac/Samples/Policies/Spot_Policies/spot_policy.pt",
            #     assets_root_path + "/Isaac/Samples/Policies/Spot_Policies/spot_env.yaml",
            # )
            print("Policy not found")
        else:
            self.load_policy(
                    policy_path + "/policy_agent.onnx", # policy_path + "/spot_policy.pt",
                    policy_path + "/env.yaml",  # policy_path + "/spot_env.yaml",
                ) 
    
        self._action_scale = 0.2
        # This is dependent on the Action Space Size
        # Leatherback has actions space = 2
        self._previous_action = np.zeros(2)
        self._policy_counter = 0

    # region Observation
    # This need to be replaced to something similar like the IsaacLab get observations
    def _compute_observation(self, command):
        """
        Compute the observation vector for the policy

        Argument:
        command (np.ndarray) -- the waypoint goal (x, y, z)

        Returns:
        np.ndarray -- The observation vector.

        position error
        heading error cosine
        heading error sine
        root_lin_vel_b[:, 0]
        root_lin_vel_b[:, 1]
        root_ang_vel_w[:, 2]
        _throttle_state
        _steering_state

        """
        # this is using the articulation type 
        # from isaacsim.core.prims import SingleArticulation
        lin_vel_I = self.robot.get_linear_velocity()
        ang_vel_I = self.robot.get_angular_velocity()
        pos_IB, q_IB = self.robot.get_world_pose()

        R_IB = quat_to_rot_matrix(q_IB)
        R_BI = R_IB.transpose()
        lin_vel_b = np.matmul(R_BI, lin_vel_I)
        ang_vel_b = np.matmul(R_BI, ang_vel_I)
        gravity_b = np.matmul(R_BI, np.array([0.0, 0.0, -1.0]))

        # The order of observations matter
        # leatherback has 8 observations
        obs = np.zeros(8)
        # Base lin vel
        obs[:3] = lin_vel_b
        # Base ang vel
        obs[3:6] = ang_vel_b
        # Gravity
        obs[6:9] = gravity_b
        # Command
        obs[9:12] = command
        # Joint states
        current_joint_pos = self.robot.get_joint_positions()
        current_joint_vel = self.robot.get_joint_velocities()
        obs[12:24] = current_joint_pos - self.default_pos
        obs[24:36] = current_joint_vel
        # Previous Action
        obs[36:48] = self._previous_action

        return obs

    def forward(self, dt, command):
        """
        Compute the desired torques and apply them to the articulation

        Argument:
        dt (float) -- Timestep update in the world.
        command (np.ndarray) -- the robot command (v_x, v_y, w_z)

        """
        if self._policy_counter % self._decimation == 0:
            obs = self._compute_observation(command)
            self.action = self._compute_action(obs)
            self._previous_action = self.action.copy()

        action = ArticulationAction(joint_positions=self.default_pos + (self.action * self._action_scale))
        self.robot.apply_action(action)

        self._policy_counter += 1
