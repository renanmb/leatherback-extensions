# Public API for module omni.kit.app:

## Classes

- class IApp
  - def delay_app_ready(self, requester_name: str)
  - def get_app_environment(self) -> str
  - def get_app_filename(self) -> str
  - def get_app_name(self) -> str
  - def get_app_version(self) -> str
  - def get_app_version_short(self) -> str
  - def get_build_version(self) -> str
  - def get_extension_manager(self) -> omni.ext._extensions.ExtensionManager
  - def get_kernel_version(self) -> str
  - def get_kit_version(self) -> str
  - def get_kit_version_hash(self) -> str
  - def get_kit_version_short(self) -> str
  - static def get_log_event_stream(*args, **kwargs) -> typing.Any
  - static def get_message_bus_event_stream(*args, **kwargs) -> typing.Any
  - def get_platform_info(self) -> dict
  - static def get_post_update_event_stream(*args, **kwargs) -> typing.Any
  - static def get_pre_update_event_stream(*args, **kwargs) -> typing.Any
  - static def get_python_scripting(*args, **kwargs) -> typing.Any
  - static def get_shutdown_event_stream(*args, **kwargs) -> typing.Any
  - static def get_startup_event_stream(*args, **kwargs) -> typing.Any
  - def get_time_since_start_ms(self) -> float
  - def get_time_since_start_s(self) -> float
  - static def get_update_event_stream(*args, **kwargs) -> typing.Any
  - def get_update_number(self) -> int
  - def is_app_external(self) -> bool
  - def is_app_ready(self) -> bool
  - def is_debug_build(self) -> bool
  - def is_running(self) -> bool
  - def post_quit(self, return_code: int = 0)
  - def post_uncancellable_quit(self, return_code: int = 0)
  - def print_and_log(self, message: str)
  - def replay_log_messages(self, arg0: carb._carb.logging.Logger)
  - def restart(self, args: typing.List[str] = [], overwrite_args: bool = False, uncancellable: bool = False)
  - def run(self, app_name: str, app_path: str, argv: typing.List[str] = []) -> int
  - def shutdown(self) -> int
  - def startup(self, app_name: str, app_path: str, argv: typing.List[str] = [])
  - def toggle_log_message_recording(self, arg0: bool)
  - def try_cancel_shutdown(self, reason: str = '') -> bool
  - def update(self)

- class IAppScripting
  - def add_search_script_folder(self, path: str) -> bool
  - def execute_file(self, path: str, args: typing.List[str]) -> bool
  - def execute_string(self, str: str, source_file: str = '', execute_as_file: bool = '') -> bool
  - static def get_event_stream(*args, **kwargs) -> typing.Any
  - def remove_search_script_folder(self, path: str) -> bool

- class SettingChangeSubscription
  - def __init__(self, path: str, on_change: Callable)

## Functions

- def acquire_app_interface(plugin_name: str = None, library_path: str = None) -> IApp
- def crash()
- def get_app_interface() -> IApp
- def get_app() -> IApp
- def send_telemetry_event(event_type: str, duration: float = 0, data1: str = '', data2: str = '', value1: float = 0.0, value2: float = 0.0)
- def log_deprecation(message: str)
- def deprecated(message = '')

## Variables

- APP_SCRIPTING_EVENT_COMMAND: int
- APP_SCRIPTING_EVENT_STDOUT: int
- APP_SCRIPTING_EVENT_STDERR: int
- RUN_LOOP_DEFAULT: str
- RUN_LOOP_SIMULATION: str
- RUN_LOOP_RENDERING: str
- RUN_LOOP_UI: str
- POST_QUIT_EVENT_TYPE: int
- PRE_SHUTDOWN_EVENT_TYPE: int
- EVENT_APP_STARTED: int
- EVENT_APP_READY: int
- EVENT_ORDER_DEFAULT: int
- UPDATE_ORDER_PYTHON_ASYNC_FUTURE_BEGIN_UPDATE: Unknown
- UPDATE_ORDER_PYTHON_ASYNC_FUTURE_END_UPDATE: int
- UPDATE_ORDER_PYTHON_EXEC_BEGIN_UPDATE: Unknown
- UPDATE_ORDER_PYTHON_EXEC_END_UPDATE: int
- UPDATE_ORDER_USD: Unknown
- UPDATE_ORDER_UNSPECIFIED: int
- UPDATE_ORDER_FABRIC_FLUSH: int
- UPDATE_ORDER_HYDRA_RENDER: int
- UPDATE_ORDER_UI_RENDER: int
- POST_UPDATE_ORDER_PYTHON_ASYNC_FUTURE: Unknown
- POST_UPDATE_ORDER_PYTHON_EXEC: Unknown

# Public API for module omni.ext:

## Classes

- class ExtensionPathType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - COLLECTION: omni.ext._extensions.ExtensionPathType
  - COLLECTION_CACHE: omni.ext._extensions.ExtensionPathType
  - COLLECTION_USER: omni.ext._extensions.ExtensionPathType
  - DIRECT_PATH: omni.ext._extensions.ExtensionPathType
  - EXT_1_FOLDER: omni.ext._extensions.ExtensionPathType

- class DownloadState
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - DOWNLOADING: omni.ext._extensions.DownloadState
  - DOWNLOAD_FAILURE: omni.ext._extensions.DownloadState
  - DOWNLOAD_SUCCESS: omni.ext._extensions.DownloadState

- class ExtensionManager
  - def add_path(self, path: str, type: ExtensionPathType = ExtensionPathType.COLLECTION)
  - def add_path_protocol_provider(self, scheme: str, on_add_path_fn: typing.Callable[[str], str], on_remove_path_fn: typing.Callable[[str], None]) -> bool
  - static def add_registry_provider(*args, **kwargs) -> typing.Any
  - def fetch_all_extension_packages(self) -> tuple
  - def fetch_extension_packages(self, arg0: str) -> tuple
  - def fetch_extension_summaries(self) -> tuple
  - def fetch_extension_versions(self, arg0: str) -> tuple
  - static def get_change_event_stream(*args, **kwargs) -> typing.Any
  - def get_enabled_extension_id(self, ext_name: str) -> str
  - def get_extension_dict(self, ext_id: str) -> carb.dictionary._dictionary.Item
  - def get_extension_packages(self) -> tuple
  - def get_extension_path(self, ext_id: str) -> str
  - def get_extensions(self) -> tuple
  - def get_folders(self) -> tuple
  - static def get_hooks(*args, **kwargs) -> typing.Any
  - def get_registry_extension_dict(self, ext_id: str) -> carb.dictionary._dictionary.Item
  - def get_registry_extension_packages(self) -> tuple
  - def get_registry_extensions(self) -> tuple
  - def get_registry_providers(self) -> tuple
  - def is_extension_enabled(self, ext_name: str) -> bool
  - def process_and_apply_all_changes(self)
  - def publish_extension(self, ext_id: str, provider_name: str = '', allow_overwrite: bool = False) -> bool
  - def pull_extension(self, ext_id: str) -> bool
  - def pull_extension_async(self, ext_id: str)
  - def refresh_registry(self)
  - def remove_path(self, path: str)
  - def remove_path_protocol_provider(self, scheme: str)
  - def remove_registry_provider(self, name: str)
  - def set_extension_enabled(self, extension_id: str, enabled: bool)
  - def set_extension_enabled_immediate(self, extension_id: str, enabled: bool) -> bool
  - def set_extensions_excluded(self, exts: typing.List[str])
  - def solve_extensions(self, exts: typing.List[str], add_enabled: bool = False, return_only_disabled: bool = False) -> tuple
  - static def subscribe_to_extension_enable(*args, **kwargs) -> typing.Any
  - def sync_registry(self) -> bool
  - def uninstall_extension(self, ext_id: str) -> bool
  - def unpublish_extension(self, ext_id: str, provider_name: str = '') -> bool

- class ExtensionStateChangeType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - AFTER_EXTENSION_DISABLE: omni.ext._extensions.ExtensionStateChangeType
  - AFTER_EXTENSION_ENABLE: omni.ext._extensions.ExtensionStateChangeType
  - BEFORE_EXTENSION_DISABLE: omni.ext._extensions.ExtensionStateChangeType
  - BEFORE_EXTENSION_ENABLE: omni.ext._extensions.ExtensionStateChangeType
  - COUNT: omni.ext._extensions.ExtensionStateChangeType

- class IHookHolder

- class IExtensionManagerHooks
  - def create_extension_state_change_hook(self, fn: typing.Callable[[str, ExtensionStateChangeType], None], type: ExtensionStateChangeType, ext_name: str = '', ext_dict_path: str = '', order: int = 0, hook_name: str = '') -> IHookHolder

- class IExtensions
  - static def create_extension_manager(*args, **kwargs) -> typing.Any

- class ICppExt
  - def shutdown(self)
  - def startup(self, arg0: str)

- class IExt(ICppExt)
  - def __init__(self)

- class IRegistryProvider
  - def __init__(self)

## Functions

- def acquire_extensions_interface(plugin_name: str = None, library_path: str = None) -> IExtensions
- def acquire_ext_interface(plugin_name: str = None, library_path: str = None) -> ICppExt
- def release_ext_interface(arg0: ICppExt)
- def get_extensions_interface() -> IExtensions
- def get_extension_name(ext_id: str) -> str
- def pack_extension(package_id: str, ext_path: str, output_folder: str) -> str
- def unpack_extension(archive_path: str, output_folder: str, ext_id: str = None, archive_subdir: str = None, skip_security_checks = True)
- def get_fast_importer_sys_paths()
- def get_all_sys_paths() -> Iterator[str]
- def create_link(link_path: str, target_path: str, target_is_dir = True)
- def is_link(path: str) -> bool
- def destroy_link(link_folder_path)
- def get_dangling_references(who, frame_depth_to_ignore: int = 0, full_details: bool = False) -> str

## Variables

- EXTENSION_EVENT_SCRIPT_CHANGED: int
- EXTENSION_EVENT_FOLDER_CHANGED: int
- EVENT_REGISTRY_REFRESH_BEGIN: int
- EVENT_REGISTRY_REFRESH_END_SUCCESS: int
- EVENT_REGISTRY_REFRESH_END_FAILURE: int
- EVENT_EXTENSION_PULL_BEGIN: int
- EVENT_EXTENSION_PULL_END_SUCCESS: int
- EVENT_EXTENSION_PULL_END_FAILURE: int
- EXTENSION_SUMMARY_FLAG_NONE: int
- EXTENSION_SUMMARY_FLAG_ANY_ENABLED: int
- EXTENSION_SUMMARY_FLAG_BUILTIN: int
- EXTENSION_SUMMARY_FLAG_INSTALLED: int

# Public API for module carb:

## Classes

- class ColorRgb
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def b(self) -> float
  - [b.setter] def b(self, arg0: float)
  - [property] def g(self) -> float
  - [g.setter] def g(self, arg0: float)
  - [property] def r(self) -> float
  - [r.setter] def r(self, arg0: float)

- class ColorRgbDouble
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def b(self) -> float
  - [b.setter] def b(self, arg0: float)
  - [property] def g(self) -> float
  - [g.setter] def g(self, arg0: float)
  - [property] def r(self) -> float
  - [r.setter] def r(self, arg0: float)

- class ColorRgba
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def a(self) -> float
  - [a.setter] def a(self, arg0: float)
  - [property] def b(self) -> float
  - [b.setter] def b(self, arg0: float)
  - [property] def g(self) -> float
  - [g.setter] def g(self, arg0: float)
  - [property] def r(self) -> float
  - [r.setter] def r(self, arg0: float)

- class ColorRgbaDouble
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def a(self) -> float
  - [a.setter] def a(self, arg0: float)
  - [property] def b(self) -> float
  - [b.setter] def b(self, arg0: float)
  - [property] def g(self) -> float
  - [g.setter] def g(self, arg0: float)
  - [property] def r(self) -> float
  - [r.setter] def r(self, arg0: float)

- class Double2
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)

- class Double3
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)
  - [property] def z(self) -> float
  - [z.setter] def z(self, arg0: float)

- class Double4
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def w(self) -> float
  - [w.setter] def w(self, arg0: float)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)
  - [property] def z(self) -> float
  - [z.setter] def z(self, arg0: float)

- class Float2
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)

- class Float3
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)
  - [property] def z(self) -> float
  - [z.setter] def z(self, arg0: float)

- class Float4
  - def __init__(self)
  - def __init__(self, arg0: float, arg1: float, arg2: float, arg3: float)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def w(self) -> float
  - [w.setter] def w(self, arg0: float)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)
  - [property] def z(self) -> float
  - [z.setter] def z(self, arg0: float)

