# Experiments on Visibility

Create the base prim

```python
from omni.isaac.core.utils.prims import create_prim
from pxr import UsdGeom, Gf

# Create the stage and define a prim path for your base prim
# For example, a Cube as a base
base_prim_path = "/World/Cube"
create_prim(base_prim_path, "Cube")
```

Get the position of the base prim

```python
from omni.isaac.core.utils.prims import get_prim_at_path
# Get the prim object
base_prim = get_prim_at_path(base_prim_path)

# Get the prim's world position
base_pos = UsdGeom.Xformable(base_prim).GetLocalTransformation().ExtractTranslation()
```

Create the second prim 

```python
# Create a new prim on top of the base prim (e.g., another Cube)
top_prim_path = "/World/Cube/TopCube"  # Example nested path
top_prim = create_prim(top_prim_path, "Cube")
```

Position the second prim on top of the first

```python
# Calculate the desired position for the top prim
# (e.g., base_pos + half_height_of_base + half_height_of_top)
# For simplicity, we assume default cube size and place it directly above
top_pos = Gf.Vec3d(base_pos[0], base_pos[1], base_pos[2] + 1.0) # Adjust 1.0 based on actual prim sizes

# Set the position of the top prim
UsdGeom.Xformable(top_prim).AddTranslateOp().Set(top_pos)
```

Set the visibility of the base prim to invisible

```python
from omni.isaac.core.utils.prims import set_prim_visibility

# Set the base prim's visibility to false (invisible)
set_prim_visibility(base_prim, False)
```

## Define() -- what is it ?

```python
import omni.isaac.core.utils.stage as stage_utils
from omni.isaac.core.prims import RigidPrim
>>>
# create a Cube at the given path
stage_utils.get_current_stage().DefinePrim("/World/Xform", "Xform")
stage_utils.get_current_stage().DefinePrim("/World/Xform/Cube", "Cube")
```

```python
import omni.isaac.core.utils.stage as stage_utils
from omni.isaac.core.scenes import Scene
import omni.isaac.core.utils.prims as prims_utils

# For remove_object
stage_utils.add_reference_to_stage("/test_path/cube.usd", "/World/Cube")
scene = Scene()
scene.remove_object("Cube")

# For delete_prim
stage_utils.add_reference_to_stage("/test_path/cube.usd", "/World/Cube")
prims_utils.delete_prim("/World/Cube")
```

## Waypoints from mouse click

There were changes to omni kit as well the IsaacSim api.

Exploring the omni kit widgets

```python
import omni.kit.viewport.utility as vp_utils
viewport_window = vp_utils.get_active_viewport_window()
mouse_x, mouse_y = viewport_window.get_mouse_position()

viewport = vp_utils.get_active_viewport()
ray_origin, ray_direction = viewport.compute_world_ray(mouse_x, mouse_y)
```

Ray casting ??

```python
import omni.physx
import carb

physx_interface = omni.physx.acquire_physx_interface()

# Set max ray length (you can change this depending on scene scale)
max_distance = 1000.0

hit = physx_interface.raycast(ray_origin, ray_direction, max_distance)

if hit["hit"]:
    print("Hit position:", hit["position"])
    print("Hit object:", hit["rigid_body"])
else:
    print("No hit")
```

```python
def get_3d_point_under_cursor():
    import omni.kit.viewport.utility as vp_utils
    import omni.physx

    viewport = vp_utils.get_active_viewport()
    mouse_x, mouse_y = vp_utils.get_active_viewport_window().get_mouse_position()

    ray_origin, ray_dir = viewport.compute_world_ray(mouse_x, mouse_y)

    physx = omni.physx.acquire_physx_interface()
    hit = physx.raycast(ray_origin, ray_dir, 1000.0)

    if hit["hit"]:
        return hit["position"]
    return None
```

## reading Mouse

reading mouse position

```python
import omni
import carb

self.input = carb.input.acquire_input_interface()
self.mouse = omni.appwindow.get_default_app_window().get_mouse()

(x,y) = self.input.get_mouse_coords_pixel(self.mouse)
print(f"get_mouse_coords_pixel : {x,y}")

(x, y) = self.input.get_mouse_coords_normalized(self.mouse)
print(f"get_mouse_coords_normalized : {x, y}")
```

reading mouse state

