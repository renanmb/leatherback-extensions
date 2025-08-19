# Intro

The idea is to use the Default perspective camera prim path with the Extension from the Sensors in order to get 3D point coordinates given mouse pixel coordinates inputs.

```python
camera_prim_path = "/OmniverseKit_Persp" # Default perspective camera prim path
```

The extension Camera Sensors is can get coordinates in 3d given the mouse coordinates.

The extension is adding a camera to the scene

```python
from isaacsim.sensors.camera import Camera
```

```python
self.camera = self.my_world.scene.add(
            Camera(
                prim_path="/World/rig/camera",
                name="camera",
                position=np.array([0.0, 0.0, 25.0]),
                frequency=20,
                resolution=(256, 256),
                orientation=rot_utils.euler_angles_to_quats(np.array([0, 90, 0]), degrees=True),
            )
        )
```        

```python
points_3d = self.camera.get_world_points_from_image_coords(points_2d, np.array([24.94, 24.9]))
```

## Error

Error with ddepth

```bash
get_mouse_coords_pixel : (0.23055556416511536, 0.36222222447395325)
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 158, in _on_global_mouse_event
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:     points_3d = self.camera.get_world_points_from_image_coords(points_2d, np.array([24.94, 24.9]))
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/isaacsim/exts/isaacsim.sensors.camera/isaacsim/sensors/camera/camera.py", line 1507, in get_world_points_from_image_coords
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:     homogenous = self._backend_utils.pad(points_2d, ((0, 0), (0, 1)), value=1.0)
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/isaacsim/exts/isaacsim.core.utils/isaacsim/core/utils/numpy/tensor.py", line 69, in pad
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:     return np.pad(data, pad_width, mode, constant_values=value)
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/isaacsim/extscache/omni.kit.pip_archive-0.0.0+d02c707b.lx64.cp310/pip_prebundle/numpy/lib/arraypad.py", line 748, in pad
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:     pad_width = _as_pairs(pad_width, array.ndim, as_index=True)
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/isaacsim/extscache/omni.kit.pip_archive-0.0.0+d02c707b.lx64.cp310/pip_prebundle/numpy/lib/arraypad.py", line 522, in _as_pairs
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:     return np.broadcast_to(x, (ndim, 2)).tolist()
2025-08-18 00:20:26 [38,910ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/isaacsim/extscache/omni.kit.pip_archive-0.0.0+d02c707b.lx64.cp310/pip_prebundle/numpy/lib/stride_tricks.py", line 413, in broadcast_to
2025-08-18 00:20:26 [38,911ms] [Error] [omni.kit.app._impl] [py stderr]:     return _broadcast_to(array, shape, subok=subok, readonly=True)
2025-08-18 00:20:26 [38,911ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/isaacsim/extscache/omni.kit.pip_archive-0.0.0+d02c707b.lx64.cp310/pip_prebundle/numpy/lib/stride_tricks.py", line 349, in _broadcast_to
2025-08-18 00:20:26 [38,911ms] [Error] [omni.kit.app._impl] [py stderr]:     it = np.nditer(
2025-08-18 00:20:26 [38,911ms] [Error] [omni.kit.app._impl] [py stderr]: ValueError: operands could not be broadcast together with remapped shapes [original->remapped]: (2,2)  and requested shape (1,2)
```

removing the depth

```bash
get_mouse_coords_pixel : (0.3993055522441864, 0.4933333396911621)
2025-08-18 00:21:57 [129,551ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 00:21:57 [129,551ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 00:21:57 [129,551ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 00:21:57 [129,551ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 158, in _on_global_mouse_event
2025-08-18 00:21:57 [129,551ms] [Error] [omni.kit.app._impl] [py stderr]:     points_3d = self.camera.get_world_points_from_image_coords(points_2d, 
2025-08-18 00:21:57 [129,551ms] [Error] [omni.kit.app._impl] [py stderr]: TypeError: Camera.get_world_points_from_image_coords() missing 1 required positional argument: 'depth'
```

## Hypothesis

There is a camera mismatch so I ahve to map the camera resolution with so it coorelates with the pixel coordinates obtained from the mouse.

You need to map viewport mouse position into the camera’s render resolution:

```python
viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
camera_w, camera_h = self.camera.get_resolution()

# Normalize viewport coords -> [0,1]
u = x / viewport_w
v = y / viewport_h

# Scale to camera pixel coords
cam_x = u * camera_w
cam_y = v * camera_h

points_2d = np.array([[cam_x, cam_y]], dtype=np.float32)
depths    = np.array([depth_value], dtype=np.float32)
points_3d = self.camera.get_world_points_from_image_coords(points_2d, depths)
```