- class Framework
  - def get_plugins(self) -> typing.List[PluginDesc]
  - def load_plugins(self, loaded_file_wildcards: typing.List[str] = [], search_paths: typing.List[str] = [])
  - def start_plugin(self, plugin: str)
  - def startup(self, argv: typing.List[str] = [], config: str = None, initial_plugins_search_paths: typing.List[str] = [], config_format: str = 'toml')
  - def try_reload_plugins(self)
  - def unload_all_plugins(self)

- class Int2
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)

- class Int3
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int, arg2: int)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)
  - [property] def z(self) -> int
  - [z.setter] def z(self, arg0: int)

- class Int4
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int, arg2: int, arg3: int)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def w(self) -> int
  - [w.setter] def w(self, arg0: int)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)
  - [property] def z(self) -> int
  - [z.setter] def z(self, arg0: int)

- class InterfaceDesc
  - [property] def name(self) -> str
  - [property] def version(self) -> Version

- class PluginDesc
  - [property] def dependencies(self) -> typing.List[InterfaceDesc]
  - [property] def impl(self) -> PluginImplDesc
  - [property] def interfaces(self) -> typing.List[InterfaceDesc]
  - [property] def libPath(self) -> str

- class PluginHotReload
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - DISABLED: carb._carb.PluginHotReload
  - ENABLED: carb._carb.PluginHotReload

- class PluginImplDesc
  - [property] def author(self) -> str
  - [property] def build(self) -> str
  - [property] def description(self) -> str
  - [property] def hotReload(self) -> PluginHotReload
  - [property] def name(self) -> str

- class Subscription
  - def __init__(self, arg0: typing.Callable[[], None])
  - def unsubscribe(self)

- class Uint2
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)

- class Uint3
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int, arg2: int)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)
  - [property] def z(self) -> int
  - [z.setter] def z(self, arg0: int)

- class Uint4
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int, arg2: int, arg3: int)
  - def __init__(self, arg0: typing.Sequence)
  - [property] def w(self) -> int
  - [w.setter] def w(self, arg0: int)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)
  - [property] def z(self) -> int
  - [z.setter] def z(self, arg0: int)

- class Version
  - def __init__(self)
  - def __init__(self, arg0: int, arg1: int)
  - [property] def major(self) -> int
  - [property] def minor(self) -> int

## Functions

- def answer_question(question: str) -> str
- def breakpoint()
- def get_framework(*args, **kwargs) -> typing.Any
- def log(source: str, level: int, fileName: str, functionName: str, lineNumber: int, message: str)
- def wait_for_native_debugger(timeout: float = -1.0, stop: bool = False, quiet: bool = False) -> bool
- def log_error(msg)
- def log_warn(msg)
- def log_info(msg)
- def log_verbose(msg)

## Variables

- filesystem: Unknown
- logging: Unknown

## Other

- sys: builtin module

# Public API for module carb.settings:

## Classes

- class ChangeEventType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - CHANGED: carb.settings._settings.ChangeEventType
  - CREATED: carb.settings._settings.ChangeEventType
  - DESTROYED: carb.settings._settings.ChangeEventType

- class ISettings
  - def create_dictionary_from_settings(self, path: str = '') -> carb.dictionary._dictionary.Item
  - def destroy_item(self, arg0: str)
  - def get(self, path: str) -> object
  - def get_as_bool(self, arg0: str) -> bool
  - def get_as_float(self, arg0: str) -> float
  - def get_as_int(self, arg0: str) -> int
  - def get_as_string(self, arg0: str) -> str
  - def get_settings_dictionary(self, path: str = '') -> carb.dictionary._dictionary.Item
  - def initialize_from_dictionary(self, arg0: carb.dictionary._dictionary.Item)
  - def is_accessible_as(self, arg0: carb.dictionary._dictionary.ItemType, arg1: str) -> bool
  - def set(self, path: str, value: object)
  - def set_bool(self, arg0: str, arg1: bool)
  - def set_bool_array(self, arg0: str, arg1: typing.List[bool])
  - def set_default(self, path: str, value: object)
  - def set_default_bool(self, arg0: str, arg1: bool)
  - def set_default_float(self, arg0: str, arg1: float)
  - def set_default_int(self, arg0: str, arg1: int)
  - def set_default_string(self, arg0: str, arg1: str)
  - def set_float(self, arg0: str, arg1: float)
  - def set_float_array(self, arg0: str, arg1: typing.List[float])
  - def set_int(self, arg0: str, arg1: int)
  - def set_int_array(self, arg0: str, arg1: typing.List[int])
  - def set_string(self, arg0: str, arg1: str)
  - def set_string_array(self, arg0: str, arg1: typing.List[str])
  - def subscribe_to_node_change_events(self, arg0: str, arg1: typing.Callable[[carb.dictionary._dictionary.Item, ChangeEventType], None]) -> SubscriptionId
  - def subscribe_to_tree_change_events(self, arg0: str, arg1: typing.Callable[[carb.dictionary._dictionary.Item, carb.dictionary._dictionary.Item, ChangeEventType], None]) -> SubscriptionId
  - def unsubscribe_to_change_events(self, id: SubscriptionId)
  - def update(self, arg0: str, arg1: carb.dictionary._dictionary.Item, arg2: str, arg3: object)

- class SubscriptionId

## Functions

- def acquire_settings_interface(plugin_name: str = None, library_path: str = None) -> ISettings
- def get_settings_interface() -> ISettings
- def get_settings() -> ISettings

## Other

- lru_cache: unknown


# Public API for module carb.dictionary:

## Classes

- class IDictionary
  - def create_item(self, arg0: object, arg1: str, arg2: ItemType) -> Item
  - def destroy_item(self, arg0: Item)
  - def get(self, base_item: Item, path: str = '') -> object
  - def get_array_length(self, arg0: Item) -> int
  - def get_as_bool(self, arg0: Item) -> bool
  - def get_as_float(self, arg0: Item) -> float
  - def get_as_int(self, arg0: Item) -> int
  - def get_as_string(self, base_item: Item, path: str = '') -> str
  - def get_dict_copy(self, base_item: Item, path: str = '') -> object
  - def get_item(self, base_item: Item, path: str = '') -> Item
  - def get_item_child_by_index(self, arg0: Item, arg1: int) -> Item
  - def get_item_child_by_index_mutable(self, arg0: Item, arg1: int) -> Item
  - def get_item_child_count(self, arg0: Item) -> int
  - def get_item_mutable(self, base_item: Item, path: str = '') -> Item
  - def get_item_name(self, base_item: Item, path: str = '') -> str
  - def get_item_parent(self, arg0: Item) -> Item
  - def get_item_parent_mutable(self, arg0: Item) -> Item
  - def get_item_type(self, arg0: Item) -> ItemType
  - def get_preferred_array_type(self, arg0: Item) -> ItemType
  - def is_accessible_as(self, arg0: ItemType, arg1: Item) -> bool
  - def is_accessible_as_array_of(self, arg0: ItemType, arg1: Item) -> bool
  - def readLock(self, arg0: Item)
  - static def set(*args, **kwargs) -> typing.Any
  - def set_bool(self, arg0: Item, arg1: bool)
  - def set_bool_array(self, arg0: Item, arg1: typing.List[bool])
  - def set_float(self, arg0: Item, arg1: float)
  - def set_float_array(self, arg0: Item, arg1: typing.List[float])
  - def set_int(self, arg0: Item, arg1: int)
  - def set_int_array(self, arg0: Item, arg1: typing.List[int])
  - def set_string(self, arg0: Item, arg1: str)
  - def set_string_array(self, arg0: Item, arg1: typing.List[str])
  - def unlock(self, arg0: Item)
  - def update(self, arg0: Item, arg1: str, arg2: Item, arg3: str, arg4: object)
  - def writeLock(self, arg0: Item)

- class ISerializer
  - def create_dictionary_from_file(self, path: str) -> Item
  - def create_dictionary_from_string_buffer(self, arg0: str) -> Item
  - def create_string_buffer_from_dictionary(self, item: Item, ser_options: int = 0) -> str
  - def save_file_from_dictionary(self, dict: Item, path: str, options: int = 0)

- class Item
  - def clear(self)
  - def get(self, arg0: str, arg1: object) -> object
  - def get_dict(self) -> object
  - def get_key_at(self, arg0: int) -> object
  - def get_keys(self) -> typing.List[str]

- class ItemType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - BOOL: carb.dictionary._dictionary.ItemType
  - COUNT: carb.dictionary._dictionary.ItemType
  - DICTIONARY: carb.dictionary._dictionary.ItemType
  - FLOAT: carb.dictionary._dictionary.ItemType
  - INT: carb.dictionary._dictionary.ItemType
  - STRING: carb.dictionary._dictionary.ItemType

- class UpdateAction
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - KEEP: carb.dictionary._dictionary.UpdateAction
  - OVERWRITE: carb.dictionary._dictionary.UpdateAction

## Functions

- def acquire_dictionary_interface(plugin_name: str = None, library_path: str = None) -> IDictionary
- def acquire_serializer_interface(plugin_name: str = None, library_path: str = None) -> ISerializer
- def get_json_serializer() -> ISerializer
- def get_toml_serializer() -> ISerializer
- def get_dictionary_interface() -> IDictionary
- def get_dictionary() -> IDictionary

## Other

- lru_cache: unknown

# Public API for module carb.tokens:

## Classes

- class ITokens
  - def exists(self, name: str) -> bool
  - def remove_token(self, name: str) -> bool
  - def resolve(self, str: str, flags: int = 0) -> str
  - def set_initial_value(self, name: str, value: str)
  - def set_value(self, name: str, value: str) -> bool

## Functions

- def acquire_tokens_interface(plugin_name: str = None, library_path: str = None) -> ITokens
- def get_tokens_interface() -> ITokens

## Variables

- RESOLVE_FLAG_LEAVE_TOKEN_IF_NOT_FOUND: int
- RESOLVE_FLAG_NONE: int

# Public API for module carb.events:

## Classes

- class AdapterType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - DISPATCH: carb.events._events.AdapterType
  - FULL: carb.events._events.AdapterType
  - PUSH_PUMP: carb.events._events.AdapterType

- class IEvent
  - def consume(self)
  - [property] def payload(self) -> carb.dictionary._dictionary.Item
  - [property] def sender(self) -> int
  - [property] def type(self) -> int

- class IEventStream
  - def create_subscription_to_pop(self, fn: typing.Callable[[IEvent], None], order: int = 0, name: str = None) -> ISubscription
  - def create_subscription_to_pop_by_type(self, event_type: int, fn: typing.Callable[[IEvent], None], order: int = 0, name: str = None) -> ISubscription
  - def create_subscription_to_push(self, fn: typing.Callable[[IEvent], None], order: int = 0, name: str = None) -> ISubscription
  - def create_subscription_to_push_by_type(self, event_type: int, fn: typing.Callable[[IEvent], None], order: int = 0, name: str = None) -> ISubscription
  - def dispatch(self, event_type: int = 0, sender: int = 0, payload: dict = {})
  - def get_subscription_to_pop_order(self, name: str) -> object
  - def get_subscription_to_push_order(self, name: str) -> object
  - def get_subscriptions_to_pop(self) -> tuple
  - def get_subscriptions_to_push(self) -> tuple
  - def pop(self) -> IEvent
  - def pump(self)
  - def push(self, event_type: int = 0, sender: int = 0, payload: dict = {})
  - def set_subscription_to_pop_order(self, name: str, order: int) -> bool
  - def set_subscription_to_push_order(self, name: str, order: int) -> bool
  - def try_pop(self) -> IEvent
  - [property] def event_count(self) -> int
  - [property] def name(self) -> str

- class IEvents
  - def acquire_unique_sender_id(self) -> int
  - def create_event_stream(self, name: str = None) -> IEventStream
  - def release_unique_sender_id(self, arg0: int)

- class IEventsAdapter
  - def create_adapter(self, type: AdapterType, name: str, mappings: typing.Sequence, **kwargs) -> IEventStream

- class ISubscription
  - def unsubscribe(self)
  - [property] def enabled(self) -> bool
  - [enabled.setter] def enabled(self, arg1: bool)
  - [property] def name(self) -> str
  - [property] def order(self) -> int
  - [order.setter] def order(self, arg1: int)

- class MappingEntry
  - def __init__(self, type: int, dispatch_name: str, push_name: str = '')
  - [property] def dispatch_name(self) -> str
  - [dispatch_name.setter] def dispatch_name(self, arg1: str)
  - [property] def push_name(self) -> str
  - [push_name.setter] def push_name(self, arg1: str)
  - [property] def type(self) -> int
  - [type.setter] def type(self, arg0: int)

