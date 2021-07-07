from typing import Optional

import libcst as cst

from function_visitor import FunctionVisitor


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
        v = FunctionVisitor()
        node.body.visit(v)
        v.log_foc_tree()

    def leave_FunctionDef(self, original_node: "FunctionDef") -> None:
        print(f'Leaving function {original_node.name.value}')
        self.current_function = None