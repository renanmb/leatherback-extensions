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