## Functions

- def acquire_events_adapter_interface(*args, **kwargs) -> typing.Any
- def acquire_events_interface(*args, **kwargs) -> typing.Any
- def type_from_string(arg0: str) -> int
- def get_events_interface() -> IEvents
- def get_events_adapter_interface() -> IEvents

## Other

- asyncio: builtin module
- inspect: builtin module

# Public API for module omni.str:

## Other

- UNKNOWN_MODULE_DEFS: unknown


# Public API for module omni.core:

## Classes

- class Float2
  - def __init__(self)
  - def __init__(self, arg0: typing.Sequence)
  - def __init__(self, x: float, y: float)
  - [property] def h(self) -> float
  - [h.setter] def h(self, arg0: float)
  - [property] def s(self) -> float
  - [s.setter] def s(self, arg0: float)
  - [property] def t(self) -> float
  - [t.setter] def t(self, arg0: float)
  - [property] def u(self) -> float
  - [u.setter] def u(self, arg0: float)
  - [property] def v(self) -> float
  - [v.setter] def v(self, arg0: float)
  - [property] def w(self) -> float
  - [w.setter] def w(self, arg0: float)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)

- class IObject

- class ITypeFactory(_ITypeFactory, IObject)
  - def __init__(self, arg0: IObject)
  - def __init__(self)
  - def get_type_id_name(self, id: int) -> str
  - def register_interface_implementations_from_module(self, module_name: str, flags: int) -> int
  - def set_interface_defaults(self, interface_id: int, impl_id: int, module_name: str, impl_version: int)
  - def unregister_interface_implementations_from_module(self, module_name: str) -> int

- class Int2
  - def __init__(self)
  - def __init__(self, arg0: typing.Sequence)
  - def __init__(self, x: int, y: int)
  - [property] def h(self) -> int
  - [h.setter] def h(self, arg0: int)
  - [property] def s(self) -> int
  - [s.setter] def s(self, arg0: int)
  - [property] def t(self) -> int
  - [t.setter] def t(self, arg0: int)
  - [property] def u(self) -> int
  - [u.setter] def u(self, arg0: int)
  - [property] def v(self) -> int
  - [v.setter] def v(self, arg0: int)
  - [property] def w(self) -> int
  - [w.setter] def w(self, arg0: int)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)

- class Result
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - ACCESS_DENIED: omni.core._core.Result
  - ALREADY_EXISTS: omni.core._core.Result
  - FAIL: omni.core._core.Result
  - INSUFFICIENT_BUFFER: omni.core._core.Result
  - INTERRUPTED: omni.core._core.Result
  - INVALID_ARGUMENT: omni.core._core.Result
  - INVALID_DATA_SIZE: omni.core._core.Result
  - INVALID_DATA_TYPE: omni.core._core.Result
  - INVALID_INDEX: omni.core._core.Result
  - INVALID_OPERATION: omni.core._core.Result
  - INVALID_STATE: omni.core._core.Result
  - NOT_ENOUGH_DATA: omni.core._core.Result
  - NOT_FOUND: omni.core._core.Result
  - NOT_IMPLEMENTED: omni.core._core.Result
  - NOT_SUPPORTED: omni.core._core.Result
  - NO_INTERFACE: omni.core._core.Result
  - NO_MORE_ITEMS: omni.core._core.Result
  - NULL_POINTER: omni.core._core.Result
  - OPERATION_ABORTED: omni.core._core.Result
  - OUT_OF_MEMORY: omni.core._core.Result
  - SUCCESS: omni.core._core.Result
  - TIMED_OUT: omni.core._core.Result
  - TOO_MUCH_DATA: omni.core._core.Result
  - TRY_AGAIN: omni.core._core.Result
  - VERSION_CHECK_FAILURE: omni.core._core.Result
  - VERSION_PARSE_ERROR: omni.core._core.Result
  - WOULD_BLOCK: omni.core._core.Result

- class TypeFactoryLoadFlags
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - NONE: omni.core._core.TypeFactoryLoadFlags

- class UInt2
  - def __init__(self)
  - def __init__(self, arg0: typing.Sequence)
  - def __init__(self, x: int, y: int)
  - [property] def h(self) -> int
  - [h.setter] def h(self, arg0: int)
  - [property] def s(self) -> int
  - [s.setter] def s(self, arg0: int)
  - [property] def t(self) -> int
  - [t.setter] def t(self, arg0: int)
  - [property] def u(self) -> int
  - [u.setter] def u(self, arg0: int)
  - [property] def v(self) -> int
  - [v.setter] def v(self, arg0: int)
  - [property] def w(self) -> int
  - [w.setter] def w(self, arg0: int)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)

## Functions

- def create_type(type_id: str, module_name: str = None, version: int = 0) -> IObject
- def register_module(module_name: str, flags: int = 0) -> int

## Other




# Public API for module carb.audio:

## Classes

- class AudioResult
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - DEVICE_DISCONNECTED: carb.audio._audio.AudioResult
  - DEVICE_LOST: carb.audio._audio.AudioResult
  - DEVICE_NOT_OPEN: carb.audio._audio.AudioResult
  - DEVICE_OPEN: carb.audio._audio.AudioResult
  - INVALID_FORMAT: carb.audio._audio.AudioResult
  - INVALID_PARAMETER: carb.audio._audio.AudioResult
  - IO_ERROR: carb.audio._audio.AudioResult
  - NOT_ALLOWED: carb.audio._audio.AudioResult
  - NOT_FOUND: carb.audio._audio.AudioResult
  - NOT_SUPPORTED: carb.audio._audio.AudioResult
  - OK: carb.audio._audio.AudioResult
  - OUT_OF_MEMORY: carb.audio._audio.AudioResult
  - OUT_OF_RANGE: carb.audio._audio.AudioResult
  - TRY_AGAIN: carb.audio._audio.AudioResult

- class Context
  - def get_caps(self) -> ContextCaps
  - def get_parameters(self, paramsToGet: int) -> ContextParams
  - static def play_sound(*args, **kwargs) -> typing.Any
  - def set_bus_count(self, count: int) -> bool
  - def set_output(self, desc: OutputDesc = None) -> AudioResult
  - def set_parameters(self, paramsToSet: int, params: ContextParams)
  - def update(self) -> AudioResult

- class ContextCaps
  - [property] def max_buses(self) -> int
  - [property] def output(self) -> typing.Any
  - [property] def selected_device(self) -> DeviceCaps

- class ContextError(Exception, BaseException)

- class ContextParams
  - def __init__(self)
  - [property] def default_playback_mode(self) -> int
  - [default_playback_mode.setter] def default_playback_mode(self, arg0: int)
  - [property] def doppler_limit(self) -> float
  - [doppler_limit.setter] def doppler_limit(self, arg0: float)
  - [property] def doppler_scale(self) -> float
  - [doppler_scale.setter] def doppler_scale(self, arg0: float)
  - [property] def flags(self) -> int
  - [flags.setter] def flags(self, arg0: int)
  - [property] def listener(self) -> typing.Any
  - [listener.setter] def listener(*args, **kwargs)
  - [property] def master_volume(self) -> float
  - [master_volume.setter] def master_volume(self, arg0: float)
  - [property] def non_spatial_frequency_ratio(self) -> float
  - [non_spatial_frequency_ratio.setter] def non_spatial_frequency_ratio(self, arg0: float)
  - [property] def non_spatial_volume(self) -> float
  - [non_spatial_volume.setter] def non_spatial_volume(self, arg0: float)
  - [property] def spatial_frequency_ratio(self) -> float
  - [spatial_frequency_ratio.setter] def spatial_frequency_ratio(self, arg0: float)
  - [property] def spatial_volume(self) -> float
  - [spatial_volume.setter] def spatial_volume(self, arg0: float)
  - [property] def speed_of_sound(self) -> float
  - [speed_of_sound.setter] def speed_of_sound(self, arg0: float)
  - [property] def units_per_meter(self) -> float
  - [units_per_meter.setter] def units_per_meter(self, arg0: float)
  - [property] def virtualization_threshold(self) -> float
  - [virtualization_threshold.setter] def virtualization_threshold(self, arg0: float)

- class ContextParams2
  - def __init__(self)

- class DecoderError(Exception, BaseException)

- class DeviceCaps
  - def get_name(self) -> str
  - [property] def channels(self) -> int
  - [channels.setter] def channels(self, arg0: int)
  - [property] def flags(self) -> int
  - [flags.setter] def flags(self, arg0: int)
  - [property] def format(self) -> SampleFormat
  - [format.setter] def format(self, arg0: SampleFormat)
  - [property] def frame_rate(self) -> int
  - [frame_rate.setter] def frame_rate(self, arg0: int)
  - [property] def guid(self) -> Guid
  - [guid.setter] def guid(self, arg0: Guid)
  - [property] def index(self) -> int
  - [index.setter] def index(self, arg0: int)

- class DspValuePair
  - def __init__(self)
  - [property] def inner(self) -> float
  - [inner.setter] def inner(self, arg0: float)
  - [property] def outer(self) -> float
  - [outer.setter] def outer(self, arg0: float)

- class EmitterAttributes
  - def __init__(self)
  - [property] def cone(self) -> EntityCone
  - [cone.setter] def cone(self, arg0: EntityCone)
  - [property] def flags(self) -> int
  - [flags.setter] def flags(self, arg0: int)
  - [property] def forward(self) -> carb._carb.Float3
  - [forward.setter] def forward(self, arg0: carb._carb.Float3)
  - [property] def position(self) -> carb._carb.Float3
  - [position.setter] def position(self, arg0: carb._carb.Float3)
  - [property] def rolloff(self) -> RolloffDesc
  - [rolloff.setter] def rolloff(self, arg0: RolloffDesc)
  - [property] def up(self) -> carb._carb.Float3
  - [up.setter] def up(self, arg0: carb._carb.Float3)
  - [property] def velocity(self) -> carb._carb.Float3
  - [velocity.setter] def velocity(self, arg0: carb._carb.Float3)

- class EncoderError(Exception, BaseException)

- class EntityAttributes
  - def __init__(self)
  - [property] def cone(self) -> EntityCone
  - [cone.setter] def cone(self, arg0: EntityCone)
  - [property] def flags(self) -> int
  - [flags.setter] def flags(self, arg0: int)
  - [property] def forward(self) -> carb._carb.Float3
  - [forward.setter] def forward(self, arg0: carb._carb.Float3)
  - [property] def position(self) -> carb._carb.Float3
  - [position.setter] def position(self, arg0: carb._carb.Float3)
  - [property] def up(self) -> carb._carb.Float3
  - [up.setter] def up(self, arg0: carb._carb.Float3)
  - [property] def velocity(self) -> carb._carb.Float3
  - [velocity.setter] def velocity(self, arg0: carb._carb.Float3)

- class EntityCone
  - def __init__(self)
  - [property] def inside_angle(self) -> float
  - [inside_angle.setter] def inside_angle(self, arg0: float)
  - [property] def low_pass_filter(self) -> DspValuePair
  - [low_pass_filter.setter] def low_pass_filter(self, arg0: DspValuePair)
  - [property] def outside_angle(self) -> float
  - [outside_angle.setter] def outside_angle(self, arg0: float)
  - [property] def reverb(self) -> DspValuePair
  - [reverb.setter] def reverb(self, arg0: DspValuePair)
  - [property] def volume(self) -> DspValuePair
  - [volume.setter] def volume(self, arg0: DspValuePair)

- class EventPoint
  - def __init__(self)
  - [property] def frame(self) -> int
  - [frame.setter] def frame(self, arg0: int)
  - [property] def id(self) -> int
  - [id.setter] def id(self, arg0: int)
  - [property] def length(self) -> int
  - [length.setter] def length(self, arg0: int)
  - [property] def loop_count(self) -> int
  - [loop_count.setter] def loop_count(self, arg0: int)
  - [property] def play_index(self) -> int
  - [play_index.setter] def play_index(self, arg0: int)

- class Float2
  - def __init__(self, arg0: float, arg1: float)
  - def __init__(self, arg0: typing.List[float])
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)

- class Guid
  - def __init__(self)
  - def from_string(self, src: str) -> bool