```python
import omni
import carb

self.input = carb.input.acquire_input_interface()
self.mouse = omni.appwindow.get_default_app_window().get_mouse()

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.LEFT_BUTTON)
if val: print(f"LEFT_BUTTON : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MIDDLE_BUTTON)
if val: print(f"MIDDLE_BUTTON : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.RIGHT_BUTTON)
if val: print(f"RIGHT_BUTTON : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.FORWARD_BUTTON)
if val: print(f"FORWARD_BUTTON : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_RIGHT)
if val: print(f"SCROLL_RIGHT : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_LEFT)
if val: print(f"SCROLL_LEFT : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_UP)
if val: print(f"SCROLL_UP : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.SCROLL_DOWN)
if val: print(f"SCROLL_DOWN : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MOVE_RIGHT)
if val: print(f"MOVE_RIGHT : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MOVE_LEFT)
if val: print(f"MOVE_LEFT : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MOVE_UP)
if val: print(f"MOVE_UP : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.MOVE_DOWN)
if val: print(f"MOVE_DOWN : {val}")

val = self.input.get_mouse_value(self.mouse, carb.input.MouseInput.COUNT)
if val: print(f"COUNT : {val}")
```

## Dependencies

The robotics samples have the following dependencies as reference

```toml
"omni.kit.uiapp" = {}
"isaacsim.core.api" = {}
"isaacsim.core.prims" = {}
"isaacsim.cortex.behaviors" = {}
"isaacsim.cortex.framework" = {}
"isaacsim.examples.browser" = {}
"isaacsim.gui.components" = {}
"isaacsim.robot.manipulators" = {}
"isaacsim.robot.manipulators.examples" = {}
"isaacsim.robot_motion.motion_generation" = {}
"isaacsim.robot.policy.examples" = {}
"isaacsim.examples.extension" = {}
"omni.graph.action" = {}
"omni.graph.nodes" = {}
"omni.graph.core" = {}
"omni.isaac.dynamic_control" = {}
"isaacsim.storage.native" = {}
"isaacsim.robot.wheeled_robots" = {}
"omni.physx" = {}
```

## Error getting the USD

It was the path, need to do a file loader for simplifying loading the policy, and assets


```bash
2025-07-29 20:16:44  [Warning] [omni.usd] Warning: in _ReportErrors at line 2890 of /builds/omniverse/usd-ci/USD/pxr/usd/usd/stage.cpp -- In </World/leatherback>: Could not open asset @/home/goat/Documents/GitHub/renanmb/leatherback-extensions/leatherback.ui.example/leatherback/ui/example/leatherback/leatherback_simple_better.usd@ for reference introduced by @anon:0x74da401d4580:World4.usd@</World/leatherback>. (computing expanded prim index for </World/leatherback> on stage @anon:0x74da401d4580:World4.usd@ <0x74da401d8da0>)
```

## get mouse widget

from the omni.kit.material.library

test_helper.py

```python
async def _simulate_mouse(self, data):
        mouse = omni.appwindow.get_default_app_window().get_mouse()
        input_provider = carb.input.acquire_input_provider()

        window_width = ui.Workspace.get_main_window_width()
        window_height = ui.Workspace.get_main_window_height()
        for type, x, y in data:
            input_provider.buffer_mouse_event(mouse, type, (x / window_width, y / window_height), 0, (x, y))
            await ui_test.human_delay(10)
```

from the omni.kit.material.library

test_drag_drop.py

line 65

```python
# do drag/drop
# fixme - as TreeView cannot get items position, use magic number for 1st icon position
source_pos = (mat_item.position.x, mat_item.position.y)
dest_pos = (preview_widget.screen_position_x+20, preview_widget.screen_position_y+20)
await self._simulate_mouse([(carb.input.MouseEventType.MOVE, source_pos[0], source_pos[1]),
                            (carb.input.MouseEventType.LEFT_BUTTON_DOWN, 0, 0)])
await self._simulate_mouse_steps(source_pos, dest_pos)
await self._simulate_mouse([(carb.input.MouseEventType.LEFT_BUTTON_UP, 0, 0)])
await ui_test.human_delay()
```    

line 128 

```python
# do drag/drop
# fixme - string_widget.screen_position_y is wrong?
source_pos = (mat_item.position.x, mat_item.position.y)
dest_pos = (string_widget.screen_position_x + (string_widget.computed_content_width/2), string_widget.screen_position_y + 46)
await self._simulate_mouse([(carb.input.MouseEventType.MOVE, source_pos[0], source_pos[1]),
                            (carb.input.MouseEventType.LEFT_BUTTON_DOWN, 0, 0)])
await self._simulate_mouse_steps(source_pos, dest_pos)
await self._simulate_mouse([(carb.input.MouseEventType.LEFT_BUTTON_UP, 0, 0)])
await ui_test.human_delay()
```

line 210

```python
# do drag/drop
# fixme - as TreeView cannot get items position, use magic number for 1st icon position
source_pos = (mat_item.position.x, mat_item.position.y)
await self._simulate_mouse([(carb.input.MouseEventType.MOVE, source_pos[0], source_pos[1]),
                            (carb.input.MouseEventType.LEFT_BUTTON_DOWN, 0, 0)])
await self._simulate_mouse_steps(source_pos, prim_ui_pos)
await self._simulate_mouse([(carb.input.MouseEventType.LEFT_BUTTON_UP, 0, 0)])
await ui_test.human_delay(10)
```

