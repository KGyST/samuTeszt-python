import functools

import jsonpickle
import os
import hashlib
from common.constants import *
from common.privateFunctions import generateFolder, open_and_create_folders, get_original_function_name, md5Collector
from common.publicFunctions import get_file_path
from io import StringIO
from typing import Callable, Type
import inspect
from copy import deepcopy
import sys
from importlib import import_module


class DumperBase:
    # FIXME mocked functions
    # FIXME global vars handling
    bDump = False

    class DumperException(Exception):
        pass

    def __init__(self,
                 extension: str,  # test default name, like '.json'
                 export_function: Callable,  # data export function, like jsondumper
                 target_folder: str=TEST_ITEMS,  # place everything into this dir
                 current_test_name: str ="current",  # test default name, like current
                 active: bool=False,  # global on/off switch of the test dumper
                 generate_init_files: bool=True,  # generate init files, like WinMerge, typically for the first run
                 nNameHex: int=12):                  # for default testcase filename generating
        self.__class__.bDump = active
        self.sMainTestFolder = target_folder
        self.sDefaultTest = current_test_name
        self.nNameHex = nNameHex
        self.sExt = extension
        self.fExport = export_function
        self.bGenerateInitFiles = generate_init_files
        self.sModule = ""
        self.sClass = ""
        self.sFunction = ""
        self.sTest = ""
        self.sCaseFolder = ""
        self.sErrorFolder = ""
        self.md5S = set()

    def __call__(self, func, *args, **kwargs):
        if not self.__class__.bDump:
            return func
        self.sModule, self.sClass, self.sFunction = get_original_function_name(func)
        self.sTest = ".".join([self.sClass, self.sFunction]) if self.sClass else self.sFunction
        self.sCaseFolder = os.path.join(self.sMainTestFolder, self.sTest)
        self.md5S.update(md5Collector(self.sCaseFolder))
        self.sErrorFolder = os.path.join(self.sMainTestFolder, self.sTest) + ERROR_STR
        if self.bGenerateInitFiles:
            self._initFiles()

    def _initFiles(self):
        # FIXME WinMerge as an option
        if not os.path.exists(sWinMergePath := os.path.join(self.sMainTestFolder, self.sTest + ".WinMerge")) \
                and not os.path.exists(self.sTest) \
                and not os.path.exists(os.path.join("..", self.sCaseFolder + ERROR_STR)):
            generateFolder(self.sCaseFolder)

            import xml.etree.ElementTree as ET
            tree = ET.parse(StringIO(WINMERGE_TEMPLATE))
            root = tree.getroot()
            root.find('paths/left').text = self.sTest
            root.find('paths/right').text = os.path.join("errors", self.sTest)
            tree.write(sWinMergePath)

    def dump(self, pre:dict, post: dict):
        sHash = hashlib.md5(self.fExport(pre).encode("ansi")).hexdigest()[:self.nNameHex]
        if sHash in self.md5S:
            return

        sFileName = "".join((sHash, self.sExt))
        post[MD5] = sHash
        pre.update(post)
        sOutput = self.fExport(pre)

        if not os.path.exists(sFile:=(os.path.join(self.sCaseFolder, sFileName))):
            with open_and_create_folders(sFile, "w") as f:
                f.write(sOutput)

        # Like current.json:
        pre[NAME] = 'Current test'
        sOutput = self.fExport(pre)
        with open_and_create_folders(os.path.join(self.sMainTestFolder, self.sDefaultTest + self.sExt), "w") as f:
            f.write(sOutput)


class FunctionDumper(DumperBase):
    """
    Decorator functor to modify the tested functions
    Reason for having a Base class is for potentially being able to inherit into an xml or yaml writer
    """

    # Very much misleading, this __call__ is called only once, at the beginning to create wrapped_function:
    def __call__(self, func, *args, **kwargs):
        if not self.__class__.bDump:
            return func
        super().__call__(func, *args, **kwargs)

        functools.wraps(func)
        def wrapped_function(*argsWrap, **kwargsWrap):
            # try:
                dPre = ({
                    MODULE_NAME: self.sModule,
                    CLASS_NAME: self.sClass,
                    FUNC_NAME: self.sFunction,
                })

                _mod = import_module(self.sModule)

                if argsWrap and hasattr(argsWrap[0], '__dict__'):
                    _class = getattr(sys.modules[self.sModule], self.sClass)
                    instance = _class.__new__(_class)
                    instance.__dict__ = argsWrap[0].__dict__
                    argsWrap = argsWrap[1:]
                    instance_pre = deepcopy(instance)
                    dPre.update({INST_PRE: instance_pre})
                else:
                    instance = None
                    instance_pre = None

                if isinstance(func, classmethod):
                    _class = getattr(_mod, self.sClass)
                    fResult = func.__func__(_class, *argsWrap[1:], **kwargsWrap)
                elif isinstance(func, staticmethod):
                    fResult = func(*argsWrap[1:], **kwargsWrap)
                else:
                    if instance_pre:
                        # member method
                        fResult = func(instance, *argsWrap, **kwargsWrap)
                        argsWrap = (instance_pre, *argsWrap)
                    else:
                        # standalone function
                        fResult = func(*argsWrap, **kwargsWrap)

            # except (Exception, TypeError, ZeroDivisionError) as e:
            #     # FIXME Exception handling
            #     raise
            # else:
                dPre.update({ARGS: argsWrap,
                             KWARGS: kwargsWrap,
                                })
                dPost = {RESULT: fResult,
                         INST_POST: instance,}
                super(FunctionDumper, self).dump(dPre, dPost)

                return fResult
        return wrapped_function


class JSONDumper(DumperBase):
    def __init__(self, *args, **kwargs):
        def jsonEx(p_sDict):
            return jsonpickle.dumps(p_sDict, indent=4, make_refs=False)
        super().__init__(".json", jsonEx, *args, **kwargs)


class YAMLDumper(DumperBase):
    def __init__(self, *args, **kwargs):
        import yaml
        super() .__init__(".yaml", yaml.dump, *args, **kwargs)


class JSONFunctionDumper(JSONDumper, FunctionDumper, ):
    pass


class YAMLFunctionDumper(YAMLDumper, FunctionDumper, ):
    pass