- class IAudioData
  - def create_empty_sound(self, format: SampleFormat, channels: int, frame_rate: int, buffer_length: int, units: UnitType = UnitType.FRAMES, name: str = None, channel_mask: int = 0) -> SoundData
  - def create_sound_from_blob(self, blob: bytes, decodedFormat: SampleFormat = SampleFormat.DEFAULT, flags: int = 0, streaming: bool = False, autoStream: int = 0) -> SoundData
  - def create_sound_from_file(self, fileName: str, decodedFormat: SampleFormat = SampleFormat.DEFAULT, flags: int = 0, streaming: bool = False, autoStream: int = 0) -> SoundData
  - def create_sound_from_float_pcm(self, pcm: typing.List[float], channels: int, frame_rate: int, channel_mask: int = 0) -> SoundData
  - def create_sound_from_int16_pcm(self, pcm: typing.List[int], channels: int, frame_rate: int, channel_mask: int = 0) -> SoundData
  - def create_sound_from_int32_pcm(self, pcm: typing.List[int], channels: int, frame_rate: int, channel_mask: int = 0) -> SoundData
  - def create_sound_from_uint8_pcm(self, pcm: typing.List[int], channels: int, frame_rate: int, channel_mask: int = 0) -> SoundData

- class IAudioPlayback
  - def create_context(self, desc: PlaybackContextDesc = ...) -> Context
  - def get_device_caps(self, index: int = 0) -> DeviceCaps
  - def get_device_count(self) -> int

- class LoopPointDesc
  - def __init__(self)

- class NotAvailable(Exception, BaseException)

- class OutputDesc
  - def __init__(self)
  - [property] def device_index(self) -> int
  - [device_index.setter] def device_index(self, arg0: int)
  - [property] def flags(self) -> int
  - [flags.setter] def flags(self, arg0: int)
  - [property] def frame_rate(self) -> int
  - [frame_rate.setter] def frame_rate(self, arg0: int)
  - [property] def speaker_mode(self) -> int
  - [speaker_mode.setter] def speaker_mode(self, arg0: int)

- class PeakVolumes
  - [property] def channels(self) -> int
  - [channels.setter] def channels(self, arg0: int)
  - [property] def peak_frame(self) -> int
  - [peak_frame.setter] def peak_frame(self, arg0: int)
  - [property] def peak_volume(self) -> float
  - [peak_volume.setter] def peak_volume(self, arg0: float)

- class PlaybackContextDesc
  - def __init__(self)
  - [property] def flags(self) -> int
  - [flags.setter] def flags(self, arg0: int)
  - [property] def max_buses(self) -> int
  - [max_buses.setter] def max_buses(self, arg0: int)
  - [property] def output(self) -> OutputDesc
  - [output.setter] def output(self, arg0: OutputDesc)
  - [property] def output_display_name(self) -> str
  - [output_display_name.setter] def output_display_name(self, arg0: str)

- class ReadOnly(Exception, BaseException)

- class RolloffDesc
  - def __init__(self)
  - [property] def far_distance(self) -> float
  - [far_distance.setter] def far_distance(self, arg0: float)
  - [property] def near_distance(self) -> float
  - [near_distance.setter] def near_distance(self, arg0: float)
  - [property] def type(self) -> RolloffType
  - [type.setter] def type(self, arg0: RolloffType)

- class RolloffType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - INVERSE: carb.audio._audio.RolloffType
  - LINEAR: carb.audio._audio.RolloffType
  - LINEAR_SQUARE: carb.audio._audio.RolloffType

- class SampleFormat
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - COUNT: carb.audio._audio.SampleFormat
  - DEFAULT: carb.audio._audio.SampleFormat
  - FLAC: carb.audio._audio.SampleFormat
  - MP3: carb.audio._audio.SampleFormat
  - OPUS: carb.audio._audio.SampleFormat
  - PCM16: carb.audio._audio.SampleFormat
  - PCM24: carb.audio._audio.SampleFormat
  - PCM32: carb.audio._audio.SampleFormat
  - PCM8: carb.audio._audio.SampleFormat
  - PCM_COUNT: carb.audio._audio.SampleFormat
  - PCM_FLOAT: carb.audio._audio.SampleFormat
  - RAW: carb.audio._audio.SampleFormat
  - VORBIS: carb.audio._audio.SampleFormat

- class SoundData
  - def clear_event_points(self)
  - def get_buffer_as_float(self, length: int = 0, offset: int = 0, units: UnitType = UnitType.FRAMES) -> typing.List[float]
  - def get_buffer_as_int16(self, length: int = 0, offset: int = 0, units: UnitType = UnitType.FRAMES) -> typing.List[int]
  - def get_buffer_as_int32(self, length: int = 0, offset: int = 0, units: UnitType = UnitType.FRAMES) -> typing.List[int]
  - def get_buffer_as_uint8(self, length: int = 0, offset: int = 0, units: UnitType = UnitType.FRAMES) -> typing.List[int]
  - def get_event_point_by_id(self, id: int) -> EventPoint
  - def get_event_point_by_index(self, index: int) -> EventPoint
  - def get_event_point_by_play_index(self, index: int) -> EventPoint
  - def get_event_point_max_play_index(self) -> int
  - def get_event_points(self) -> typing.List[EventPoint]
  - def get_format(self) -> SoundFormat
  - def get_length(self, units: UnitType = UnitType.FRAMES) -> int
  - def get_max_instances(self) -> int
  - def get_memory_used(self) -> int
  - def get_metadata(self, tag_name: str) -> str
  - def get_metadata_by_index(self, index: int) -> typing.Tuple[str, str]
  - def get_name(self) -> str
  - def get_peak_level(self) -> PeakVolumes
  - def get_valid_length(self, units: UnitType = UnitType.FRAMES) -> int
  - def is_decoded(self) -> bool
  - def save_to_file(self, file_name: str, format: SampleFormat = SampleFormat.DEFAULT, flags: int = 0) -> bool
  - def set_event_points(self, eventPoints: typing.List[EventPoint]) -> bool
  - def set_max_instances(self, limit: int)
  - def set_metadata(self, tag_name: str, tag_value: str) -> bool
  - def set_valid_length(self, length: int, units: UnitType = UnitType.FRAMES)
  - def write_buffer_with_float(self, data: typing.List[float], offset: int = 0, units: UnitType = UnitType.FRAMES)
  - def write_buffer_with_int16(self, data: typing.List[int], offset: int = 0, units: UnitType = UnitType.FRAMES)
  - def write_buffer_with_int32(self, data: typing.List[int], offset: int = 0, units: UnitType = UnitType.FRAMES)
  - def write_buffer_with_uint8(self, data: typing.List[int], offset: int = 0, units: UnitType = UnitType.FRAMES)

- class SoundDataError(Exception, BaseException)

- class SoundFormat
  - def __init__(self)
  - [property] def bits_per_sample(self) -> int
  - [bits_per_sample.setter] def bits_per_sample(self, arg0: int)
  - [property] def block_size(self) -> int
  - [block_size.setter] def block_size(self, arg0: int)
  - [property] def channel_mask(self) -> int
  - [channel_mask.setter] def channel_mask(self, arg0: int)
  - [property] def channels(self) -> int
  - [channels.setter] def channels(self, arg0: int)
  - [property] def format(self) -> SampleFormat
  - [format.setter] def format(self, arg0: SampleFormat)
  - [property] def frame_rate(self) -> int
  - [frame_rate.setter] def frame_rate(self, arg0: int)
  - [property] def frame_size(self) -> int
  - [frame_size.setter] def frame_size(self, arg0: int)
  - [property] def frames_per_block(self) -> int
  - [frames_per_block.setter] def frames_per_block(self, arg0: int)
  - [property] def valid_bits_per_sample(self) -> int
  - [valid_bits_per_sample.setter] def valid_bits_per_sample(self, arg0: int)

- class Speaker
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - BACK_CENTER: carb.audio._audio.Speaker
  - BACK_LEFT: carb.audio._audio.Speaker
  - BACK_RIGHT: carb.audio._audio.Speaker
  - COUNT: carb.audio._audio.Speaker
  - FRONT_CENTER: carb.audio._audio.Speaker
  - FRONT_LEFT: carb.audio._audio.Speaker
  - FRONT_LEFT_WIDE: carb.audio._audio.Speaker
  - FRONT_RIGHT: carb.audio._audio.Speaker
  - FRONT_RIGHT_WIDE: carb.audio._audio.Speaker
  - LOW_FREQUENCY_EFFECT: carb.audio._audio.Speaker
  - SIDE_LEFT: carb.audio._audio.Speaker
  - SIDE_RIGHT: carb.audio._audio.Speaker
  - TOP_BACK_LEFT: carb.audio._audio.Speaker
  - TOP_BACK_RIGHT: carb.audio._audio.Speaker
  - TOP_FRONT_LEFT: carb.audio._audio.Speaker
  - TOP_FRONT_RIGHT: carb.audio._audio.Speaker
  - TOP_LEFT: carb.audio._audio.Speaker
  - TOP_RIGHT: carb.audio._audio.Speaker

- class UnitType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - BYTES: carb.audio._audio.UnitType
  - FRAMES: carb.audio._audio.UnitType
  - MICROSECONDS: carb.audio._audio.UnitType
  - MILLISECONDS: carb.audio._audio.UnitType

- class Voice
  - def get_parameters(self, params_to_get: int = 4294967295) -> VoiceParams
  - def get_play_cursor(self, type: UnitType) -> int
  - def is_playing(self) -> bool
  - def set_balance(self, pan: float, fade: float)
  - def set_doppler_scale(self, scale: float)
  - def set_frequency_ratio(self, ratio: float)
  - def set_loop_point(self, point: LoopPointDesc) -> bool
  - def set_matrix(self, matrix: typing.List[float])
  - def set_mute(self, mute: bool)
  - def set_occlusion(self, direct: float, reverb: float)
  - def set_parameters(self, params_to_set: int, params: VoiceParams)
  - def set_playback_mode(self, playback_mode: int)
  - def set_position(self, position: carb._carb.Float3)
  - def set_priority(self, priority: int)
  - def set_rolloff_curve(self, type: RolloffType, near_distance: float, far_distance: float, volume: typing.List[Float2] = [], low_frequency: typing.List[Float2] = [], low_pass_direct: typing.List[Float2] = [], low_pass_reverb: typing.List[Float2] = [], reverb: typing.List[Float2] = [])
  - def set_spatial_mix_level(self, level: float)
  - def set_velocity(self, velocity: carb._carb.Float3)
  - def set_volume(self, volume: float)
  - def stop(self)

- class VoiceParamBalance
  - def __init__(self)
  - [property] def fade(self) -> float
  - [fade.setter] def fade(self, arg0: float)
  - [property] def pan(self) -> float
  - [pan.setter] def pan(self, arg0: float)

- class VoiceParamOcclusion
  - def __init__(self)
  - [property] def direct(self) -> float
  - [direct.setter] def direct(self, arg0: float)
  - [property] def reverb(self) -> float
  - [reverb.setter] def reverb(self, arg0: float)

- class VoiceParams
  - def __init__(self)
  - [property] def balance(self) -> VoiceParamBalance
  - [balance.setter] def balance(self, arg0: VoiceParamBalance)
  - [property] def doppler_scale(self) -> float
  - [doppler_scale.setter] def doppler_scale(self, arg0: float)
  - [property] def emitter(self) -> EmitterAttributes
  - [emitter.setter] def emitter(self, arg0: EmitterAttributes)
  - [property] def frequency_ratio(self) -> float
  - [frequency_ratio.setter] def frequency_ratio(self, arg0: float)
  - [property] def occlusion(self) -> VoiceParamOcclusion
  - [occlusion.setter] def occlusion(self, arg0: VoiceParamOcclusion)
  - [property] def playback_mode(self) -> int
  - [playback_mode.setter] def playback_mode(self, arg0: int)
  - [property] def priority(self) -> int
  - [priority.setter] def priority(self, arg0: int)
  - [property] def spatial_mix_level(self) -> float
  - [spatial_mix_level.setter] def spatial_mix_level(self, arg0: float)
  - [property] def volume(self) -> float
  - [volume.setter] def volume(self, arg0: float)

## Functions

- def acquire_data_interface(plugin_name: str = None, library_path: str = None) -> IAudioData
- def acquire_playback_interface(plugin_name: str = None, library_path: str = None) -> IAudioPlayback
- def get_force_off_playback_mode_flags(flags: int) -> int
- def get_force_on_playback_mode_flags(flags: int) -> int

## Variables

