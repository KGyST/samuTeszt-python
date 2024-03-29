# SamuTest

## What is this?
This is a unit-testing metaframework (built on top of unittest and pytest) that makes it possible to automatize both the test writing ("Recording") and testing itself ("Playing").
## How it works
Instead of writing test functions, one only has to put a decorator to the function to be tested. 
Anytime (if conditions met; during functional testing or even in production) the decorator dumps out function arguments (like args, kwargs, global variables, etc) and the results (returned values, raised exceptions, modified values of global variables) into data (by default .json) files.
This is the "Recording" phase.

When running tests ("Playing"), the test runner function reads all data files, calls the function according the data in them and compares the results. If the test fails, it writes another data file (or record), making it easy to compare the expected and the given result.
## Development Driven Testing Manifesto

## TODOs
- PublicFunctions parameters fixes, docstrings
- Variable/parameter naming conventions
- Folder structure *items/errors*
  - Class names in folder names, customizable
  - There should be a `tests` folder. If not in the actual folder, one has to handle the paths in order not to have two source files with the same name at different paths. So multiple `tests` folders, each besides the actual source file.   
  - Under it, a (module).class.function (+ `_items`. or not)
    - It would be more elegant to create suites in a module/class/functon manner
  - Besides it, an `_errors`
  - And there a `.WinMerge`
- Facelift/update outdated stuff
  - ~~WinMerge~~
  - ... as an option
- Object-oriented issues
  - Class variable handling by metaclass
  - `__new__()` parameter anomalies 
---
- Global variable handling pre/post
- Options to be added
- Parametrization, new parameters
  - `run_only`
- Exception as a result handling + config
  - Whether to run `current.json` 
- Function mocking
- Test fixtures and `__init__.json` 
- Packaging and distribution
  - Case names
- Test runner:
  - Simple test runner, PyCharm integration
  - Test stuites based on mod/class/func
- ~~MD5 checking: if another file with the same MD5 is there, but with another filename, don't write it.~~
- Config object
  - .json, .yaml, .xml
- `current.json` issues rotating (.001, .002 etc)
- Dumping into a database instead of files
- `@JSONFunctionDumper` to be able to be run as `@JSONFunctionDumper` (not only as `@JSONFunctionDumper()`)
- If `tests` is not a subfolder of the tested function, it's not possible to import the module (no `folder.module`)