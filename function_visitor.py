from typing import List, Optional

import libcst as cst

from flow_of_control import FlowOfControl, FoCSplitNode, FoCBranchNode
from utils import code_gen


class FunctionVisitor(cst.CSTVisitor):
    def __init__(self, node: cst.FunctionDef):
        super().__init__()
        self.func = node
        self.foc = FlowOfControl(node.name.value)
        self.split_node_stack: List[FoCSplitNode] = []

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
            if_split_node = FoCSplitNode(node)
            self.split_node_stack.append(if_split_node)
        else:
            assert top_split.state == 'or_else'
            top_split.add_if(node)

        if top_split:
            print(f'depth={top_split.depth}')

        return True

    def visit_If_body(self, node: "If") -> None:
        print(f'Visiting if body {code_gen(node.test)}')
        top_split = self.top_split_node()

        if top_split:
            print(f'depth={top_split.depth}')

        top_split.add_child(FoCBranchNode(node.test))
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
            condition = cst.UnaryOperation(
                operator=cst.Not(),
                expression=top_split.ifs[0].test,
            )

            for _if in top_split.ifs[1:]:
                condition = cst.BooleanOperation(
                    left=condition,
                    operator=cst.And(),
                    right=cst.UnaryOperation(
                        operator=cst.Not(),
                        expression=_if.test,
                    )
                )

            top_split.add_child(FoCBranchNode(condition))

    def visit_Else_body(self, node: "Else") -> None:
        print(f'Visiting Else body')

        top_split = self.top_split_node()
        condition = cst.UnaryOperation(
            operator=cst.Not(),
            expression=top_split.ifs[0].test,
        )

        for _if in top_split.ifs[1:]:
            condition = cst.BooleanOperation(
                left=condition,
                operator=cst.And(),
                right=cst.UnaryOperation(
                    operator=cst.Not(),
                    expression=_if.test,
                )
            )
        top_split.add_child(FoCBranchNode(condition))

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

            next_top_split = self.top_split_node()

            if next_top_split is None:
                parent = self.foc.root
            else:
                parent = next_top_split.current_branch()

            parent.add_child(split_node)
        else:
            top_split.depth -= 1

    def log_foc_tree(self):
        print(self.foc)