- AUDIO_IMAGE_FLAG_ALPHA_BLEND: int
- AUDIO_IMAGE_FLAG_MULTI_CHANNEL: int
- AUDIO_IMAGE_FLAG_NOISE_COLOR: int
- AUDIO_IMAGE_FLAG_SPLIT_CHANNELS: int
- AUDIO_IMAGE_FLAG_USE_LINES: int
- CONE_ANGLE_OMNI_DIRECTIONAL: float
- CONTEXT_FLAG_BAKING: int
- CONTEXT_FLAG_MANUAL_STOP: int
- CONTEXT_PARAM_ALL: int
- CONTEXT_PARAM_DEFAULT_PLAYBACK_MODE: int
- CONTEXT_PARAM_DOPPLER_LIMIT: int
- CONTEXT_PARAM_DOPPLER_SCALE: int
- CONTEXT_PARAM_LISTENER: int
- CONTEXT_PARAM_MASTER_VOLUME: int
- CONTEXT_PARAM_NON_SPATIAL_FREQUENCY_RATIO: int
- CONTEXT_PARAM_NON_SPATIAL_VOLUME: int
- CONTEXT_PARAM_SPATIAL_FREQUENCY_RATIO: int
- CONTEXT_PARAM_SPATIAL_VOLUME: int
- CONTEXT_PARAM_SPEED_OF_SOUND: int
- CONTEXT_PARAM_VIDEO_LATENCY: int
- CONTEXT_PARAM_VIRTUALIZATION_THRESHOLD: int
- CONTEXT_PARAM_WORLD_UNIT_SCALE: int
- DATA_FLAG_CALC_PEAKS: int
- DATA_FLAG_SKIP_EVENT_POINTS: int
- DATA_FLAG_SKIP_METADATA: int
- DEFAULT_CHANNEL_COUNT: int
- DEFAULT_FORMAT: int
- DEFAULT_FRAME_RATE: int
- DEFAULT_SPEED_OF_SOUND: float
- DEVICE_FLAG_CONNECTED: int
- DEVICE_FLAG_DEFAULT: int
- DEVICE_FLAG_NOT_OPEN: int
- DEVICE_FLAG_STREAMER: int
- ENTITY_FLAG_ALL: int
- ENTITY_FLAG_CONE: int
- ENTITY_FLAG_FORWARD: int
- ENTITY_FLAG_MAKE_PERP: int
- ENTITY_FLAG_NORMALIZE: int
- ENTITY_FLAG_POSITION: int
- ENTITY_FLAG_ROLLOFF: int
- ENTITY_FLAG_UP: int
- ENTITY_FLAG_VELOCITY: int
- EVENT_POINT_INVALID_FRAME: int
- EVENT_POINT_LOOP_INFINITE: int
- INSTANCES_UNLIMITED: int
- INVALID_DEVICE_INDEX: int
- INVALID_SPEAKER_NAME: int
- MAX_CHANNELS: int
- MAX_FRAMERATE: int
- MAX_NAME_LENGTH: int
- MEMORY_LIMIT_THRESHOLD: int
- META_DATA_TAG_ALBUM: str
- META_DATA_TAG_ARCHIVAL_LOCATION: str
- META_DATA_TAG_ARTIST: str
- META_DATA_TAG_AUDIO_SOURCE_WEBSITE: str
- META_DATA_TAG_BPM: str
- META_DATA_TAG_CLEAR_ALL_TAGS: NoneType
- META_DATA_TAG_COMMENT: str
- META_DATA_TAG_COMMISSIONED: str
- META_DATA_TAG_COMPOSER: str
- META_DATA_TAG_CONTACT: str
- META_DATA_TAG_COPYRIGHT: str
- META_DATA_TAG_CREATION_DATE: str
- META_DATA_TAG_CROPPED: str
- META_DATA_TAG_DESCRIPTION: str
- META_DATA_TAG_DIMENSIONS: str
- META_DATA_TAG_DISC: str
- META_DATA_TAG_DPI: str
- META_DATA_TAG_EDITOR: str
- META_DATA_TAG_ENCODER: str
- META_DATA_TAG_END_TIME: str
- META_DATA_TAG_ENGINEER: str
- META_DATA_TAG_FILE_NAME: str
- META_DATA_TAG_GENRE: str
- META_DATA_TAG_INITIAL_KEY: str
- META_DATA_TAG_INTERNET_ARTIST_WEBSITE: str
- META_DATA_TAG_INTERNET_COMMERCIAL_INFORMATION_URL: str
- META_DATA_TAG_INTERNET_COPYRIGHT_URL: str
- META_DATA_TAG_INTERNET_RADIO_STATION_NAME: str
- META_DATA_TAG_INTERNET_RADIO_STATION_OWNER: str
- META_DATA_TAG_INTERNET_RADIO_STATION_URL: str
- META_DATA_TAG_ISRC: str
- META_DATA_TAG_KEYWORDS: str
- META_DATA_TAG_LANGUAGE: str
- META_DATA_TAG_LICENSE: str
- META_DATA_TAG_LIGHTNESS: str
- META_DATA_TAG_LOCATION: str
- META_DATA_TAG_MEDIUM: str
- META_DATA_TAG_ORGANIZATION: str
- META_DATA_TAG_ORIGINAL_YEAR: str
- META_DATA_TAG_OWNER: str
- META_DATA_TAG_PALETTE_SETTING: str
- META_DATA_TAG_PAYMENT_URL: str
- META_DATA_TAG_PERFORMER: str
- META_DATA_TAG_PLAYLIST_DELAY: str
- META_DATA_TAG_PUBLISHER: str
- META_DATA_TAG_RECORDING_DATE: str
- META_DATA_TAG_SHARPNESS: str
- META_DATA_TAG_SOURCE_FORM: str
- META_DATA_TAG_SPEED: str
- META_DATA_TAG_START_TIME: str
- META_DATA_TAG_SUBGENRE: str
- META_DATA_TAG_SUBJECT: str
- META_DATA_TAG_TECHNICIAN: str
- META_DATA_TAG_TERMS_OF_USE: str
- META_DATA_TAG_TITLE: str
- META_DATA_TAG_TRACK_NUMBER: str
- META_DATA_TAG_VERSION: str
- META_DATA_TAG_WEBSITE: str
- META_DATA_TAG_WRITER: str
- MIN_CHANNELS: int
- MIN_FRAMERATE: int
- OUTPUT_FLAG_DEVICE: int
- PLAYBACK_MODE_DEFAULT_DISTANCE_DELAY: int
- PLAYBACK_MODE_DEFAULT_INTERAURAL_DELAY: int
- PLAYBACK_MODE_DEFAULT_USE_DOPPLER: int
- PLAYBACK_MODE_DEFAULT_USE_FILTERS: int
- PLAYBACK_MODE_DEFAULT_USE_REVERB: int
- PLAYBACK_MODE_DISTANCE_DELAY: int
- PLAYBACK_MODE_FADE_IN: int
- PLAYBACK_MODE_INTERAURAL_DELAY: int
- PLAYBACK_MODE_LISTENER_RELATIVE: int
- PLAYBACK_MODE_MUTED: int
- PLAYBACK_MODE_NO_POSITION_SIMULATION: int
- PLAYBACK_MODE_NO_SPATIAL_LOW_FREQUENCY_EFFECT: int
- PLAYBACK_MODE_PAUSED: int
- PLAYBACK_MODE_SIMULATE_POSITION: int
- PLAYBACK_MODE_SPATIAL: int
- PLAYBACK_MODE_SPATIAL_MIX_LEVEL_MATRIX: int
- PLAYBACK_MODE_STOP_ON_SIMULATION: int
- PLAYBACK_MODE_USE_DOPPLER: int
- PLAYBACK_MODE_USE_FILTERS: int
- PLAYBACK_MODE_USE_REVERB: int
- SAVE_FLAG_DEFAULT: int
- SAVE_FLAG_STRIP_EVENT_POINTS: int
- SAVE_FLAG_STRIP_METADATA: int
- SAVE_FLAG_STRIP_PEAKS: int
- SPEAKER_FLAG_BACK_CENTER: int
- SPEAKER_FLAG_BACK_LEFT: int
- SPEAKER_FLAG_BACK_RIGHT: int
- SPEAKER_FLAG_FRONT_CENTER: int
- SPEAKER_FLAG_FRONT_LEFT: int
- SPEAKER_FLAG_FRONT_LEFT_WIDE: int
- SPEAKER_FLAG_FRONT_RIGHT: int
- SPEAKER_FLAG_FRONT_RIGHT_WIDE: int
- SPEAKER_FLAG_LOW_FREQUENCY_EFFECT: int
- SPEAKER_FLAG_SIDE_LEFT: int
- SPEAKER_FLAG_SIDE_RIGHT: int
- SPEAKER_FLAG_TOP_BACK_LEFT: int
- SPEAKER_FLAG_TOP_BACK_RIGHT: int
- SPEAKER_FLAG_TOP_FRONT_LEFT: int
- SPEAKER_FLAG_TOP_FRONT_RIGHT: int
- SPEAKER_FLAG_TOP_LEFT: int
- SPEAKER_FLAG_TOP_RIGHT: int
- SPEAKER_MODE_COUNT: int
- SPEAKER_MODE_DEFAULT: int
- SPEAKER_MODE_FIVE_POINT_ONE: int
- SPEAKER_MODE_FIVE_POINT_ZERO: int
- SPEAKER_MODE_FOUR_POINT_ONE: int
- SPEAKER_MODE_MONO: int
- SPEAKER_MODE_NINE_POINT_ONE: int
- SPEAKER_MODE_NINE_POINT_ONE_POINT_FOUR: int
- SPEAKER_MODE_NINE_POINT_ONE_POINT_SIX: int
- SPEAKER_MODE_QUAD: int
- SPEAKER_MODE_SEVEN_POINT_ONE: int
- SPEAKER_MODE_SEVEN_POINT_ONE_POINT_FOUR: int
- SPEAKER_MODE_SIX_POINT_ONE: int
- SPEAKER_MODE_STEREO: int
- SPEAKER_MODE_THREE_POINT_ZERO: int
- SPEAKER_MODE_TWO_POINT_ONE: int
- SPEAKER_MODE_VALID_BITS: int
- VOICE_PARAM_ALL: int
- VOICE_PARAM_BALANCE: int
- VOICE_PARAM_DOPPLER_SCALE: int
- VOICE_PARAM_EMITTER: int
- VOICE_PARAM_FREQUENCY_RATIO: int
- VOICE_PARAM_MATRIX: int
- VOICE_PARAM_MUTE: int
- VOICE_PARAM_OCCLUSION_FACTOR: int
- VOICE_PARAM_PAUSE: int
- VOICE_PARAM_PLAYBACK_MODE: int
- VOICE_PARAM_PRIORITY: int
- VOICE_PARAM_SPATIAL_MIX_LEVEL: int
- VOICE_PARAM_VOLUME: int

# Public API for module carb.dictionary:

## Classes

- class IDictionary
  - def create_item(self, arg0: object, arg1: str, arg2: ItemType) -> Item
  - def destroy_item(self, arg0: Item)
  - def get(self, base_item: Item, path: str = '') -> object
  - def get_array_length(self, arg0: Item) -> int
  - def get_as_bool(self, arg0: Item) -> bool
  - def get_as_float(self, arg0: Item) -> float
  - def get_as_int(self, arg0: Item) -> int
  - def get_as_string(self, base_item: Item, path: str = '') -> str
  - def get_dict_copy(self, base_item: Item, path: str = '') -> object
  - def get_item(self, base_item: Item, path: str = '') -> Item
  - def get_item_child_by_index(self, arg0: Item, arg1: int) -> Item
  - def get_item_child_by_index_mutable(self, arg0: Item, arg1: int) -> Item
  - def get_item_child_count(self, arg0: Item) -> int
  - def get_item_mutable(self, base_item: Item, path: str = '') -> Item
  - def get_item_name(self, base_item: Item, path: str = '') -> str
  - def get_item_parent(self, arg0: Item) -> Item
  - def get_item_parent_mutable(self, arg0: Item) -> Item
  - def get_item_type(self, arg0: Item) -> ItemType
  - def get_preferred_array_type(self, arg0: Item) -> ItemType
  - def is_accessible_as(self, arg0: ItemType, arg1: Item) -> bool
  - def is_accessible_as_array_of(self, arg0: ItemType, arg1: Item) -> bool
  - def readLock(self, arg0: Item)
  - static def set(*args, **kwargs) -> typing.Any
  - def set_bool(self, arg0: Item, arg1: bool)
  - def set_bool_array(self, arg0: Item, arg1: typing.List[bool])
  - def set_float(self, arg0: Item, arg1: float)
  - def set_float_array(self, arg0: Item, arg1: typing.List[float])
  - def set_int(self, arg0: Item, arg1: int)
  - def set_int_array(self, arg0: Item, arg1: typing.List[int])
  - def set_string(self, arg0: Item, arg1: str)
  - def set_string_array(self, arg0: Item, arg1: typing.List[str])
  - def unlock(self, arg0: Item)
  - def update(self, arg0: Item, arg1: str, arg2: Item, arg3: str, arg4: object)
  - def writeLock(self, arg0: Item)

