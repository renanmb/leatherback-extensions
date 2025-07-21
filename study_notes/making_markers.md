# Study Note on making Markers

IsaacSim has a builtin api to make spheres.

```python
from isaacsim.core.api.objects import VisualSphere

VisualSphere(
        prim_path="/new_cube_2",
        name="cube_1",
        position=base_command, #np.array([0, 0, 1.0]),
        # scale=np.array([0.6, 0.5, 0.2]),
        # size=1.0,
        radius = 0.1,
        color=np.array([255, 0, 0]),
    )
```

IsaacLab is using the PointInstancer to make visualization markers which is quite elaborate.

IsaacLab has a way to implement visualization markers that is great for debugging models and is not present in IsaacSim.

inside source -> isaaclab -> markers -> visualization_markers.py

Can be called in isaaclab with the following and has implementation examples in the docs:

Creating Visualization Markers

https://isaac-sim.github.io/IsaacLab/main/source/how-to/draw_markers.html#

```python
from isaaclab.markers import VisualizationMarkers
```

The following method updates the markers dynamically in the viewport which are given as .....

```python
# needed to import for allowing type-hinting: np.ndarray | torch.Tensor | None
from __future__ import annotations

import numpy as np
import torch
from dataclasses import MISSING

import isaacsim.core.utils.stage as stage_utils
import omni.kit.commands
import omni.physx.scripts.utils as physx_utils
from pxr import Gf, PhysxSchema, Sdf, Usd, UsdGeom, UsdPhysics, Vt

import isaaclab.sim as sim_utils
from isaaclab.sim.spawners import SpawnerCfg
from isaaclab.utils.configclass import configclass
from isaaclab.utils.math import convert_quat

def visualize(
    self,
    translations: np.ndarray | torch.Tensor | None = None,
    orientations: np.ndarray | torch.Tensor | None = None,
    scales: np.ndarray | torch.Tensor | None = None,
    marker_indices: list[int] | np.ndarray | torch.Tensor | None = None,
):
    """Update markers in the viewport.

    .. note::
        If the prim `PointInstancer` is hidden in the stage, the function will simply return
        without updating the markers. This helps in unnecessary computation when the markers
        are not visible.

    Whenever updating the markers, the input arrays must have the same number of elements
    in the first dimension. If the number of elements is different, the `UsdGeom.PointInstancer`
    will raise an error complaining about the mismatch.

    Additionally, the function supports dynamic update of the markers. This means that the
    number of markers can change between calls. For example, if you have 24 points that you
    want to visualize, you can pass 24 translations, orientations, and scales. If you want to
    visualize only 12 points, you can pass 12 translations, orientations, and scales. The
    function will automatically update the number of markers in the scene.

    The function will also update the marker prototypes based on their prototype indices. For instance,
    if you have two marker prototypes, and you pass the following marker indices: [0, 1, 0, 1], the function
    will update the first and third markers with the first prototype, and the second and fourth markers
    with the second prototype. This is useful when you want to visualize different markers in the same
    scene. The list of marker indices must have the same number of elements as the translations, orientations,
    or scales. If the number of elements is different, the function will raise an error.

    .. caution::
        This function will update all the markers instanced from the prototypes. That means
        if you have 24 markers, you will need to pass 24 translations, orientations, and scales.

        If you want to update only a subset of the markers, you will need to handle the indices
        yourself and pass the complete arrays to this function.

    Args:
        translations: Translations w.r.t. parent prim frame. Shape is (M, 3).
            Defaults to None, which means left unchanged.
        orientations: Quaternion orientations (w, x, y, z) w.r.t. parent prim frame. Shape is (M, 4).
            Defaults to None, which means left unchanged.
        scales: Scale applied before any rotation is applied. Shape is (M, 3).
            Defaults to None, which means left unchanged.
        marker_indices: Decides which marker prototype to visualize. Shape is (M).
            Defaults to None, which means left unchanged provided that the total number of markers
            is the same as the previous call. If the number of markers is different, the function
            will update the number of markers in the scene.

    Raises:
        ValueError: When input arrays do not follow the expected shapes.
        ValueError: When the function is called with all None arguments.
    """
    # check if it is visible (if not then let's not waste time)
    if not self.is_visible():
        return
    # check if we have any markers to visualize
    num_markers = 0
    # resolve inputs
    # -- position
    if translations is not None:
        if isinstance(translations, torch.Tensor):
            translations = translations.detach().cpu().numpy()
        # check that shape is correct
        if translations.shape[1] != 3 or len(translations.shape) != 2:
            raise ValueError(f"Expected `translations` to have shape (M, 3). Received: {translations.shape}.")
        # apply translations
        self._instancer_manager.GetPositionsAttr().Set(Vt.Vec3fArray.FromNumpy(translations))
        # update number of markers
        num_markers = translations.shape[0]
    # -- orientation
    if orientations is not None:
        if isinstance(orientations, torch.Tensor):
            orientations = orientations.detach().cpu().numpy()
        # check that shape is correct
        if orientations.shape[1] != 4 or len(orientations.shape) != 2:
            raise ValueError(f"Expected `orientations` to have shape (M, 4). Received: {orientations.shape}.")
        # roll orientations from (w, x, y, z) to (x, y, z, w)
        # internally USD expects (x, y, z, w)
        orientations = convert_quat(orientations, to="xyzw")
        # apply orientations
        self._instancer_manager.GetOrientationsAttr().Set(Vt.QuathArray.FromNumpy(orientations))
        # update number of markers
        num_markers = orientations.shape[0]
    # -- scales
    if scales is not None:
        if isinstance(scales, torch.Tensor):
            scales = scales.detach().cpu().numpy()
        # check that shape is correct
        if scales.shape[1] != 3 or len(scales.shape) != 2:
            raise ValueError(f"Expected `scales` to have shape (M, 3). Received: {scales.shape}.")
        # apply scales
        self._instancer_manager.GetScalesAttr().Set(Vt.Vec3fArray.FromNumpy(scales))
        # update number of markers
        num_markers = scales.shape[0]
    # -- status
    if marker_indices is not None or num_markers != self._count:
        # apply marker indices
        if marker_indices is not None:
            if isinstance(marker_indices, torch.Tensor):
                marker_indices = marker_indices.detach().cpu().numpy()
            elif isinstance(marker_indices, list):
                marker_indices = np.array(marker_indices)
            # check that shape is correct
            if len(marker_indices.shape) != 1:
                raise ValueError(f"Expected `marker_indices` to have shape (M,). Received: {marker_indices.shape}.")
            # apply proto indices
            self._instancer_manager.GetProtoIndicesAttr().Set(Vt.IntArray.FromNumpy(marker_indices))
            # update number of markers
            num_markers = marker_indices.shape[0]
        else:
            # check that number of markers is not zero
            if num_markers == 0:
                raise ValueError("Number of markers cannot be zero! Hint: The function was called with no inputs?")
            # set all markers to be the first prototype
            self._instancer_manager.GetProtoIndicesAttr().Set([0] * num_markers)
    # set number of markers
    self._count = num_markers
```

