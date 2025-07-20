# How Articulations Work

Notes about how the simulator is controlling the articulations

## IsaacLab stuff

Inside the IsaacLab there is an example how the Isaaclab leverages the builtin APIs in IsaacSim to control the articulations in a programmatically defined number of environments.

Inside the articulation_data.py in the line 230:

```python
##
# Joint commands -- Set into simulation.
##

joint_pos_target: torch.Tensor = None
"""Joint position targets commanded by the user. Shape is (num_instances, num_joints).

For an implicit actuator model, the targets are directly set into the simulation.
For an explicit actuator model, the targets are used to compute the joint torques (see :attr:`applied_torque`),
which are then set into the simulation.
"""

joint_vel_target: torch.Tensor = None
"""Joint velocity targets commanded by the user. Shape is (num_instances, num_joints).

For an implicit actuator model, the targets are directly set into the simulation.
For an explicit actuator model, the targets are used to compute the joint torques (see :attr:`applied_torque`),
which are then set into the simulation.
"""

joint_effort_target: torch.Tensor = None
"""Joint effort targets commanded by the user. Shape is (num_instances, num_joints).

For an implicit actuator model, the targets are directly set into the simulation.
For an explicit actuator model, the targets are used to compute the joint torques (see :attr:`applied_torque`),
which are then set into the simulation.
"""

```

We can see that IsaacLab is sending the control_actions throught the method ```_apply_actuator_model()``` using a tensor instantiated in the object ```_data```

Inside source -> isaaclab -> assets -> articulation

Inside the articulation.py in the line 1443:

```python
def _apply_actuator_model(self):
    """Processes joint commands for the articulation by forwarding them to the actuators.

    The actions are first processed using actuator models. Depending on the robot configuration,
    the actuator models compute the joint level simulation commands and sets them into the PhysX buffers.
    """
    # process actions per group
    for actuator in self.actuators.values():
        # prepare input for actuator model based on cached data
        # TODO : A tensor dict would be nice to do the indexing of all tensors together
        control_action = ArticulationActions(
            joint_positions=self._data.joint_pos_target[:, actuator.joint_indices],
            joint_velocities=self._data.joint_vel_target[:, actuator.joint_indices],
            joint_efforts=self._data.joint_effort_target[:, actuator.joint_indices],
            joint_indices=actuator.joint_indices,
        )
        # compute joint command from the actuator model
        control_action = actuator.compute(
            control_action,
            joint_pos=self._data.joint_pos[:, actuator.joint_indices],
            joint_vel=self._data.joint_vel[:, actuator.joint_indices],
        )
        # update targets (these are set into the simulation)
        if control_action.joint_positions is not None:
            self._joint_pos_target_sim[:, actuator.joint_indices] = control_action.joint_positions
        if control_action.joint_velocities is not None:
            self._joint_vel_target_sim[:, actuator.joint_indices] = control_action.joint_velocities
        if control_action.joint_efforts is not None:
            self._joint_effort_target_sim[:, actuator.joint_indices] = control_action.joint_efforts
        # update state of the actuator model
        # -- torques
        self._data.computed_torque[:, actuator.joint_indices] = actuator.computed_effort
        self._data.applied_torque[:, actuator.joint_indices] = actuator.applied_effort
        # -- actuator data
        self._data.soft_joint_vel_limits[:, actuator.joint_indices] = actuator.velocity_limit
        # TODO: find a cleaner way to handle gear ratio. Only needed for variable gear ratio actuators.
        if hasattr(actuator, "gear_ratio"):
            self._data.gear_ratio[:, actuator.joint_indices] = actuator.gear_ratio
```

The object self.actuators is a dictionary where the Keys are 

```python
actuators: dict[str, ActuatorBase]
"""Dictionary of actuator instances for the articulation.

The keys are the actuator names and the values are the actuator instances. The actuator instances
are initialized based on the actuator configurations specified in the :attr:`ArticulationCfg.actuators`
attribute. They are used to compute the joint commands during the :meth:`write_data_to_sim` function.
"""
```

It can only be a type of joint like joint_positions or joint_velocities or joint_efforts and its associated joint_indices.

```python
joint_positions=self._data.joint_pos_target[:, actuator.joint_indices]
joint_velocities=self._data.joint_vel_target[:, actuator.joint_indices]
joint_efforts=self._data.joint_effort_target[:, actuator.joint_indices]
```

ArticulationData is inside the articulation_data.py at isaaclab assets articulation

It is creating a buffer in the initialize method to contain all the information of the articulations.

```python
# container for data access
self._data = ArticulationData(self.root_physx_view, self.device)
```