- class ISerializer
  - def create_dictionary_from_file(self, path: str) -> Item
  - def create_dictionary_from_string_buffer(self, arg0: str) -> Item
  - def create_string_buffer_from_dictionary(self, item: Item, ser_options: int = 0) -> str
  - def save_file_from_dictionary(self, dict: Item, path: str, options: int = 0)

- class Item
  - def clear(self)
  - def get(self, arg0: str, arg1: object) -> object
  - def get_dict(self) -> object
  - def get_key_at(self, arg0: int) -> object
  - def get_keys(self) -> typing.List[str]

- class ItemType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - BOOL: carb.dictionary._dictionary.ItemType
  - COUNT: carb.dictionary._dictionary.ItemType
  - DICTIONARY: carb.dictionary._dictionary.ItemType
  - FLOAT: carb.dictionary._dictionary.ItemType
  - INT: carb.dictionary._dictionary.ItemType
  - STRING: carb.dictionary._dictionary.ItemType

- class UpdateAction
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - KEEP: carb.dictionary._dictionary.UpdateAction
  - OVERWRITE: carb.dictionary._dictionary.UpdateAction

## Functions

- def acquire_dictionary_interface(plugin_name: str = None, library_path: str = None) -> IDictionary
- def acquire_serializer_interface(plugin_name: str = None, library_path: str = None) -> ISerializer
- def get_json_serializer() -> ISerializer
- def get_toml_serializer() -> ISerializer
- def get_dictionary_interface() -> IDictionary
- def get_dictionary() -> IDictionary

## Other

- lru_cache: unknown

# Public API for module carb.input:

## Classes

- class ActionEvent
  - [property] def action(self) -> str
  - [property] def flags(self) -> int
  - [property] def value(self) -> float

- class ActionMappingDesc
  - [property] def device(self) -> object
  - [property] def deviceType(self) -> DeviceType
  - [property] def input(self) -> object
  - [property] def modifiers(self) -> int

- class ActionMappingSet

- class DeviceType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - GAMEPAD: carb.input.DeviceType
  - KEYBOARD: carb.input.DeviceType
  - MOUSE: carb.input.DeviceType

- class EventType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - UNKNOWN: carb.input.EventType

- class FilterResult
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - CONSUME: carb.input.FilterResult
  - RETAIN: carb.input.FilterResult

- class Gamepad(InputDevice)

- class GamepadConnectionEvent
  - [property] def device(self) -> InputDevice
  - [property] def gamepad(self) -> Gamepad
  - [property] def type(self) -> GamepadConnectionEventType

- class GamepadConnectionEventType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - CONNECTED: carb.input.GamepadConnectionEventType
  - CREATED: carb.input.GamepadConnectionEventType
  - DESTROYED: carb.input.GamepadConnectionEventType
  - DISCONNECTED: carb.input.GamepadConnectionEventType

- class GamepadEvent
  - [property] def device(self) -> InputDevice
  - [property] def gamepad(self) -> Gamepad
  - [property] def input(self) -> GamepadInput
  - [property] def value(self) -> float

- class GamepadInput
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - A: carb.input.GamepadInput
  - B: carb.input.GamepadInput
  - COUNT: carb.input.GamepadInput
  - DPAD_DOWN: carb.input.GamepadInput
  - DPAD_LEFT: carb.input.GamepadInput
  - DPAD_RIGHT: carb.input.GamepadInput
  - DPAD_UP: carb.input.GamepadInput
  - LEFT_SHOULDER: carb.input.GamepadInput
  - LEFT_STICK: carb.input.GamepadInput
  - LEFT_STICK_DOWN: carb.input.GamepadInput
  - LEFT_STICK_LEFT: carb.input.GamepadInput
  - LEFT_STICK_RIGHT: carb.input.GamepadInput
  - LEFT_STICK_UP: carb.input.GamepadInput
  - LEFT_TRIGGER: carb.input.GamepadInput
  - MENU1: carb.input.GamepadInput
  - MENU2: carb.input.GamepadInput
  - RIGHT_SHOULDER: carb.input.GamepadInput
  - RIGHT_STICK: carb.input.GamepadInput
  - RIGHT_STICK_DOWN: carb.input.GamepadInput
  - RIGHT_STICK_LEFT: carb.input.GamepadInput
  - RIGHT_STICK_RIGHT: carb.input.GamepadInput
  - RIGHT_STICK_UP: carb.input.GamepadInput
  - RIGHT_TRIGGER: carb.input.GamepadInput
  - X: carb.input.GamepadInput
  - Y: carb.input.GamepadInput

- class IInput
  - def add_action_mapping(self, action_mapping_set: ActionMappingSet, action: str, keyboard: Keyboard, keyboard_input: KeyboardInput, modifiers: int = 0) -> int
  - def add_action_mapping(self, action_mapping_set: ActionMappingSet, action: str, mouse: Mouse, mouse_input: MouseInput, modifiers: int = 0) -> int
  - def add_action_mapping(self, action_mapping_set: ActionMappingSet, action: str, gamepad: Gamepad, gamepad_input: GamepadInput) -> int
  - def clear_action_mappings(self, arg0: ActionMappingSet, arg1: str)
  - def create_action_mapping_set(self, arg0: str) -> ActionMappingSet
  - def destroy_action_mapping_set(self, arg0: ActionMappingSet)
  - def distribute_buffered_events(self)
  - def filter_buffered_events(self, arg0: typing.Callable[[InputEvent], FilterResult])
  - def get_action_button_flags(self, arg0: ActionMappingSet, arg1: str) -> int
  - def get_action_count(self, arg0: ActionMappingSet) -> int
  - def get_action_mapping_count(self, arg0: ActionMappingSet, arg1: str) -> int
  - def get_action_mapping_set_by_path(self, arg0: str) -> ActionMappingSet
  - def get_action_mappings(self, arg0: ActionMappingSet, arg1: str) -> typing.List[ActionMappingDesc]
  - def get_action_value(self, arg0: ActionMappingSet, arg1: str) -> float
  - def get_actions(self, arg0: ActionMappingSet) -> typing.List[str]
  - def get_device_name(self, arg0: InputDevice) -> str
  - def get_device_type(self, arg0: InputDevice) -> DeviceType
  - def get_gamepad_button_flags(self, arg0: Gamepad, arg1: GamepadInput) -> int
  - def get_gamepad_guid(self, arg0: Gamepad) -> str
  - def get_gamepad_name(self, arg0: Gamepad) -> str
  - def get_gamepad_value(self, arg0: Gamepad, arg1: GamepadInput) -> float
  - def get_global_modifier_flags(self, modifiers: int = 0, mouse_buttons: object = None) -> int
  - static def get_input_provider(*args, **kwargs) -> typing.Any
  - def get_keyboard_button_flags(self, arg0: Keyboard, arg1: KeyboardInput) -> int
  - def get_keyboard_name(self, arg0: Keyboard) -> str
  - def get_keyboard_value(self, arg0: Keyboard, arg1: KeyboardInput) -> float
  - def get_modifier_flags(self, modifiers: int = 0, input_devices: typing.List[InputDevice] = [], device_types: typing.List[DeviceType] = [], mouse_buttons: object = None) -> int
  - def get_mouse_button_flags(self, arg0: Mouse, arg1: MouseInput) -> int
  - def get_mouse_coords_normalized(self, arg0: Mouse) -> carb._carb.Float2
  - def get_mouse_coords_pixel(self, arg0: Mouse) -> carb._carb.Float2
  - def get_mouse_name(self, arg0: Mouse) -> str
  - def get_mouse_value(self, arg0: Mouse, arg1: MouseInput) -> float
  - def remove_action_mapping(self, arg0: ActionMappingSet, arg1: str, arg2: int)
  - def set_action_mapping(self, action_mapping_set: ActionMappingSet, action: str, index: int, keyboard: Keyboard, keyboard_input: KeyboardInput, modifiers: int = 0)
  - def set_action_mapping(self, action_mapping_set: ActionMappingSet, action: str, index: int, mouse: Mouse, mouse_input: MouseInput, modifiers: int = 0)
  - def set_action_mapping(self, action_mapping_set: ActionMappingSet, action: str, index: int, gamepad: Gamepad, gamepad_input: GamepadInput)
  - def set_default_action_mapping(self, arg0: ActionMappingSet, arg1: str, arg2: Keyboard, arg3: KeyboardInput, arg4: int) -> bool
  - def set_default_action_mapping(self, arg0: ActionMappingSet, arg1: str, arg2: Gamepad, arg3: GamepadInput) -> bool
  - def set_default_action_mapping(self, arg0: ActionMappingSet, arg1: str, arg2: Mouse, arg3: MouseInput, arg4: int) -> bool
  - def shutdown(self)
  - def startup(self)
  - def subscribe_to_action_events(self, arg0: ActionMappingSet, arg1: str, arg2: typing.Callable[[ActionEvent], bool]) -> int
  - def subscribe_to_gamepad_connection_events(self, arg0: typing.Callable[[GamepadConnectionEvent], None]) -> int
  - def subscribe_to_gamepad_events(self, arg0: Gamepad, arg1: typing.Callable[[GamepadEvent], bool]) -> int
  - def subscribe_to_input_events(self, eventFn: typing.Callable[[InputEvent], bool], eventTypes: int = 4294967295, device: InputDevice = None, order: int = -1) -> int
  - def subscribe_to_keyboard_events(self, arg0: Keyboard, arg1: typing.Callable[[KeyboardEvent], bool]) -> int
  - def subscribe_to_mouse_events(self, arg0: Mouse, arg1: typing.Callable[[MouseEvent], bool]) -> int
  - def unsubscribe_to_action_events(self, arg0: int)
  - def unsubscribe_to_gamepad_connection_events(self, arg0: int)
  - def unsubscribe_to_gamepad_events(self, arg0: Gamepad, arg1: int)
  - def unsubscribe_to_input_events(self, arg0: int)
  - def unsubscribe_to_keyboard_events(self, arg0: Keyboard, arg1: int)
  - def unsubscribe_to_mouse_events(self, arg0: Mouse, arg1: int)

- class InputDevice

- class InputEvent
  - [property] def device(self) -> InputDevice
  - [property] def deviceType(self) -> DeviceType
  - [property] def event(self) -> object

- class InputProvider
  - def buffer_gamepad_event(self, arg0: Gamepad, arg1: GamepadInput, arg2: float)
  - def buffer_keyboard_char_event(self, arg0: Keyboard, arg1: str, arg2: int)
  - def buffer_keyboard_key_event(self, arg0: Keyboard, arg1: KeyboardEventType, arg2: KeyboardInput, arg3: int)
  - def buffer_mouse_event(self, arg0: Mouse, arg1: MouseEventType, arg2: carb._carb.Float2, arg3: int, arg4: carb._carb.Float2)
  - def create_gamepad(self, arg0: str, arg1: str) -> Gamepad
  - def create_keyboard(self, arg0: str) -> Keyboard
  - def create_mouse(self, arg0: str) -> Mouse
  - def destroy_gamepad(self, arg0: Gamepad)
  - def destroy_keyboard(self, arg0: Keyboard)
  - def destroy_mouse(self, arg0: Mouse)
  - def set_gamepad_connected(self, arg0: Gamepad, arg1: bool)
  - def update_gamepad(self, arg0: Gamepad)
  - def update_keyboard(self, arg0: Keyboard)
  - def update_mouse(self, arg0: Mouse)

- class Keyboard(InputDevice)

- class KeyboardEvent
  - [property] def device(self) -> InputDevice
  - [property] def input(self) -> object
  - [property] def keyboard(self) -> Keyboard
  - [property] def modifiers(self) -> int
  - [property] def type(self) -> KeyboardEventType

- class KeyboardEventType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - CHAR: carb.input.KeyboardEventType
  - KEY_PRESS: carb.input.KeyboardEventType
  - KEY_RELEASE: carb.input.KeyboardEventType
  - KEY_REPEAT: carb.input.KeyboardEventType

