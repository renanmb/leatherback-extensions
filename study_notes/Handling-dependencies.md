# Handling extra dependencies from Within the Script



Add this inside the extension.toml

```toml
[python.pip_archive]
# This tells Isaac Sim to download and install these via pip on startup
requirements = [
    "onnxruntime"
]
```

Script imports if not it tries to install

```python
import subprocess
import sys

try:
    import onnxruntime as ort
except ImportError:
    print("onnxruntime not found. Installing...")
    # Using sys.executable ensures it installs to the specific Python 
    # environment Isaac Sim is currently using.
    subprocess.check_call([sys.executable, "-m", "pip", "install", "onnxruntime"])
    import onnxruntime as ort
    print("onnxruntime installed successfully.")
```

Outputs following error

```bash
2026-02-23T01:55:04Z [22,355ms] [Error] [omni.ext._impl.custom_importer] Failed to import python module leatherback.example.interactive. Error: No module named 'onnxruntime'. Traceback:
Traceback (most recent call last):
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/controller/policy_controller.py", line 19, in <module>
    import onnxruntime as ort
ModuleNotFoundError: No module named 'onnxruntime'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/goat/isaacsim/kit/kernel/py/omni/ext/_impl/custom_importer.py", line 85, in import_module
    return importlib.import_module(name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/goat/isaacsim/kit/python/lib/python3.11/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/__init__.py", line 1, in <module>
    from .impl import LeatherbackExampleExtension
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/__init__.py", line 1, in <module>
    from .leatherback_example import LeatherbackExample
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive/leatherback/example/interactive/impl/leatherback_example.py", line 7, in <module>
    from leatherback.example.ackermann.leatherback import LeatherbackPolicy
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/leatherback/__init__.py", line 1, in <module>
    from .leatherback import LeatherbackPolicy
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/leatherback/leatherback.py", line 9, in <module>
    from leatherback.example.ackermann.controller import PolicyController
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/controller/__init__.py", line 2, in <module>
    from .policy_controller import *
  File "/home/goat/Documents/GitHub/boredengineer/leatherback.example.ackermann/leatherback/example/ackermann/controller/policy_controller.py", line 25, in <module>
    import onnxruntime as ort
ModuleNotFoundError: No module named 'onnxruntime'

2026-02-23T01:55:04Z [22,355ms] [Error] [carb.scripting-python.plugin] Exception: Extension python module: 'leatherback.example.interactive' in '/home/goat/Documents/GitHub/boredengineer/leatherback.example.interactive' failed to load.

At:
  /home/goat/isaacsim/kit/kernel/py/omni/ext/_impl/_internal.py(222): startup
  /home/goat/isaacsim/kit/kernel/py/omni/ext/_impl/_internal.py(337): startup_extension
  PythonExtension.cpp::startup()(2): <module>
  /home/goat/isaacsim/extscache/omni.kit.window.extensions-1.4.27+69cbf6ad/omni/kit/window/extensions/ext_commands.py(33): do
  /home/goat/isaacsim/extscache/omni.kit.commands-1.4.10+69cbf6ad.lx64.r.cp311/omni/kit/undo/undo.py(81): execute
  /home/goat/isaacsim/extscache/omni.kit.commands-1.4.10+69cbf6ad.lx64.r.cp311/omni/kit/commands/command.py(463): execute
  /home/goat/isaacsim/extscache/omni.kit.window.extensions-1.4.27+69cbf6ad/omni/kit/window/extensions/common.py(556): toggle_extension
  /home/goat/isaacsim/extscache/omni.kit.window.extensions-1.4.27+69cbf6ad/omni/kit/window/extensions/ext_components.py(108): toggle

2026-02-23T01:55:04Z [22,355ms] [Error] [omni.ext.plugin] [ext: leatherback.example.interactive-0.0.1] Failed to startup python extension.
onnxruntime not found. Installing...
Requirement already satisfied: onnxruntime in /home/goat/anaconda3/lib/python3.12/site-packages (1.24.2)
Requirement already satisfied: flatbuffers in /home/goat/anaconda3/lib/python3.12/site-packages (from onnxruntime) (25.12.19)
Requirement already satisfied: numpy>=1.21.6 in /home/goat/anaconda3/lib/python3.12/site-packages (from onnxruntime) (2.2.6)
Requirement already satisfied: packaging in /home/goat/anaconda3/lib/python3.12/site-packages (from onnxruntime) (24.1)
Requirement already satisfied: protobuf in /home/goat/anaconda3/lib/python3.12/site-packages (from onnxruntime) (4.25.3)
Requirement already satisfied: sympy in /home/goat/anaconda3/lib/python3.12/site-packages (from onnxruntime) (1.13.2)
Requirement already satisfied: mpmath<1.4,>=1.1.0 in /home/goat/anaconda3/lib/python3.12/site-packages (from sympy->onnxruntime) (1.3.0)

[notice] A new release of pip is available: 25.3 -> 26.0.1
[notice] To update, run: pip install --upgrade pip

```
