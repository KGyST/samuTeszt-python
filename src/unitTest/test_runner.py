import unittest
import json
from common.publicFunctions import *
from common.privateFunctions import generateFolder, caseFileCollector, open_and_create_folders
from common.constants import *
import jsonpickle
from typing import Callable
from decorator.decorators import FunctionDumper


#FIXME currently this is .json only, enable for yaml xml through DI
class JSONTestSuite(unittest.TestSuite):
    def __init__(self,
                 target_folder: str=TEST_ITEMS,
                 cases_only: str="",
                 case_filter_func: Callable=case_filter_func,
                 comparer_func: Callable=default_comparer_func,
                 ):
        """
        :param target_folder:
        :param cases_only: filenames with or without extension divided by;
        :param case_filter_func:
        :param comparer_func:
        """
        # self._tests is an inherited member!
        self._tests = []
        self._folder = os.path.join(target_folder, )
        FunctionDumper.bDump = False
        # generateFolder()

        for sFilePath in caseFileCollector(self._folder,
                                           cases_only,
                                           case_filter_func,
                                           ".json"):
            try:
                with open(os.path.join(self._folder, sFilePath), "r") as jf:
                    testData = jsonpickle.loads(jf.read())
                testCase = JSONTestCase(testData, self._folder, sFilePath, comparer_func)
                testCase.maxDiff = None
                self.addTest(testCase)
            except json.decoder.JSONDecodeError:
                print(f"JSONDecodeError - Filename: {sFilePath}")
                continue
        super().__init__(self._tests)

    def __contains__(self, test_name: str) -> bool:
        for test in self._tests:
            if test._testMethodName == test_name:
                return True
        return False


class JSONTestCase(unittest.TestCase):
    def __init__(self, test_data:dict, dir: str, file_name: str, comparer_func: Callable):
        self.sDir = dir
        self.sFile = file_name
        func = self.JSONTestCaseFactory(test_data, dir, file_name, comparer_func)
        setattr(JSONTestCase, func.__name__, func)
        super().__init__(func.__name__)


    @staticmethod
    def JSONTestCaseFactory(test_data:dict, parent_folder: str, file_name: str, comparer_function: Callable=default_comparer_func)->'Callable':
        def func(object):
            sOutFile = os.path.join(parent_folder, "errors", file_name)
            testResult = None

            try:
                import importlib
                module = importlib.import_module(test_data[MODULE_NAME])
                if CLASS_NAME in test_data and test_data[CLASS_NAME]:
                    _class = getattr(module, test_data[CLASS_NAME])
                    func = getattr(_class, test_data[FUNC_NAME])
                else:
                    func = getattr(module, test_data[FUNC_NAME])

                comparer_function(object, func, test_data[ARGS], test_data[KWARGS], test_data[RESULT])
            except Exception as e:
                # FIXME exception to json TypeError: Object of type ZeroDivisionError is not JSON serializable
                # "exception": JSONSeriazable(e)
                test_data.update({RESULT: testResult,})

                # try:
                with open_and_create_folders(sOutFile, "w") as fOutput:
                    json.dump(test_data, fOutput, indent=4)
                raise
        if NAME in test_data:
            func.__name__ = test_data[NAME]
        else:
            func.__name__ = "test_" + file_name[:-5]
        return func