- class KeyboardInput
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - A: carb.input.KeyboardInput
  - APOSTROPHE: carb.input.KeyboardInput
  - B: carb.input.KeyboardInput
  - BACKSLASH: carb.input.KeyboardInput
  - BACKSPACE: carb.input.KeyboardInput
  - C: carb.input.KeyboardInput
  - CAPS_LOCK: carb.input.KeyboardInput
  - COMMA: carb.input.KeyboardInput
  - COUNT: carb.input.KeyboardInput
  - D: carb.input.KeyboardInput
  - DEL: carb.input.KeyboardInput
  - DOWN: carb.input.KeyboardInput
  - E: carb.input.KeyboardInput
  - END: carb.input.KeyboardInput
  - ENTER: carb.input.KeyboardInput
  - EQUAL: carb.input.KeyboardInput
  - ESCAPE: carb.input.KeyboardInput
  - F: carb.input.KeyboardInput
  - F1: carb.input.KeyboardInput
  - F10: carb.input.KeyboardInput
  - F11: carb.input.KeyboardInput
  - F12: carb.input.KeyboardInput
  - F2: carb.input.KeyboardInput
  - F3: carb.input.KeyboardInput
  - F4: carb.input.KeyboardInput
  - F5: carb.input.KeyboardInput
  - F6: carb.input.KeyboardInput
  - F7: carb.input.KeyboardInput
  - F8: carb.input.KeyboardInput
  - F9: carb.input.KeyboardInput
  - G: carb.input.KeyboardInput
  - GRAVE_ACCENT: carb.input.KeyboardInput
  - H: carb.input.KeyboardInput
  - HOME: carb.input.KeyboardInput
  - I: carb.input.KeyboardInput
  - INSERT: carb.input.KeyboardInput
  - J: carb.input.KeyboardInput
  - K: carb.input.KeyboardInput
  - KEY_0: carb.input.KeyboardInput
  - KEY_1: carb.input.KeyboardInput
  - KEY_2: carb.input.KeyboardInput
  - KEY_3: carb.input.KeyboardInput
  - KEY_4: carb.input.KeyboardInput
  - KEY_5: carb.input.KeyboardInput
  - KEY_6: carb.input.KeyboardInput
  - KEY_7: carb.input.KeyboardInput
  - KEY_8: carb.input.KeyboardInput
  - KEY_9: carb.input.KeyboardInput
  - L: carb.input.KeyboardInput
  - LEFT: carb.input.KeyboardInput
  - LEFT_ALT: carb.input.KeyboardInput
  - LEFT_BRACKET: carb.input.KeyboardInput
  - LEFT_CONTROL: carb.input.KeyboardInput
  - LEFT_SHIFT: carb.input.KeyboardInput
  - LEFT_SUPER: carb.input.KeyboardInput
  - M: carb.input.KeyboardInput
  - MENU: carb.input.KeyboardInput
  - MINUS: carb.input.KeyboardInput
  - N: carb.input.KeyboardInput
  - NUMPAD_0: carb.input.KeyboardInput
  - NUMPAD_1: carb.input.KeyboardInput
  - NUMPAD_2: carb.input.KeyboardInput
  - NUMPAD_3: carb.input.KeyboardInput
  - NUMPAD_4: carb.input.KeyboardInput
  - NUMPAD_5: carb.input.KeyboardInput
  - NUMPAD_6: carb.input.KeyboardInput
  - NUMPAD_7: carb.input.KeyboardInput
  - NUMPAD_8: carb.input.KeyboardInput
  - NUMPAD_9: carb.input.KeyboardInput
  - NUMPAD_ADD: carb.input.KeyboardInput
  - NUMPAD_DEL: carb.input.KeyboardInput
  - NUMPAD_DIVIDE: carb.input.KeyboardInput
  - NUMPAD_ENTER: carb.input.KeyboardInput
  - NUMPAD_EQUAL: carb.input.KeyboardInput
  - NUMPAD_MULTIPLY: carb.input.KeyboardInput
  - NUMPAD_SUBTRACT: carb.input.KeyboardInput
  - NUM_LOCK: carb.input.KeyboardInput
  - O: carb.input.KeyboardInput
  - P: carb.input.KeyboardInput
  - PAGE_DOWN: carb.input.KeyboardInput
  - PAGE_UP: carb.input.KeyboardInput
  - PAUSE: carb.input.KeyboardInput
  - PERIOD: carb.input.KeyboardInput
  - PRINT_SCREEN: carb.input.KeyboardInput
  - Q: carb.input.KeyboardInput
  - R: carb.input.KeyboardInput
  - RIGHT: carb.input.KeyboardInput
  - RIGHT_ALT: carb.input.KeyboardInput
  - RIGHT_BRACKET: carb.input.KeyboardInput
  - RIGHT_CONTROL: carb.input.KeyboardInput
  - RIGHT_SHIFT: carb.input.KeyboardInput
  - RIGHT_SUPER: carb.input.KeyboardInput
  - S: carb.input.KeyboardInput
  - SCROLL_LOCK: carb.input.KeyboardInput
  - SEMICOLON: carb.input.KeyboardInput
  - SLASH: carb.input.KeyboardInput
  - SPACE: carb.input.KeyboardInput
  - T: carb.input.KeyboardInput
  - TAB: carb.input.KeyboardInput
  - U: carb.input.KeyboardInput
  - UNKNOWN: carb.input.KeyboardInput
  - UP: carb.input.KeyboardInput
  - V: carb.input.KeyboardInput
  - W: carb.input.KeyboardInput
  - X: carb.input.KeyboardInput
  - Y: carb.input.KeyboardInput
  - Z: carb.input.KeyboardInput

- class Mouse(InputDevice)

- class MouseEvent
  - [property] def device(self) -> InputDevice
  - [property] def modifiers(self) -> int
  - [property] def mouse(self) -> Mouse
  - [property] def normalized_coords(self) -> carb._carb.Float2
  - [property] def pixel_coords(self) -> carb._carb.Float2
  - [property] def scrollDelta(self) -> carb._carb.Float2
  - [property] def type(self) -> MouseEventType

- class MouseEventType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - LEFT_BUTTON_DOWN: carb.input.MouseEventType
  - LEFT_BUTTON_UP: carb.input.MouseEventType
  - MIDDLE_BUTTON_DOWN: carb.input.MouseEventType
  - MIDDLE_BUTTON_UP: carb.input.MouseEventType
  - MOVE: carb.input.MouseEventType
  - RIGHT_BUTTON_DOWN: carb.input.MouseEventType
  - RIGHT_BUTTON_UP: carb.input.MouseEventType
  - SCROLL: carb.input.MouseEventType

- class MouseInput
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - BACK_BUTTON: carb.input.MouseInput
  - COUNT: carb.input.MouseInput
  - FORWARD_BUTTON: carb.input.MouseInput
  - LEFT_BUTTON: carb.input.MouseInput
  - MIDDLE_BUTTON: carb.input.MouseInput
  - MOVE_DOWN: carb.input.MouseInput
  - MOVE_LEFT: carb.input.MouseInput
  - MOVE_RIGHT: carb.input.MouseInput
  - MOVE_UP: carb.input.MouseInput
  - RIGHT_BUTTON: carb.input.MouseInput
  - SCROLL_DOWN: carb.input.MouseInput
  - SCROLL_LEFT: carb.input.MouseInput
  - SCROLL_RIGHT: carb.input.MouseInput
  - SCROLL_UP: carb.input.MouseInput

## Functions

- def acquire_input_interface(plugin_name: str = None, library_path: str = None) -> IInput
- def acquire_input_provider(*args, **kwargs) -> typing.Any
- def get_action_mapping_desc_from_string(arg0: str) -> ActionMappingDesc
- def get_string_from_action_mapping_desc(arg0: GamepadInput) -> str

## Variables

- BUTTON_FLAG_DOWN: int
- BUTTON_FLAG_PRESSED: int
- BUTTON_FLAG_RELEASED: int
- BUTTON_FLAG_UP: int
- EVENT_TYPE_ALL: int
- KEYBOARD_MODIFIER_FLAG_ALT: int
- KEYBOARD_MODIFIER_FLAG_CAPS_LOCK: int
- KEYBOARD_MODIFIER_FLAG_CONTROL: int
- KEYBOARD_MODIFIER_FLAG_NUM_LOCK: int
- KEYBOARD_MODIFIER_FLAG_SHIFT: int
- KEYBOARD_MODIFIER_FLAG_SUPER: int
- SUBSCRIPTION_ORDER_DEFAULT: Unknown
- SUBSCRIPTION_ORDER_FIRST: int
- SUBSCRIPTION_ORDER_LAST: Unknown

# Public API for module carb.profiler:

## Classes

- class FlowType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - BEGIN: carb.profiler._profiler.FlowType
  - END: carb.profiler._profiler.FlowType

- class IProfileMonitor
  - def get_last_profile_events(self) -> ProfileEvents
  - def mark_frame_end(self)

- class IProfiler
  - def begin(self, mask: int, name: str)
  - def end(self, mask: int)
  - def ensure_thread(self)
  - def flow(self, arg0: int, arg1: FlowType, arg2: int, arg3: str)
  - def frame(self, arg0: int, arg1: str)
  - def get_capture_mask(self) -> int
  - def instant(self, arg0: int, arg1: InstantType, arg2: str)
  - def is_python_profiling_enabled(self) -> bool
  - def set_capture_mask(self, mask: int) -> int
  - def set_python_profiling_enabled(self, enable: bool)
  - def shutdown(self)
  - def startup(self)
  - def value_float(self, mask: int, value: float, name: str)
  - def value_int(self, mask: int, value: int, name: str)
  - def value_uint(self, mask: int, value: int, name: str)

- class InstantType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - PROCESS: carb.profiler._profiler.InstantType
  - THREAD: carb.profiler._profiler.InstantType

- class ProfileEvents
  - def get_main_thread_id(self) -> int
  - def get_profile_events(self, thread_id: int = 0) -> tuple
  - def get_profile_thread_ids(self) -> tuple

## Functions

- def acquire_profile_monitor_interface(plugin_name: str = None, library_path: str = None) -> IProfileMonitor
- def acquire_profiler_interface(plugin_name: str = None, library_path: str = None) -> IProfiler
- def begin_with_location(mask: int, name: str, function: str = '', filepath: str = '', lineno: int = 0)
- def end(mask: int)
- def is_profiler_active() -> bool
- def supports_dynamic_source_locations() -> bool
- def begin(mask, name, stack_offset = 0)
- def profile(func = None, mask = 1, zone_name = None, add_args = False)

## Other

- asyncio: builtin module
- functools: builtin module

# Public API for module carb.windowing:

## Classes

- class Cursor

- class CursorMode
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - DISABLED: carb.windowing.CursorMode
  - HIDDEN: carb.windowing.CursorMode
  - NORMAL: carb.windowing.CursorMode

- class CursorStandardShape
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - ARROW: carb.windowing.CursorStandardShape
  - CROSSHAIR: carb.windowing.CursorStandardShape
  - HAND: carb.windowing.CursorStandardShape
  - HORIZONTAL_RESIZE: carb.windowing.CursorStandardShape
  - IBEAM: carb.windowing.CursorStandardShape
  - VERTICAL_RESIZE: carb.windowing.CursorStandardShape

- class GLContext

- class IGLContext
  - def create_context_opengl(self, width: int, height: int) -> GLContext
  - def create_context_opengles(self, width: int, height: int) -> GLContext
  - def destroy_context(self, arg0: GLContext)
  - def make_context_current(self, arg0: GLContext)

- class IWindowing
  - def create_cursor(self, arg0: Image, arg1: int, arg2: int) -> Cursor
  - def create_cursor_standard(self, arg0: CursorStandardShape) -> Cursor
  - def create_window(self, width: int, height: int, title: str, fullscreen: bool, hints: int = 0) -> Window
  - def destroy_cursor(self, arg0: Cursor)
  - def destroy_window(self, arg0: Window)
  - def focus_window(self, arg0: Window)
  - def get_clipboard(self, arg0: Window) -> str
  - def get_cursor_mode(self, arg0: Window) -> CursorMode
  - def get_cursor_position(self, arg0: Window) -> carb._carb.Int2
  - def get_input_mode(self, arg0: Window, arg1: InputMode) -> bool
  - def get_keyboard(self, arg0: Window) -> carb.input.Keyboard
  - def get_monitor_position(self, arg0: Monitor) -> carb._carb.Int2
  - def get_monitor_work_area(self, arg0: Monitor) -> tuple
  - def get_monitors(self) -> tuple
  - def get_mouse(self, arg0: Window) -> carb.input.Mouse
  - def get_native_display(self, arg0: Window) -> capsule
  - def get_native_window(self, arg0: Window) -> capsule
  - def get_window_height(self, arg0: Window) -> int
  - def get_window_opacity(self, arg0: Window) -> float
  - def get_window_position(self, arg0: Window) -> carb._carb.Int2
  - def get_window_user_pointer(self, arg0: Window) -> capsule
  - def get_window_width(self, arg0: Window) -> int
  - def hide_window(self, arg0: Window)
  - def is_window_focused(self, arg0: Window) -> bool
  - def is_window_fullscreen(self, arg0: Window) -> bool
  - def is_window_maximized(self, arg0: Window) -> bool
  - def is_window_minimized(self, arg0: Window) -> bool
  - def maximize_window(self, arg0: Window)
  - def minimize_window(self, arg0: Window)
  - def poll_events(self)
  - def resize_window(self, arg0: Window, arg1: int, arg2: int)
  - def restore_window(self, arg0: Window)
  - def set_clipboard(self, arg0: Window, arg1: str)
  - def set_cursor(self, arg0: Window, arg1: Cursor)
  - def set_cursor_mode(self, arg0: Window, arg1: CursorMode)
  - def set_cursor_position(self, arg0: Window, arg1: carb._carb.Int2)
  - def set_input_mode(self, arg0: Window, arg1: InputMode, arg2: bool)
  - def set_window_content_scale(self, arg0: Window) -> carb._carb.Float2
  - def set_window_fullscreen(self, arg0: Window, arg1: bool)
  - def set_window_icon(self, arg0: Window, arg1: Image)
  - def set_window_opacity(self, arg0: Window, arg1: float)
  - def set_window_position(self, arg0: Window, arg1: carb._carb.Int2)
  - def set_window_should_close(self, arg0: Window, arg1: bool)
  - def set_window_title(self, arg0: Window, arg1: str)
  - def set_window_user_pointer(self, arg0: Window, arg1: capsule)
  - def should_window_close(self, arg0: Window) -> bool
  - def show_window(self, arg0: Window)
  - def translate_key(self, arg0: carb.input.KeyboardInput) -> carb.input.KeyboardInput
  - def update_input_devices(self)
  - def wait_events(self)

