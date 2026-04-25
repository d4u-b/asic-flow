# Execution Path

Back: [[00_Python_Function_Map]]

## Main Runtime Chain

1. [src/asic_flow/__main__.py](../../src/asic_flow/__main__.py) calls `main()` from `asic_flow.cli`.
2. [[02_Module_cli#main]] parses CLI args and branches into `list` or `run`.
3. [[02_Module_cli#_load_executor]] calls [[03_Module_config#load_manifest]].
4. [[03_Module_config#load_manifest]] builds a `Manifest` and `FlowDefinition` objects.
5. `FlowExecutor(...)` is created in [[05_Module_executor#flowexecutor__init__]].
6. [[05_Module_executor#flowexecutorlist_flows]] returns enabled flows for `list`.
7. [[05_Module_executor#flowexecutorrun]] prepares directories and resolves requested flow names.
8. [[05_Module_executor#flowexecutor_run_one]] recursively walks dependencies.
9. [[06_Module_registry#load_flow_class]] imports the plugin class named by the manifest.
10. Flow objects inherit from [[07_Module_flows_base#baseflow]].
11. Concrete `run()` methods come from [[08_Module_flows_builtin#commandflowrun]] or a custom plugin such as [[09_Module_project_flows_custom_power#powerflowrun]].
12. Shell commands are executed through [[07_Module_flows_base#baseflowrun_command]].

## Trace By Use Case

### `asic-flow list`

- [[02_Module_cli#main]]
- [[02_Module_cli#_load_executor]]
- [[03_Module_config#load_manifest]]
- [[05_Module_executor#flowexecutorlist_flows]]

### `asic-flow run quality`

- [[02_Module_cli#main]]
- [[02_Module_cli#_load_executor]]
- [[03_Module_config#load_manifest]]
- [[05_Module_executor#flowexecutorrun]]
- [[05_Module_executor#flowexecutor_run_one]]
- [[06_Module_registry#load_flow_class]]
- `flow.run()` in a builtin or custom plugin

## Important Data Objects

- `FlowDefinition`: per-flow config loaded from manifest. See [[03_Module_config]].
- `Manifest`: project-wide runtime config. See [[03_Module_config]].
- `FlowContext`: runtime state and path resolution. See [[04_Module_context]].
