from typing import Optional

import libcst as cst
from libcst._nodes.internal import CodegenState


def main():
    with open("guinea_pig.py", "r") as source:
        tree = cst.parse_module(source.read())

        with open('tree.py', 'w') as f:
            f.write(str(tree))

        module_visitor = ModuleVisitor()
        tree.visit(module_visitor)


class ModuleVisitor(cst.CSTVisitor):
    def __init__(self):
        super(ModuleVisitor, self).__init__()
        self.current_function = None

    def visit_ClassDef(self, node: cst.ClassDef) -> Optional[bool]:
        return False  # Don't look for class methods

    def visit_FunctionDef(self, node: cst.FunctionDef) -> Optional[bool]:
        print(f'Visiting function {node.name.value}')
        self.current_function = node
        v = FunctionBodyVisitor()
        node.body.visit(v)
        print(v.foc)
        return False

    def leave_FunctionDef(self, original_node: "FunctionDef") -> None:
        print(f'Leaving function {original_node.name.value}')
        self.current_function = None


class FlowOfControlNode:
    def __init__(self, name, parent):
        self.children = []
        self.name = name
        self.parent = parent

    def __repr__(self):
        return f'({self.name}, {self.children})'

class FlowOfControl:
    def __init__(self):
        self.root = FlowOfControlNode('root', None)
        self.current_node = self.root
        self.depth = 0

    def add_node(self, node: cst.CSTNode):
        node_name = 'EMPTY' if node is None else type(node).__name__
        new_foc_node = FlowOfControlNode(node_name, self.current_node)
        self.current_node.children.append(new_foc_node)
        self.current_node = new_foc_node
        self.depth += 1

    def move_up(self):
        self.current_node = self.current_node.parent
        self.depth -= 1

    def __repr__(self):
        return repr(self.root)

def code_gen(node, compact = False):
    state = CodegenState(
        default_indent=" " if compact else " " * 4, default_newline=' ' if compact else '\n'
    )
    node._codegen(state)
    return "".join(state.tokens)

class FunctionBodyVisitor(cst.CSTVisitor):
    def __init__(self):
        super().__init__()
        self.foc = FlowOfControl()
    #
    # def on_visit(self, node: "CSTNode") -> bool:
    #     print(f'VISIT {code_gen(node, True)}')
    #     return super(FunctionBodyVisitor, self).on_visit(node)

    def visit_ClassDef(self, node: "ClassDef") -> Optional[bool]:
        return False

    def visit_FunctionDef(self, node: "FunctionDef") -> Optional[bool]:
        return False

    def visit_If(self, node: "If") -> Optional[bool]:
        print(f'{" " * self.foc.depth}Visiting If {code_gen(node.test)}')
        self.foc.add_node(node)
        node.body.visit(self)
        return False

    def visit_Else(self, node: "Else") -> Optional[bool]:
        print(f'{" " * self.foc.depth}Visiting Else')
        self.foc.add_node(node)
        return True

    def leave_Else(self, original_node: "Else") -> None:
        self.foc.move_up()
        print(f'{" " * self.foc.depth}Leaving Else')


    def leave_If(self, original_node: "If") -> None:
        self.foc.move_up()
        print(f'{" " * self.foc.depth}Leaving If {code_gen(original_node.test)}')
        if original_node.orelse is not None:
            original_node.orelse.visit(self)
        else:
            self.foc.add_node(None)


if __name__ == "__main__":
    main()