Special attention to the:

```python
# -- joint commands (sent to the actuator from the user)
self._data.joint_pos_target = torch.zeros(self.num_instances, self.num_joints, device=self.device)
self._data.joint_vel_target = torch.zeros_like(self._data.joint_pos_target)
self._data.joint_effort_target = torch.zeros_like(self._data.joint_pos_target)
```

```python
def _create_buffers(self):
    # constants
    self._ALL_INDICES = torch.arange(self.num_instances, dtype=torch.long, device=self.device)

    # external forces and torques
    self.has_external_wrench = False
    self._external_force_b = torch.zeros((self.num_instances, self.num_bodies, 3), device=self.device)
    self._external_torque_b = torch.zeros_like(self._external_force_b)

    # asset named data
    self._data.joint_names = self.joint_names
    self._data.body_names = self.body_names
    # tendon names are set in _process_fixed_tendons function

    # -- joint properties
    self._data.default_joint_pos_limits = self.root_physx_view.get_dof_limits().to(self.device).clone()
    self._data.default_joint_stiffness = self.root_physx_view.get_dof_stiffnesses().to(self.device).clone()
    self._data.default_joint_damping = self.root_physx_view.get_dof_dampings().to(self.device).clone()
    self._data.default_joint_armature = self.root_physx_view.get_dof_armatures().to(self.device).clone()
    self._data.default_joint_friction_coeff = (
        self.root_physx_view.get_dof_friction_coefficients().to(self.device).clone()
    )

    self._data.joint_pos_limits = self._data.default_joint_pos_limits.clone()
    self._data.joint_vel_limits = self.root_physx_view.get_dof_max_velocities().to(self.device).clone()
    self._data.joint_effort_limits = self.root_physx_view.get_dof_max_forces().to(self.device).clone()
    self._data.joint_stiffness = self._data.default_joint_stiffness.clone()
    self._data.joint_damping = self._data.default_joint_damping.clone()
    self._data.joint_armature = self._data.default_joint_armature.clone()
    self._data.joint_friction_coeff = self._data.default_joint_friction_coeff.clone()

    # -- body properties
    self._data.default_mass = self.root_physx_view.get_masses().clone()
    self._data.default_inertia = self.root_physx_view.get_inertias().clone()

    # -- joint commands (sent to the actuator from the user)
    self._data.joint_pos_target = torch.zeros(self.num_instances, self.num_joints, device=self.device)
    self._data.joint_vel_target = torch.zeros_like(self._data.joint_pos_target)
    self._data.joint_effort_target = torch.zeros_like(self._data.joint_pos_target)
    # -- joint commands (sent to the simulation after actuator processing)
    self._joint_pos_target_sim = torch.zeros_like(self._data.joint_pos_target)
    self._joint_vel_target_sim = torch.zeros_like(self._data.joint_pos_target)
    self._joint_effort_target_sim = torch.zeros_like(self._data.joint_pos_target)

    # -- computed joint efforts from the actuator models
    self._data.computed_torque = torch.zeros_like(self._data.joint_pos_target)
    self._data.applied_torque = torch.zeros_like(self._data.joint_pos_target)

    # -- other data that are filled based on explicit actuator models
    self._data.soft_joint_vel_limits = torch.zeros(self.num_instances, self.num_joints, device=self.device)
    self._data.gear_ratio = torch.ones(self.num_instances, self.num_joints, device=self.device)

    # soft joint position limits (recommended not to be too close to limits).
    joint_pos_mean = (self._data.joint_pos_limits[..., 0] + self._data.joint_pos_limits[..., 1]) / 2
    joint_pos_range = self._data.joint_pos_limits[..., 1] - self._data.joint_pos_limits[..., 0]
    soft_limit_factor = self.cfg.soft_joint_pos_limit_factor
    # add to data
    self._data.soft_joint_pos_limits = torch.zeros(self.num_instances, self.num_joints, 2, device=self.device)
    self._data.soft_joint_pos_limits[..., 0] = joint_pos_mean - 0.5 * joint_pos_range * soft_limit_factor
    self._data.soft_joint_pos_limits[..., 1] = joint_pos_mean + 0.5 * joint_pos_range * soft_limit_factor
```

## IsaacSim Stuff

Inside the isaacsim exts isaacsim.core.api -> isaacsim -> core -> api -> controllers

Inside the articulation_controller.py at line 38

The method apply_action() is being used to apply the changes to the joints in the simulator. ArticulationController is either used directly or through class interfaces such as single_articulation.py 

from isaacsim.core.prims import SingleArticulation

