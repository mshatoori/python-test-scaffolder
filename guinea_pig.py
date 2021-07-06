from time import sleep as sleep2


def function_to_be_tested(i):
    print('i is:', i)

    if i <= 0:
        return 0

    if isinstance(i + 9, int):
        print('Yooo')
    elif i is None:
        print(None)
    else:
        print('Meh')

    if i > 9:
        if i < 10:
            i -= 1
        if i == 9:
            assert False

    sleep2(4)
    return "Yay! I'm going to be tested using this project!"


def another_function():
    pass


def _internal_function():
    pass

class Clazz:
    def func_in_class(self):
        pass


# (root, [
# (EMPTY, [
# (If, []), (If, []), (Else, []), (If, [(If, []), (EMPTY, [(If, []), (EMPTY, []), (EMPTY, [])])])])])