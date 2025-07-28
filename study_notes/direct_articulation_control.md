# Study on Direct Articulation Control

Several objectives by doing a Direct Articulation Control extension.

- Simplify the extension reducing into a single python script, maybe 2 scripts. 
- Study How far we can diverge from the IsaacLab training

IsaacLab for leatherback in its simplest example is trained using direct control of all the joints and the car has the ackermann geometry, so understand whether or not you need a controller interface for training and how far you can deviate from the original setting is interesting.


## Initializing the Robot

The idea of initializing the robot can mean different things depending on the project, for the Nvidia demos like the spot it is using the ```config_loader.py``` to parse the YAML from isaaclab and set the values for effort_modes, for the gains (stiffness and damping), the limits in set_limits as the maximum effort set_max_efforts(max_effort) and maximum joint velocities set_max_joint_velocities(max_vel).

For the extension and samples related to the Ackermann and wheeled robots the initialize method is trying to get the Joint indices.

The method ```get_dof_index``` is from SingleArticulation.

The following code is fromt he ```ackermann_robot.py``` and we must initialize

```python
def initialize(self, physics_sim_view=None) -> None:
    """
    _wheel_dof_indices replaced by _throttle_dof_indices and _steering_dof_indices
    _throttle_dof_indices the joint indices related to the _throttle_dof_names
    
    """
    super().initialize(physics_sim_view=physics_sim_view)
    if self._throttle_dof_names is not None:
        self._throttle_dof_indices = [
            self.get_dof_index(self._throttle_dof_names[i]) for i in range(len(self._throttle_dof_names))
        ]
    if self._steering_dof_names is not None:
        # self._steering_dof_indices = [2, 3]
        self._steering_dof_indices = [
            self.get_dof_index(self._steering_dof_names[i]) for i in range(len(self._steering_dof_names))
        ]
    elif self._throttle_dof_indices or self._steering_dof_indices is None:
        carb.log_error("need to have either joint names or joint indices")

    self._num_wheel_dof = len(self._throttle_dof_indices)
    self._num_steering_dof = len(self._steering_dof_indices)
    # this was an idea
    # self.actuators = {
    #     "joint_positions": self._steering_dof_indices,
    #     "joint_velocities": self._throttle_dof_indices
    # }
    return
```

From the ```class SpotPolicyController(BaseController):``` currently at the ```spot_policy_controller.py``` it is initializing the articulation controller

```python
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
```