Right now you’re hard-coding 24.9. That means you’ll always “unproject” at ~25m.

If you want the actual depth under the cursor, you need the depth buffer from the sensor:

```python
depth_img = self.camera.get_depth()
depth_value = depth_img[int(cam_y), int(cam_x)]
```


The attribute ```get_viewport_size()``` doesnt exist so instead must use something like ```omni.kit.viewport.get_viewport_window_size()```

```python
viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
```

```python
import omni.kit.viewport

viewport_width, viewport_height = omni.kit.viewport.get_viewport_window_size()
```

In the example of extension window.py

```python
from omni import ui
```

It is checking if the mouse is inside the window

```python
(x, y) = self._input.get_mouse_coords_normalized(None)
x *= ui.Workspace.get_main_window_width()
y *= ui.Workspace.get_main_window_height()

rect = WindowRect(self)
if rect.is_inside(x, y):
    return True

if self._parent is not None:
    # Here widget position is different from window
    rect = WidgetRect(self._parent)
    if rect.is_inside(x, y):
        return True

for window in self._valid_windows:
    if window is None:
        continue
    rect = WindowRect(window)
    if rect.is_inside(x, y):
        return True
```                

<!-- EXAMPLE -->

For example this can dock and only show certain UI elements

Example from https://forums.developer.nvidia.com/t/only-show-viewport-and-extension-ui-upon-loading-the-extension/267276

as well mentioned: https://forums.developer.nvidia.com/t/ui-elements-in-isaac-sim/335917

```python
windows = omni.ui.Workspace.get_windows()
for window in windows: 
    if str(window) =="Viewport" or str(window) == "Script Editor":
        omni.ui.Workspace.show_window(str(window), True)
    else:
        omni.ui.Workspace.show_window(str(window), False)
```        

<!-- Example -->

Inside the omni graph ui nodes in the class ```ViewportPressGesture```

This is mapping the pixel coordinates of the mouse with the viewport.

```python
def on_ended(self):
    if not self._start_pos_valid:
        return

    mouse = self.sender.gesture_payload.mouse
    resolution = self._viewport_api.resolution

    # Position in normalized coords
    pos_norm = self._viewport_api.map_ndc_to_texture(mouse)[0]
    pos_norm = (pos_norm[0], 1.0 - pos_norm[1])
    pos_valid = True
    if not all(0.0 <= x <= 1.0 for x in pos_norm):
        pos_valid = False
        pos_norm = [0.0, 0.0]

    # Position in viewport resolution pixels
    pos_pixel = (pos_norm[0] * resolution[0], pos_norm[1] * resolution[1])

    payload = {
        "viewport": self._viewport_window_name,
        "gesture": self._gesture_name,
        "pos_norm_x": pos_norm[0],
        "pos_norm_y": pos_norm[1],
        "pos_pixel_x": pos_pixel[0],
        "pos_pixel_y": pos_pixel[1],
        "pos_valid": pos_valid,
    }
    self._message_bus.push(self._event_type_ended, payload=payload)

    self._start_pos_valid = False
```

<!-- Maybe this is how to get the Depth -->

```python
self._camera.get_current_frame()["distance_to_camera"]
```

There is no attribute distance_to_camera

```bash
2025-08-18 20:11:25 [3,284,000ms] [Error] [omni.kit.app._impl] [py stderr]:     depth_img = self.camera.get_current_frame()["distance_to_camera"]
2025-08-18 20:11:25 [3,284,000ms] [Error] [omni.kit.app._impl] [py stderr]: KeyError: 'distance_to_camera'
```


```bash
get_mouse_coords_pixel : (0.17986111342906952, 0.30888888239860535)
2025-08-18 20:17:10 [3,629,327ms] [Warning] [isaacsim.sensors.camera.camera] [get_depth][/OmniverseKit_Persp] WARNING: Annotator 'distance_to_image_plane' not found. Available annotators: dict_keys(['rendering_time', 'rendering_frame', 'rgba', 'distance_to_camera']). Returning None
depth_img : None
```

now it gets the distance

```bash
get_mouse_coords_pixel : (0.3013888895511627, 0.4399999976158142)
depth_img : [[13.682562  13.682561  13.682563  ... 13.682563  13.682562  13.682563 ]
 [12.821138  12.821136  12.821138  ... 12.821138  12.821137  12.821138 ]
 [12.061757  12.061756  12.061758  ... 12.061758  12.061757  12.061758 ]
 ...
 [ 1.4558295  1.4558294  1.4558294 ...  1.4558293  1.4558293  1.4558295]
 [ 1.4454958  1.4454958  1.4454957 ...  1.4454958  1.445496   1.4454958]
 [ 1.435308   1.4353079  1.4353079 ...  1.435308   1.4353077  1.435308 ]]

```

