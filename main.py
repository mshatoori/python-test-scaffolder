import ast
from typing import Any


def main():
    with open("guinea_pig.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)


class Analyzer(ast.NodeVisitor):
    def visit_Module(self, node: ast.Module) -> Any:
        print('Visited', ast.dump(node, indent=2))

if __name__ == "__main__":
    main()
