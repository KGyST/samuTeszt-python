from samuTeszt.src.decorator.decorators import Dumper
from samuTeszt.examples.helpers import ZeroDivisionErrorCatcher


@Dumper()
@ZeroDivisionErrorCatcher
def funcTestee(number):
    return 1 / number


if __name__ == "__main__":
    for i in range(-1, 3):
        i = funcTestee(i)
        print(i)

    print(funcTestee(100))

