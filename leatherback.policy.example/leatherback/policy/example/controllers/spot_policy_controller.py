
import io
from typing import Optional

import carb
import numpy as np
import omni
import torch
from isaacsim.core.api.controllers.base_controller import BaseController
from isaacsim.core.prims import SingleArticulation
from isaacsim.core.utils.prims import define_prim, get_prim_at_path

# must experiment with the config_loader - general vs bespoke
# if general must add a way to configure it through the python API
from .spot_config_loader import get_articulation_props, get_physics_properties, get_robot_joint_properties, parse_env_config

# Adding the ONNX runtime
import os
import onnxruntime as ort

class SpotPolicyController(BaseController):
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

        if not prim.IsValid():
            prim = define_prim(prim_path, "Xform")
            if usd_path:
                prim.GetReferences().AddReference(usd_path)
            else:
                carb.log_error("unable to add robot usd, usd_path not provided")

        if root_path == None:
            self.robot = SingleArticulation(prim_path=prim_path, name=name, position=position, orientation=orientation)
        else:
            self.robot = SingleArticulation(prim_path=root_path, name=name, position=position, orientation=orientation)

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

    def initialize(
        self,
        physics_sim_view: omni.physics.tensors.SimulationView = None,
        effort_modes: str = "force",
        control_mode: str = "position",
        set_gains: bool = True,
        set_limits: bool = True,
        set_articulation_props: bool = True,
    ) -> None:
        """
        Initializes the robot and sets up the controller.

        Args:
            physics_sim_view (optional): The physics simulation view.
            effort_modes (str, optional): The effort modes. Defaults to "force".
            control_mode (str, optional): The control mode. Defaults to "position".
            set_gains (bool, optional): Whether to set the joint gains. Defaults to True.
            set_limits (bool, optional): Whether to set the limits. Defaults to True.
            set_articulation_props (bool, optional): Whether to set the articulation properties. Defaults to True.
        """
        self.robot.initialize(physics_sim_view=physics_sim_view)
        self.robot.get_articulation_controller().set_effort_modes(effort_modes)
        self.robot.get_articulation_controller().switch_control_mode(control_mode)
        max_effort, max_vel, stiffness, damping, self.default_pos, self.default_vel = get_robot_joint_properties(
            self.policy_env_params, self.robot.dof_names
        )
        if set_gains:
            self.robot._articulation_view.set_gains(stiffness, damping)
        if set_limits:
            self.robot._articulation_view.set_max_efforts(max_effort)
            self.robot._articulation_view.set_max_joint_velocities(max_vel)
        if set_articulation_props:
            self._set_articulation_props()

    def _set_articulation_props(self) -> None:
        """
        Sets the articulation root properties from the policy environment parameters.
        """
        articulation_prop = get_articulation_props(self.policy_env_params)

        solver_position_iteration_count = articulation_prop.get("solver_position_iteration_count")
        solver_velocity_iteration_count = articulation_prop.get("solver_velocity_iteration_count")
        stabilization_threshold = articulation_prop.get("stabilization_threshold")
        enabled_self_collisions = articulation_prop.get("enabled_self_collisions")
        sleep_threshold = articulation_prop.get("sleep_threshold")

        if solver_position_iteration_count not in [None, float("inf")]:
            self.robot.set_solver_position_iteration_count(solver_position_iteration_count)
        if solver_velocity_iteration_count not in [None, float("inf")]:
            self.robot.set_solver_velocity_iteration_count(solver_velocity_iteration_count)
        if stabilization_threshold not in [None, float("inf")]:
            self.robot.set_stabilization_threshold(stabilization_threshold)
        if isinstance(enabled_self_collisions, bool):
            self.robot.set_enabled_self_collisions(enabled_self_collisions)
        if sleep_threshold not in [None, float("inf")]:
            self.robot.set_sleep_threshold(sleep_threshold)

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
            outputs = self.session.run(output_names, ort_inputs)
            # Get output and flatten to 1D array like .view(-1).numpy()
            action = outputs[0].reshape(-1)
        # end region ONNX
        
        return action

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

