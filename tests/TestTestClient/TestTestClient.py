from decorator.decorators import JSONDumper
from JSONUnittest_TestTestClient import test_JSONTestTestClient

glob_variable = 1


@JSONDumper(testSuite=test_JSONTestTestClient)
def funcTestee(p_iNum):
    return 1 / p_iNum


# def funcTesteeWithMultipleReturnValues(p_iNum):
#     return p_iNum, 1/p_iNum
#
# def simplestFunction(p_iNum):
#     return 1+p_iNum

if __name__ == "__main__":
    for i in range(-1, 3):
        i = funcTestee(i)
        print(i)
