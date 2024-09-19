from common.privateFunctions import open_and_create_folders
import json
from common.constants import MAIN, BUILTINS, MODULE_NAME
import jsonpickle
from .ICodec import ICodec
from data.ProgramState import ProgramState


class JSONCodec(ICodec):
    sExt = ".json"
    _module = ""

    PY_OBJECT = 'py/object'
    PY_FUNCTION = 'py/function'
    PY_TYPE = 'py/type'

    @staticmethod
    def read(path: str) -> 'ProgramState':
        JSONCodec.find_and_import_classes(path)
        jf = open(path, "r").read()
        try:
            from decorator import Dumper
            Dumper.bDump = False
            assert isinstance(_result := jsonpickle.loads(jf), ProgramState)
            return _result
        except Exception as e:
            raise JSONCodec.StorageException(e)

    @staticmethod
    def reads(data: str) -> 'ProgramState':
        assert isinstance(_result := jsonpickle.loads(data), ProgramState)
        return _result

    @staticmethod
    def dumps(data) -> str:
        from decorator import Dumper
        Dumper.bDump = False
        _dumps = json.dumps(data.__getstate__(), indent=4)
        return _dumps

    @staticmethod
    def dump(path: str, data: dict):
        with open_and_create_folders(path, "w") as fOutput:
            fOutput.write(JSONCodec.dumps(data))

    @staticmethod
    def find_and_import_classes(path: str):
        """
        Import modules that define classes dumped in test cases
        Recursively calls _find_and_import_classes
        FIXME to abstract not to be json-dependent
        :param path: test case data file path
        :return: None
        """
        with open(path, "r") as jf:
            importData = json.loads(jf.read())
            JSONCodec._find_and_import_classes(importData)

    @staticmethod
    def _find_and_import_classes(importData):
        """
        Recursor called by find_and_import_classes
        :param importData:
        :return: None
        """
        import importlib

        if isinstance(importData, dict):
            if JSONCodec.PY_OBJECT in importData:
                class_path = importData[JSONCodec.PY_OBJECT]
                module_name, class_name = class_path.rsplit('.', 1)
                try:
                    module = importlib.import_module(module_name)
                    if module_name != BUILTINS:
                        getattr(module, class_name)  # Ensure the class is loaded
                except (ImportError, AttributeError) as e:
                    print(f"Error importing {class_path}: {e}")
            for key, value in importData.items():
                JSONCodec._find_and_import_classes(value)
        elif isinstance(importData, list):
            for item in importData:
                JSONCodec._find_and_import_classes(item)

    # @staticmethod
    # def clean(j: str):
    #     dJson = json.loads(j)
    #     JSONCodec._module = dJson[MODULE_NAME]
    #     dJson = JSONCodec._clean(dJson)
    #     return json.dumps(dJson, indent=4)
    #
    # @staticmethod
    # def _clean(element):
    #     if isinstance(element, dict):
    #         _dElement = {}
    #         for k, item in element.items():
    #             if not JSONCodec._isBuiltin(item):
    #                 if k == JSONCodec.PY_OBJECT or k == JSONCodec.PY_FUNCTION or k == JSONCodec.PY_TYPE:
    #                     if item.startswith(MAIN):
    #                         item = str.replace(item, MAIN, JSONCodec._module)
    #                 item = JSONCodec._clean(item)
    #                 _dElement[k] = item
    #         element = _dElement
    #     elif isinstance(element, list) or isinstance(element, tuple):
    #         _lElement = []
    #         for item in element:
    #             if not JSONCodec._isBuiltin(item):
    #                 item = JSONCodec._clean(item)
    #                 _lElement.append(item)
    #         element = _lElement
    #         if isinstance(element, tuple):
    #             element = tuple(element)
    #     return element
    #
    # @staticmethod
    # def _isBuiltin(item):
    #     if isinstance(item, dict):
    #         if JSONCodec.PY_OBJECT in item:
    #             if item[JSONCodec.PY_OBJECT].startswith(BUILTINS):
    #                 return True
    #     return False
