import glob
import os.path
import shutil
from samuTeszt.src.common.constants import TEST_ITEMS
from samuTeszt.src.common.publicFunctions import *


def md5Collector(codec,
                 folder: str = TEST_ITEMS,
                 cases_only: str = "",
                 case_filter_func: Callable = case_filter_func) -> dict[str, str]:
    """
    Collects MD5s of test cases
    :param codec: codec
    :param folder: where to collect
    :param cases_only:
    :param case_filter_func:
    :return:
    """
    # TODO doesn't seem to work
    dResult = {}
    for sFilePath in caseFileCollector(folder, cases_only, case_filter_func, codec.sExt):
        dCase = codec.read(os.path.join(folder, sFilePath))
        # if MD5 in dCase:
        #     sMD5 = dCase[MD5]
        #     dResult[sMD5] = sFilePath
    return dResult


def caseFileCollector(folder: str,
                      cases_only: str,
                      case_filter_func: Callable,
                      ext: str) -> list[str]:
    resultCaseS = []
    if not os.path.exists(folder):
        return resultCaseS
    resultCaseS = glob.glob('**/*' + ext, root_dir=folder, recursive=True)
    if case_filter_func:
        def _caseFilter(file_name: str):
            return case_filter_func(file_name, ext, cases_to_be_tested=cases_only)
        resultCaseS = list(filter(_caseFilter, resultCaseS))
    return resultCaseS


def generateFolder(folder_path: str, force_delete: bool = False):
    """
    :param folder_path:
    :param force_delete:
    :return: None
    """
    if os.path.exists(folder_path):
        if force_delete:
            try:
                shutil.rmtree(folder_path)
            except OSError:
                # FIXME maybe removing all the files from the folder
                pass
        else:
            # Common case
            return
    try:
        os.makedirs(folder_path)
    except PermissionError:
        # FIXME handling
        pass


def open_and_create_folders(file: str, mode: str):
    try:
        return open(file, mode)
    except FileNotFoundError:
        folder_path = os.path.dirname(file)
        os.makedirs(folder_path, exist_ok=True)
        return open(file, mode)

# ----------------------------------------------------------

def _get_calling_module_name() -> str:
    """
    Gets the module name from its filename if the module itself is the __main__
    :return: the module_name: str
    """
    import inspect
    frame = inspect.currentframe().f_back
    while frame:
        if frame.f_globals['__name__'] == '__main__':
            _f = frame.f_globals['__file__']
            return os.path.splitext(os.path.basename(_f))[0]
        frame = frame.f_back
    return frame.f_globals['__name__']


def _get_original_function(func: 'Callable') -> 'Callable':
    """
    Recursively get the original function if there are decorators on it.
    :param func: The decorated function or bound method
    :return: The original undecorated function
    """
    from samuTeszt.src.decorator.decorators import _Dumper

    if hasattr(func, '__self__') and isinstance(func.__self__, _Dumper):
        return func.__self__.func

    # If it's a method wrapped by a decorator like `Dumper`, it might have a __wrapped__ attribute
    if hasattr(func, '__wrapped__'):
        return _get_original_function(func.__wrapped__)

    # Handle bound methods that are transformed (like __call__)
    if hasattr(func, '__func__'):
        func = func.__func__

    # Check for closure attributes that might hide the original function
    if hasattr(func, '__closure__') and func.__closure__:
        try:
            for cell in func.__closure__:
                if isinstance((_callable := cell.cell_contents), Callable) and not isinstance(_callable, type):
                    return _get_original_function(_callable)
        except (ValueError, IndexError, AttributeError):
            return func
    return func


def get_original_function_name(func: 'Callable') -> tuple[str, str, str]:
    """
    Get the real function name considering module names, class names, decorators, etc.
    :param func: a function
    :return: (module_name: str, class_name: str, function_name: str)
    """

    module_name, class_name, func_name = None, None, func.__name__

    # Extract the original function from the closure attribute of the wrapper
    original_func = _get_original_function(func)
    if original_func:
        module_name = original_func.__module__
        class_name = original_func.__qualname__.split('.')[0] if '.' in original_func.__qualname__ else ""
        func_name = original_func.__name__

    # When the script is run directly, use __file__ to get the module name
    if module_name == '__main__':
        module_name = _get_calling_module_name()
    return module_name, class_name, func_name

