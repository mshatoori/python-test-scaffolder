import libcst as cst

from module_visitor import ModuleVisitor


def main():
    module_name = 'guinea_pig'
    with open(f"{module_name}.py", "r") as source:
        tree = cst.parse_module(source.read())

        module_visitor = ModuleVisitor(module_name)
        tree.visit(module_visitor)


if __name__ == "__main__":
    main()
