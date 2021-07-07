from typing import Optional, List

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
        return True

    def visit_FunctionDef_body(self, node: "FunctionDef") -> None:
        print(f'Visiting function body {node.name.value}')
        v = FunctionBodyVisitor()
        node.body.visit(v)

    def leave_FunctionDef(self, original_node: "FunctionDef") -> None:
        print(f'Leaving function {original_node.name.value}')
        self.current_function = None


class FoCNode:
    def __init__(self, parent: Optional['FoCNode']):
        self.parent = parent


class FoCRootNode(FoCNode):
    def __init__(self):
        super(FoCRootNode, self).__init__(None)


class FlowOfControl:
    def __init__(self):
        self.root = FoCRootNode()

    def __repr__(self):
        return repr(self.root)


def code_gen(node, compact=False):
    state = CodegenState(
        default_indent=" " if compact else " " * 4, default_newline=' ' if compact else '\n'
    )
    node._codegen(state)
    return "".join(state.tokens)


class FoCBranchNode(FoCNode):
    def __init__(self, parent: Optional[FoCNode]):
        super(FoCBranchNode, self).__init__(parent)


class FoCSplitNode(FoCNode):
    def __init__(self, parent: Optional[FoCNode]):
        super(FoCSplitNode, self).__init__(parent)
        self.branches = []
        self.state = 'new'
        self.depth = 0

    def add_branch(self, node: Optional[cst.CSTNode]) -> FoCBranchNode:
        branch = FoCBranchNode(self)
        self.branches.append(branch)
        return branch

    def current_branch(self):
        return self.branches[-1]


class FunctionBodyVisitor(cst.CSTVisitor):
    def __init__(self):
        super().__init__()
        self.foc = FlowOfControl()
        self.split_node_stack: List[FoCSplitNode] = []
        self.current_node = self.foc.root
        self.chained_if_else_number = 0

    def top_split_node(self) -> Optional[FoCSplitNode]:
        if self.split_node_stack:
            return self.split_node_stack[-1]
        return None

    def visit_ClassDef(self, node: "ClassDef") -> Optional[bool]:
        return False

    def visit_FunctionDef(self, node: "FunctionDef") -> Optional[bool]:
        return False

    def visit_If(self, node: "If") -> Optional[bool]:
        print(f'Visiting if {code_gen(node.test)}')

        top_split = self.top_split_node()

        if top_split is None or top_split.state == 'in_body':
            parent = None
            if top_split is not None:
                parent = top_split.current_branch()

            if_split_node = FoCSplitNode(parent)
            self.split_node_stack.append(if_split_node)
        else:
            assert top_split.state == 'or_else'
            top_split.depth += 1


        if top_split:
            print(f'depth={top_split.depth}')

        return True

    def visit_If_body(self, node: "If") -> None:
        print(f'Visiting if body {code_gen(node.test)}')
        top_split = self.top_split_node()


        if top_split:
            print(f'depth={top_split.depth}')

        top_split.add_branch(node.body)
        top_split.state = 'in_body'

    def leave_If_body(self, node: "If") -> None:
        print(f'Leaving if body {code_gen(node.test)}')

    def visit_If_orelse(self, node: "If") -> None:
        print(f'Visiting if orelse {code_gen(node.orelse) if node.orelse else "EMPTY"}')

        top_split = self.top_split_node()
        top_split.state = 'or_else'


        if top_split:
            print(f'depth={top_split.depth}')

        if node.orelse is None:
            top_split.add_branch(node.orelse)
        elif isinstance(node.orelse, cst.If):
            pass
        elif isinstance(node.orelse, cst.Else):
            branch = self.split_node_stack[-1].add_branch(node.orelse)

    def leave_If_orelse(self, node: "If") -> None:
        print(f'Leaving if orelse {code_gen(node.orelse) if node.orelse else "EMPTY"}')
        top_split = self.top_split_node()
        top_split.state = 'done'


        if top_split:
            print(f'depth={top_split.depth}')

    def leave_If(self, original_node: "If") -> None:
        print(f'Leaving if {code_gen(original_node.test)}')

        top_split = self.top_split_node()
        assert top_split.state == 'done'


        if top_split:
            print(f'depth={top_split.depth}')

        if top_split.depth == 0:
            split_node = self.split_node_stack.pop()
            # todo: add this split node to the tree
            print(f'DELETE HERE: {len(split_node.branches)}')
        else:
            top_split.depth -= 1


if __name__ == "__main__":
    main()
