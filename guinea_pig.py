from time import sleep as sleep2


def function_to_be_tested(i):
    print('i is:', i)
    sleep2(4)
    return "Yay! I'm going to be tested using this project!"


def another_function():
    pass


def _internal_function():
    pass

class Clazz:
    def func_in_class(self):
        pass