Now it gets an weird error

```bash
get_mouse_coords_pixel : (0.31458333134651184, 0.5255555510520935)
depth_value : 5.633884429931641
Camera points 3D : [[ 1.0747981  -0.6310528   0.00949851]]
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 110, in on_physics_step
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]:     self.leatherback.forward(step_size, self._base_command)
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/leatherback/leatherback.py", line 154, in forward
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]:     obs = self._compute_observation(command)
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/leatherback/leatherback.py", line 110, in _compute_observation
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]:     target_heading_w = np.arctan2(command[1]-pos_IB[1], command[0]-pos_IB[0])
2025-08-18 20:25:20 [4,119,001ms] [Error] [omni.kit.app._impl] [py stderr]: IndexError: index 1 is out of bounds for axis 0 with size 1
```

Solution was the flatten the array

## Issue with Mapping

Mapping is wrong maybe need to get the Coordinates in pixel and convert it to the frame of reference of the viewport

```python
import omni.kit.viewport.utility as vp_utils

viewport = vp_utils.get_active_viewport_window()
(x_global, y_global) = self._input.get_mouse_coords_pixel(self.mouse)
# Get viewport rect in window coordinates
rect = viewport.get_window_rect()   # (x, y, width, height)

vx, vy, vw, vh = rect
x_viewport = x_global - vx
y_viewport = y_global - vy

x_norm = x_viewport / vw
y_norm = y_viewport / vh
```

## Has to be inside the Viewport

```python
class WindowRect(Rect):
    def __init__(self, window: ui.Window):
        width = window.width
        height = window.height
        if width == 0:
            # TODO: here is a work around for window width is 0.
            width = window.frame.computed_width
        if height == 0:
            # TODO: here is a work around for window height is 0.
            height = window.frame.computed_height
        super().__init__(window.position_x, width, window.position_y, height)
```

## Massive issue

```bash
2025-08-18 01:07:48 [29,260ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:48 [29,260ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:48 [29,260ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:48 [29,260ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:48 [29,260ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:48 [29,260ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:48 [29,274ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:48 [29,275ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:48 [29,275ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:48 [29,275ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:48 [29,275ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:48 [29,275ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:48 [29,292ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:48 [29,292ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:48 [29,292ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:48 [29,292ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:48 [29,292ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:48 [29,292ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:48 [29,312ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:48 [29,312ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:48 [29,312ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:48 [29,312ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:48 [29,312ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:48 [29,312ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:48 [29,331ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:48 [29,332ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:48 [29,332ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:48 [29,332ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:48 [29,332ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:48 [29,332ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:48 [29,351ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:48 [29,351ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:48 [29,351ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:48 [29,351ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:48 [29,351ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:48 [29,351ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:49 [29,550ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:49 [29,551ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:49 [29,551ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:49 [29,551ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:49 [29,551ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:49 [29,551ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
2025-08-18 01:07:49 [29,611ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 01:07:49 [29,611ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 01:07:49 [29,611ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 01:07:49 [29,611ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 146, in _on_global_mouse_event
2025-08-18 01:07:49 [29,611ms] [Error] [omni.kit.app._impl] [py stderr]:     viewport_w, viewport_h = self._input.get_viewport_size(self.mouse)
2025-08-18 01:07:49 [29,611ms] [Error] [omni.kit.app._impl] [py stderr]: AttributeError: 'carb.input.IInput' object has no attribute 'get_viewport_size'
```

## Error trying to get depth at coordinates


```bash
get_mouse_coords_pixel : (0.17847222089767456, 0.42777779698371887)
2025-08-18 19:17:20 [38,867ms] [Warning] [isaacsim.sensors.camera.camera] [get_depth][/OmniverseKit_Persp] WARNING: Annotator 'distance_to_image_plane' not found. Available annotators: dict_keys(['rendering_time', 'rendering_frame', 'rgba']). Returning None
2025-08-18 19:17:20 [38,867ms] [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2025-08-18 19:17:20 [38,867ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 141, in _on_input_event
2025-08-18 19:17:20 [38,867ms] [Error] [omni.kit.app._impl] [py stderr]:     return self._on_global_mouse_event(event.event)
2025-08-18 19:17:20 [38,867ms] [Error] [omni.kit.app._impl] [py stderr]:   File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 181, in _on_global_mouse_event
2025-08-18 19:17:20 [38,867ms] [Error] [omni.kit.app._impl] [py stderr]:     depth_value = depth_img[int(y), int(x)]
2025-08-18 19:17:20 [38,867ms] [Error] [omni.kit.app._impl] [py stderr]: TypeError: 'NoneType' object is not subscriptable
```