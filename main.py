import libcst as cst

from module_visitor import ModuleVisitor


def main():
    with open("guinea_pig.py", "r") as source:
        tree = cst.parse_module(source.read())

        with open('tree.py', 'w') as f:
            f.write(str(tree))

        module_visitor = ModuleVisitor()
        tree.visit(module_visitor)


if __name__ == "__main__":
    main()
