from decorators import JSONDumper

glob_variable = 1

@JSONDumper(targetDir="..\\..\\tests\\testTest_suites", isActive=True)
def funcTestee(p_iNum):
    return 1/p_iNum

# def funcTesteeWithMultipleReturnValues(p_iNum):
#     return p_iNum, 1/p_iNum
#
# def simplestFunction(p_iNum):
#     return 1+p_iNum


for i in range(-1, 3):
    i = funcTestee(i)
    print(i)