Can observe it is directly calling the ```UsdGeomPointInstancer Class Reference``` from the Pixar USD libraries to apply the translations to the Markers:

```python
# apply translations
self._instancer_manager.GetPositionsAttr().Set(Vt.Vec3fArray.FromNumpy(translations))
```

Vt is from Omniverse kit

Vec3fArray - An array of type GfVec3f.

The ```VisualizationMarkersCfg```

```python
import isaaclab.sim as sim_utils
from isaaclab.markers import VisualizationMarkersCfg, VisualizationMarkers

##
# configuration
##

WAYPOINT_CFG = VisualizationMarkersCfg(
    prim_path="/World/Visuals/Cones",
    markers={
        "marker0": sim_utils.SphereCfg(
            radius=0.1,
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 0.0, 0.0)),
        ),
        "marker1": sim_utils.SphereCfg(
            radius=0.1,
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(0.0, 0.0, 1.0)),
        ),
    }
)
```

```python
import isaacsim.core.utils.stage as stage_utils
# create a new prim
stage = stage_utils.get_current_stage()
self._instancer_manager = UsdGeom.PointInstancer.Define(stage, prim_path)
```

```python
def _add_markers_prototypes(self, markers_cfg: dict[str, sim_utils.SpawnerCfg]):
    """Adds markers prototypes to the scene and sets the markers instancer to use them."""
    # add markers based on config
    for name, cfg in markers_cfg.items():
        # resolve prim path
        marker_prim_path = f"{self.prim_path}/{name}"
        # create a child prim for the marker
        marker_prim = cfg.func(prim_path=marker_prim_path, cfg=cfg)
        # make the asset uninstanceable (in case it is)
        # point instancer defines its own prototypes so if an asset is already instanced, this doesn't work.
        self._process_prototype_prim(marker_prim)
        # add child reference to point instancer
        self._instancer_manager.GetPrototypesRel().AddTarget(marker_prim_path)
    # check that we loaded all the prototypes
    prototypes = self._instancer_manager.GetPrototypesRel().GetTargets()
    if len(prototypes) != len(markers_cfg):
        raise RuntimeError(
            f"Failed to load all the prototypes. Expected: {len(markers_cfg)}. Received: {len(prototypes)}."
        )
```