# Torch obs and actions
# [ 3.55045653e-01 -2.97760044e-05 -2.75765357e-01  4.87735511e-04
#  -7.53019088e-01  1.02547855e-04 -3.88556550e-03 -9.96758393e-05
#  -9.99992446e-01  0.00000000e+00  0.00000000e+00  0.00000000e+00
#  -9.28463418e-02  9.26030296e-02 -8.88389492e-02  8.85685211e-02
#  -7.28533113e-01 -7.28490421e-01 -9.27930421e-01 -9.27923194e-01
#   9.73495483e-01  9.73346472e-01  9.71988618e-01  9.71962333e-01
#   1.08871555e+00 -1.09006476e+00  1.87726939e+00 -1.87811220e+00
#   1.57401724e+01  1.57396240e+01  1.61292458e+01  1.61281548e+01
#  -4.26473045e+01 -4.26454849e+01 -4.34234009e+01 -4.34203339e+01
#   0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
#   0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
#   0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
# [-1.1420251   0.49554253  0.7358983   0.8543083  -1.832414   -1.2075065
#  -1.5706075  -1.4929144   1.266975   -0.3193593   1.33172     1.0254235 ]
# [ 2.36350346e-01 -1.23990629e-02 -4.65317327e-01 -7.47620230e-01
#  -1.10109528e+00  1.71383650e-01 -2.26552359e-02  9.78485644e-03
#  -9.99695452e-01  2.00000000e+00  0.00000000e+00  0.00000000e+00
#  -7.57222533e-02  8.93462928e-02 -2.10831225e-02  7.20812645e-02
#  -5.19308084e-01 -4.72965562e-01 -6.88473350e-01 -6.76793313e-01
#   4.88680243e-01  3.37104082e-01  4.70076919e-01  4.36783671e-01
#   4.57340449e-01  1.71513438e-01  4.49495697e+00 -2.23059282e-01
#   7.52083302e+00  1.00018682e+01  9.85732079e+00  1.05642757e+01
#  -1.35736599e+01 -2.13830872e+01 -1.38935833e+01 -1.56575956e+01
#  -1.14202511e+00  4.95542526e-01  7.35898316e-01  8.54308307e-01
#  -1.83241403e+00 -1.20750654e+00 -1.57060754e+00 -1.49291444e+00
#   1.26697505e+00 -3.19359303e-01  1.33171999e+00  1.02542353e+00]
# [-1.9123288   0.9221938  -0.17080104  0.82162756 -1.0934291  -0.33516392
#  -1.9421065  -0.969033    0.98640877 -0.7520321   0.6602783   2.0751028 ]

# [ 3.55045653e-01 -2.97760044e-05 -2.75765357e-01  4.87735511e-04
#  -7.53019088e-01  1.02547855e-04 -3.88556550e-03 -9.96758393e-05
#  -9.99992446e-01  0.00000000e+00  0.00000000e+00  0.00000000e+00
#  -9.28463418e-02  9.26030296e-02 -8.88389492e-02  8.85685211e-02
#  -7.28533113e-01 -7.28490421e-01 -9.27930421e-01 -9.27923194e-01
#   9.73495483e-01  9.73346472e-01  9.71988618e-01  9.71962333e-01
#   1.08871555e+00 -1.09006476e+00  1.87726939e+00 -1.87811220e+00
#   1.57401724e+01  1.57396240e+01  1.61292458e+01  1.61281548e+01
#  -4.26473045e+01 -4.26454849e+01 -4.34234009e+01 -4.34203339e+01
#   0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
#   0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00
#   0.00000000e+00  0.00000000e+00  0.00000000e+00  0.00000000e+00]
# [-1.1169034   0.73662144 -1.2117995   0.3732706  -1.7603846  -3.2634368
#  -1.8045475  -0.93836284  0.64597756  0.8874576  -0.08557706  0.6719725 ]
# [ 2.07369061e-01  1.29008468e-02 -4.41449491e-01  1.05433004e+00
#  -9.46720429e-01 -4.35932667e-02 -2.16513988e-02 -1.45084400e-02
#  -9.99660303e-01  2.00000000e+00  0.00000000e+00  0.00000000e+00
#  -1.00743500e-01  6.27032466e-02 -8.54792468e-02  3.93748194e-02
#  -5.06391817e-01 -5.46556914e-01 -6.64936012e-01 -6.60347021e-01
#   4.32780504e-01  4.83721614e-01  3.44051361e-01  3.95580173e-01
#  -1.17593086e+00 -1.54121745e+00 -8.08825493e-01 -2.61477089e+00
#   8.00611591e+00  4.92044115e+00  1.05743208e+01  1.15809050e+01
#  -1.65401592e+01 -1.41999769e+01 -2.06787148e+01 -1.76795425e+01
#  -1.11690342e+00  7.36621439e-01 -1.21179950e+00  3.73270601e-01
#  -1.76038456e+00 -3.26343679e+00 -1.80454755e+00 -9.38362837e-01
#   6.45977557e-01  8.87457609e-01 -8.55770558e-02  6.71972513e-01]

