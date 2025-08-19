# Trying to subscribe to mouse events


Error 

```bash
2025-08-14 23:40:13 [26,115ms] [Error] [asyncio] Task exception was never retrieved
future: <Task finished name='Task-222' coro=<BaseSampleUITemplate._on_load_world.<locals>._on_load_world_async() done, defined at /home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/base_ui_extension.py:108> exception=TypeError('get_mouse_value(): incompatible function arguments. The following argument types are supported:\n    1. (self: carb.input.IInput, arg0: carb.input.Mouse, arg1: carb.input.MouseInput) -> float\n\nInvoked with: <carb.input.IInput object at 0x7792aafa74b0>, <carb.input.Mouse object at 0x7791fc3d69f0>, <MouseEventType.MIDDLE_BUTTON_DOWN: 2>')>
Traceback (most recent call last):
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/base_ui_extension.py", line 111, in _on_load_world_async
    await self._sample.load_world_async()
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/base_ui.py", line 41, in load_world_async
    await self.setup_post_load()
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 89, in setup_post_load
    self.val = self._input.get_mouse_value(self.mouse, carb.input.MouseEventType.MIDDLE_BUTTON_DOWN)
TypeError: get_mouse_value(): incompatible function arguments. The following argument types are supported:
    1. (self: carb.input.IInput, arg0: carb.input.Mouse, arg1: carb.input.MouseInput) -> float

Invoked with: <carb.input.IInput object at 0x7792aafa74b0>, <carb.input.Mouse object at 0x7791fc3d69f0>, <MouseEventType.MIDDLE_BUTTON_DOWN: 2>
```

## Solution

There is an example on how to subscribe to the mouse events and get its coordinates.

Inside the window.py in the ```omni.ki.widget.custom-1.0.9```


Line 148:

```python
def _setup_hooks(self):
  self._input_sub_id = self._input.subscribe_to_input_events(self._on_input_event, order=-10000)
```

Line 152

```python
def _on_input_event(self, event, *_):
  if event.deviceType == carb.input.DeviceType.MOUSE:
      return self._on_global_mouse_event(event.event)
  elif event.deviceType == carb.input.DeviceType.KEYBOARD:
      return self._on_global_keyboard(event.event)
  else:
      return True
```

Line 165:

```python
def _on_global_mouse_event(self, event, *_):
  if not self.visible:
      return True

  # We care only mouse down
  while True:
      if event.type == carb.input.MouseEventType.LEFT_BUTTON_DOWN:
          break
      if event.type == carb.input.MouseEventType.MIDDLE_BUTTON_DOWN:
          break
      if event.type == carb.input.MouseEventType.RIGHT_BUTTON_DOWN:
          break
      # if event.type == carb.input.MouseEventType.MOVE:
      #     break
      return True

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

  # Now the click is outside the popup window rect, hide it.
  if (not self._on_pre_close) or self._on_pre_close():
      self.visible = False
      # Also close children
      for window in self._valid_windows:
          if window is not None:
              window.visible = False
  return True
```

## Example 

From the ```placement_mode.py``` inside the omni.physx.zerogravity extension there is a great example on how to subscribe to mouse events.

Line 100:

```python
self._settings = carb.settings.get_settings()
```

Line 168:

```python
# setup for input handlers for raycast drag manipulation
self._input = carb.input.acquire_input_interface()
self._appwindow = omni.appwindow.get_default_app_window()
```

line 173:

```python
self._mouse = self._appwindow.get_mouse()
```

line 451:

```python
def _on_app_update_event(self, evt):
  """ Event handler app update events occuring every frame"""
  if self._enabled and self._physx_attached_to_stage:
      left_button_down = (
          self._input.get_mouse_button_flags(self._mouse, carb.input.MouseInput.LEFT_BUTTON)
          & carb.input.BUTTON_FLAG_DOWN
      ) == carb.input.BUTTON_FLAG_DOWN
      left_button_down = left_button_down & (
          not self._settings.get_as_bool(pxzerog.SETTINGS_PLACEMENT_MODE_ALLOW_DROP_ON_TRANSFORM_GIZMO_CHANGES)
      )
      if self._physx_zero_gravity:
          self._physx_zero_gravity.notify_gizmo_state(left_button_down)
          self._apply_gizmo_transforms()

          # Undo/redo: determine when can there are no more transform changes
          if self._is_capturing_transform_changes:
              now_s = self._app.get_time_since_start_s()
              elapsed_s = now_s - self._last_transform_change_time_s
              if elapsed_s > 0.5:
                  self._is_capturing_transform_changes = False
                  # execute a command to apply the transform to usd.
                  omni.kit.commands.execute(
                      "PlacementModeTransform",
                      physx_authoring=self._physx_zero_gravity,
                      capture_session_id=self._capture_session_id,
                  )

          self._physx_zero_gravity.placement_simulate()
```

So if the the left button is pressed it returns true

```python
left_button_down = (
                self._input.get_mouse_button_flags(self._mouse, carb.input.MouseInput.LEFT_BUTTON)
                & carb.input.BUTTON_FLAG_DOWN
            ) == carb.input.BUTTON_FLAG_DOWN
```

Can use the carb.input.MouseInput.MIDDLE_BUTTON and it seems that carb.input.BUTTON_FLAG_DOWN is the same 