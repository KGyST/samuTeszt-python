from samuTeszt.src.decorator.decorators import Recorder
from samuTeszt.examples.helpers import ZeroDivisionErrorCatcher


@Recorder()
@ZeroDivisionErrorCatcher
def funcTestee(num: int):
    return 1 / num, num


if __name__ == "__main__":
    for i in range(-1, 3):
        i = funcTestee(i)
        print(i)

    print(funcTestee(100))

