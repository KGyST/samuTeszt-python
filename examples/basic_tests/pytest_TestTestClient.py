from pyTest.pyTestFramework import getTests, defaultComparer
import os
import pytest

pytest_plugins = ("pyTest.conftest")

class Test_JSONpytestClient():
    testOnly    = os.environ['TEST_ONLY'] if "TEST_ONLY" in os.environ else ""            # Delimiter: ; without space, filenames without ext
    targetDir   = "testJSONTest"
    isActive    = False

    @pytest.mark.parametrize(
        'p_testCase', getTests("testJSONTest")
    )
    def test_file(self, p_testCase):
        from basicTestClient import funcTestee

        defaultComparer(funcTestee, p_testCase)

        print(p_testCase)

