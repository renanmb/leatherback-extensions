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