- class Image
  - def __init__(self, width: int, height: int, pixels: bytes)

- class InputMode
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - LOCK_KEY_MODS: carb.windowing.InputMode
  - RAW_MOUSE_MOTION: carb.windowing.InputMode
  - STICKY_KEYS: carb.windowing.InputMode
  - STICKY_MOUSE_BUTTONS: carb.windowing.InputMode

- class Monitor

- class Window

## Functions

- def acquire_gl_context_interface(plugin_name: str = None, library_path: str = None) -> IGLContext
- def acquire_windowing_interface(plugin_name: str = None, library_path: str = None) -> IWindowing

## Variables

- WINDOW_HINT_FLOATING: int
- WINDOW_HINT_MAXIMIZED: int
- WINDOW_HINT_NONE: int
- WINDOW_HINT_NO_AUTO_ICONIFY: int
- WINDOW_HINT_NO_DECORATION: int
- WINDOW_HINT_NO_FOCUS_ON_SHOW: int
- WINDOW_HINT_NO_RESIZE: int
- WINDOW_HINT_SCALE_TO_MONITOR: int

# Public API for module carb.eventdispatcher:

## Classes

- class Event
  - def get(self, key_name: str) -> object
  - def has_key(self, key_name: str) -> bool
  - [property] def event_name(self) -> str

- class IEventDispatcher
  - def dispatch_event(self, event_name: str, payload: handle = None) -> int
  - def has_observers(self, event_name: str, filter: handle = None) -> bool
  - static def observe_event(*args, **kwargs) -> typing.Any

- class IMessageQueue
  - def get_name(self) -> str
  - def get_owning_thread(self) -> int
  - def has_messages(self) -> bool
  - def peek(self, fn: typing.Callable[[Event], None]) -> bool
  - def stop(self)
  - def try_pop(self, fn: typing.Callable[[Event], None]) -> bool

- class IMessageQueueFactory
  - def create_message_queue(self, name: str, **kwargs) -> typing.Tuple[IMessageQueue, bool]
  - def get_message_queue(self, name: str) -> IMessageQueue

- class ObserverGuard
  - def reset(self)
  - [property] def enabled(self) -> bool
  - [enabled.setter] def enabled(self, arg1: bool)
  - [property] def name(self) -> str
  - [property] def order(self) -> int
  - [order.setter] def order(self, arg1: int)

## Functions

- def acquire_eventdispatcher_interface(*args, **kwargs) -> typing.Any
- def acquire_messagequeue_factory_interface(*args, **kwargs) -> typing.Any
- def get_eventdispatcher_interface() -> IEventDispatcher
- def get_eventdispatcher() -> IEventDispatcher
- def get_messagequeue_factory_interface() -> IMessageQueueFactory
- def get_messagequeue_factory() -> IMessageQueueFactory

## Other

- asyncio: builtin module
- lru_cache: unknown


# Public API for module carb.variant:

## Classes

- class IVariant

## Functions

- def acquire_variant_interface(plugin_name: str = None, library_path: str = None) -> IVariant
- def get_variant_interface() -> IVariant
- def get_variant() -> IVariant

## Other

- lru_cache: unknown

# Public API for module omni.core:

## Classes

- class Float2
  - def __init__(self)
  - def __init__(self, arg0: typing.Sequence)
  - def __init__(self, x: float, y: float)
  - [property] def h(self) -> float
  - [h.setter] def h(self, arg0: float)
  - [property] def s(self) -> float
  - [s.setter] def s(self, arg0: float)
  - [property] def t(self) -> float
  - [t.setter] def t(self, arg0: float)
  - [property] def u(self) -> float
  - [u.setter] def u(self, arg0: float)
  - [property] def v(self) -> float
  - [v.setter] def v(self, arg0: float)
  - [property] def w(self) -> float
  - [w.setter] def w(self, arg0: float)
  - [property] def x(self) -> float
  - [x.setter] def x(self, arg0: float)
  - [property] def y(self) -> float
  - [y.setter] def y(self, arg0: float)

- class IObject

- class ITypeFactory(_ITypeFactory, IObject)
  - def __init__(self, arg0: IObject)
  - def __init__(self)
  - def get_type_id_name(self, id: int) -> str
  - def register_interface_implementations_from_module(self, module_name: str, flags: int) -> int
  - def set_interface_defaults(self, interface_id: int, impl_id: int, module_name: str, impl_version: int)
  - def unregister_interface_implementations_from_module(self, module_name: str) -> int

- class Int2
  - def __init__(self)
  - def __init__(self, arg0: typing.Sequence)
  - def __init__(self, x: int, y: int)
  - [property] def h(self) -> int
  - [h.setter] def h(self, arg0: int)
  - [property] def s(self) -> int
  - [s.setter] def s(self, arg0: int)
  - [property] def t(self) -> int
  - [t.setter] def t(self, arg0: int)
  - [property] def u(self) -> int
  - [u.setter] def u(self, arg0: int)
  - [property] def v(self) -> int
  - [v.setter] def v(self, arg0: int)
  - [property] def w(self) -> int
  - [w.setter] def w(self, arg0: int)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)

- class Result
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - ACCESS_DENIED: omni.core._core.Result
  - ALREADY_EXISTS: omni.core._core.Result
  - FAIL: omni.core._core.Result
  - INSUFFICIENT_BUFFER: omni.core._core.Result
  - INTERRUPTED: omni.core._core.Result
  - INVALID_ARGUMENT: omni.core._core.Result
  - INVALID_DATA_SIZE: omni.core._core.Result
  - INVALID_DATA_TYPE: omni.core._core.Result
  - INVALID_INDEX: omni.core._core.Result
  - INVALID_OPERATION: omni.core._core.Result
  - INVALID_STATE: omni.core._core.Result
  - NOT_ENOUGH_DATA: omni.core._core.Result
  - NOT_FOUND: omni.core._core.Result
  - NOT_IMPLEMENTED: omni.core._core.Result
  - NOT_SUPPORTED: omni.core._core.Result
  - NO_INTERFACE: omni.core._core.Result
  - NO_MORE_ITEMS: omni.core._core.Result
  - NULL_POINTER: omni.core._core.Result
  - OPERATION_ABORTED: omni.core._core.Result
  - OUT_OF_MEMORY: omni.core._core.Result
  - SUCCESS: omni.core._core.Result
  - TIMED_OUT: omni.core._core.Result
  - TOO_MUCH_DATA: omni.core._core.Result
  - TRY_AGAIN: omni.core._core.Result
  - VERSION_CHECK_FAILURE: omni.core._core.Result
  - VERSION_PARSE_ERROR: omni.core._core.Result
  - WOULD_BLOCK: omni.core._core.Result

- class TypeFactoryLoadFlags
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - NONE: omni.core._core.TypeFactoryLoadFlags

- class UInt2
  - def __init__(self)
  - def __init__(self, arg0: typing.Sequence)
  - def __init__(self, x: int, y: int)
  - [property] def h(self) -> int
  - [h.setter] def h(self, arg0: int)
  - [property] def s(self) -> int
  - [s.setter] def s(self, arg0: int)
  - [property] def t(self) -> int
  - [t.setter] def t(self, arg0: int)
  - [property] def u(self) -> int
  - [u.setter] def u(self, arg0: int)
  - [property] def v(self) -> int
  - [v.setter] def v(self, arg0: int)
  - [property] def w(self) -> int
  - [w.setter] def w(self, arg0: int)
  - [property] def x(self) -> int
  - [x.setter] def x(self, arg0: int)
  - [property] def y(self) -> int
  - [y.setter] def y(self, arg0: int)

## Functions

- def create_type(type_id: str, module_name: str = None, version: int = 0) -> IObject
- def register_module(module_name: str, flags: int = 0) -> int

## Other




# Public API for module omni.structuredlog:

## Classes

- class IStructuredLogControl(_IStructuredLogControl, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def close_log(self, event: int)
  - def stop(self)

- class IStructuredLogControl2(_IStructuredLogControl2, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def emit_process_lifetime_exit_event(self, reason: str)

- class IStructuredLogExtraFields(_IStructuredLogExtraFields, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def set_value(self, field_name: str, value: str, flags: int) -> bool

- class IStructuredLogFromILog(_IStructuredLogFromILog, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def disable_logging(self)
  - def enable_logging(self)
  - [property] def logging_event_id(self) -> int

- class IStructuredLogFromILog2(_IStructuredLogFromILog2, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def set_logging_event_flags(self, set_flags: int, clear_flags: int) -> bool
  - [property] def log_level(self) -> int
  - [log_level.setter] def log_level(self, arg1: int)

- class IStructuredLogSettings(_IStructuredLogSettings, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def enable_schemas_from_settings(self) -> bool
  - def get_log_path_for_event(self, event_id: int) -> str
  - def load_privacy_settings(self) -> bool
  - static def set_event_id_mode(*args, **kwargs) -> typing.Any
  - [property] def event_id_mode(self) -> typing.Any
  - [property] def event_id_type(self) -> typing.Any
  - [property] def event_queue_size(self) -> int
  - [event_queue_size.setter] def event_queue_size(self, arg1: int)
  - [property] def log_default_name(self) -> str
  - [log_default_name.setter] def log_default_name(self, arg1: str)
  - [property] def log_output_path(self) -> str
  - [log_output_path.setter] def log_output_path(self, arg1: str)
  - [property] def log_retention_count(self) -> int
  - [log_retention_count.setter] def log_retention_count(self, arg1: int)
  - [property] def log_size_limit(self) -> int
  - [log_size_limit.setter] def log_size_limit(self, arg1: int)
  - [property] def session_id(self) -> int
  - [property] def user_id(self) -> str
  - [user_id.setter] def user_id(self, arg1: str)

- class IStructuredLogSettings2(_IStructuredLogSettings2, omni.core._core.IObject)
  - def __init__(self, arg0: omni.core._core.IObject)
  - def __init__(self)
  - def set_output_flags(self, flags_to_add: int, flags_to_remove: int)
  - [property] def heartbeat_period(self) -> int
  - [heartbeat_period.setter] def heartbeat_period(self, arg1: int)
  - [property] def need_log_headers(self) -> bool
  - [need_log_headers.setter] def need_log_headers(self, arg1: bool)
  - [property] def output_flags(self) -> int

- class IdMode
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - FAST_SEQUENTIAL: omni.structuredlog._structuredlog.IdMode
  - RANDOM: omni.structuredlog._structuredlog.IdMode
  - SEQUENTIAL: omni.structuredlog._structuredlog.IdMode

- class IdType
  - def __init__(self, value: int)
  - [property] def name(self) -> str
  - [property] def value(self) -> int
  - UINT64: omni.structuredlog._structuredlog.IdType
  - UUID: omni.structuredlog._structuredlog.IdType

- class InvalidEventException

- class InvalidSchemaException

- class StructuredLogEvent
  - [property] def eventId(self) -> int
  - [property] def schema(self) -> dict

- class UniqueApp
  - def connect_client_process(self) -> bool
  - def disconnect_client_process(self)

## Functions

- def create_launch_guard() -> UniqueApp
- def register_schema(schema: dict) -> dict
- def send_event(*args, **kwargs) -> typing.Any

## Variables

- ALL_SCHEMAS: int
- DEFAULT_LOG_PATH_EVENT: int

## Other