```python
def apply_action(self, control_actions: ArticulationAction) -> None:
    """Apply joint positions, velocities and/or efforts to control an articulation

    Args:
        control_actions (ArticulationAction): actions to be applied for next physics step.
        indices (Optional[Union[list, np.ndarray]], optional): degree of freedom indices to apply actions to.
                                                                Defaults to all degrees of freedom.

    .. hint::

        High stiffness makes the joints snap faster and harder to the desired target,
        and higher damping smoothes but also slows down the joint's movement to target

        * For position control, set relatively high stiffness and low damping (to reduce vibrations)
        * For velocity control, stiffness must be set to zero with a non-zero damping
        * For effort control, stiffness and damping must be set to zero

    Example:

    .. code-block:: python

        >>> from isaacsim.core.utils.types import ArticulationAction
        >>>
        >>> # move all the robot joints to the indicated position
        >>> action = ArticulationAction(joint_positions=np.array([0.0, -1.0, 0.0, -2.2, 0.0, 2.4, 0.8, 0.04, 0.04]))
        >>> prim.apply_action(action)
        >>>
        >>> # close the robot fingers: panda_finger_joint1 (7) and panda_finger_joint2 (8) to 0.0
        >>> action = ArticulationAction(joint_positions=np.array([0.0, 0.0]), joint_indices=np.array([7, 8]))
        >>> prim.apply_action(action)
    """
    self._articulation_controller.apply_action(control_actions=control_actions)
    return
```

from isaacsim.core.api.controllers.articulation_controller import ArticulationController

```python
def apply_action(self, control_actions: ArticulationAction) -> None:
    """[summary]

    Args:
        control_actions (ArticulationAction): actions to be applied for next physics step.
        indices (Optional[Union[list, np.ndarray]], optional): degree of freedom indices to apply actions to.
                                                                Defaults to all degrees of freedom.

    Raises:
        Exception: [description]
    """
    applied_actions = self.get_applied_action()
    joint_positions = control_actions.joint_positions
    if control_actions.joint_indices is None:
        joint_indices = self._articulation_view._backend_utils.resolve_indices(
            control_actions.joint_indices, applied_actions.joint_positions.shape[0], self._articulation_view._device
        )
    else:
        joint_indices = control_actions.joint_indices

    if control_actions.joint_positions is not None:
        joint_positions = self._articulation_view._backend_utils.convert(
            control_actions.joint_positions, device=self._articulation_view._device
        )
        joint_positions = self._articulation_view._backend_utils.expand_dims(joint_positions, 0)
        for i in range(control_actions.get_length()):
            if joint_positions[0][i] is None or np.isnan(
                self._articulation_view._backend_utils.to_numpy(joint_positions[0][i])
            ):
                joint_positions[0][i] = applied_actions.joint_positions[joint_indices[i]]
    joint_velocities = control_actions.joint_velocities
    if control_actions.joint_velocities is not None:
        joint_velocities = self._articulation_view._backend_utils.convert(
            control_actions.joint_velocities, device=self._articulation_view._device
        )
        joint_velocities = self._articulation_view._backend_utils.expand_dims(joint_velocities, 0)
        for i in range(control_actions.get_length()):
            if joint_velocities[0][i] is None or np.isnan(joint_velocities[0][i]):
                joint_velocities[0][i] = applied_actions.joint_velocities[joint_indices[i]]
    joint_efforts = control_actions.joint_efforts
    if control_actions.joint_efforts is not None:
        joint_efforts = self._articulation_view._backend_utils.convert(
            control_actions.joint_efforts, device=self._articulation_view._device
        )
        joint_efforts = self._articulation_view._backend_utils.expand_dims(joint_efforts, 0)
        for i in range(control_actions.get_length()):
            if joint_efforts[0][i] is None or np.isnan(joint_efforts[0][i]):
                joint_efforts[0][i] = 0
    self._articulation_view.apply_action(
        ArticulationActions(
            joint_positions=joint_positions,
            joint_velocities=joint_velocities,
            joint_efforts=joint_efforts,
            joint_indices=control_actions.joint_indices,
        )
    )
    return
```

In the end the control_actions object must contain one of the joint types: joint_positions or joint_velocities or joint_efforts

And must contain the respect joint_indices for that particular joint. IsaacLab deals with this by creating a data buffer before calling the ArticulationActions

```python
self._articulation_view.apply_action(
    ArticulationActions(
        joint_positions=joint_positions,
        joint_velocities=joint_velocities,
        joint_efforts=joint_efforts,
        joint_indices=control_actions.joint_indices,
    )
```