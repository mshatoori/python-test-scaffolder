from typing import Optional

import libcst as cst

from function_visitor import FunctionVisitor
from test_generator import TestGenerator


class ModuleVisitor(cst.CSTVisitor):
    def __init__(self):
        super(ModuleVisitor, self).__init__()
        self.current_function = None

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        return False  # Don't look for class methods

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        print(f'Visiting function {node.name.value}')
        self.current_function = node
        return True

    def visit_FunctionDef_body(self, node: "FunctionDef") -> None:
        print(f'Visiting function body {node.name.value}')
        v = FunctionVisitor(node)
        node.body.visit(v)

        tg = TestGenerator(v.foc)
        with open('gen_test.py', 'w') as test_file:
            test_file.write(tg.generate())


    def leave_FunctionDef(self, original_node: "FunctionDef") -> None:
        print(f'Leaving function {original_node.name.value}')
        self.current_function = None