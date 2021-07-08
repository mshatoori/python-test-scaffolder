import re
from typing import Optional

import libcst as cst


class FlowOfControl:
    def __init__(self, name, module_name):
        self.root = FoCRootNode()
        self.name = name
        self.module_name = module_name

    def __repr__(self):
        return f'FoC Tree:\n{repr(self.root)}'


class FoCNode:
    def __init__(self):
        self.parent = None
        self.children = []

    def add_child(self, child: 'FoCNode') -> 'FoCNode':
        child.parent = self
        self.children.append(child)
        return child

    def __repr__(self):
        children_reprs = [f'{repr(c)}' for c in self.children]

        children_reprs_str = '\n'.join(children_reprs)

        if children_reprs_str:
            children_reprs_str = ':\n' + re.sub(r'^', r'=', children_reprs_str, flags=re.M)

        return f'[{self.__class__.__name__}({len(self.children)}){children_reprs_str}]'


class FoCRootNode(FoCNode):
    def __init__(self):
        super(FoCRootNode, self).__init__()


class FoCBranchNode(FoCNode):
    def __init__(self):
        super(FoCBranchNode, self).__init__()
        self.conditions = []
        self.possible_paths = []

    def add_condition(self, condition: Optional[cst.CSTNode]):
        self.conditions.append(condition)


class FoCSplitNode(FoCNode):
    def __init__(self):
        super(FoCSplitNode, self).__init__()
        self.state = 'new'
        self.ifs = []
        self.depth = 0

        self.possible_paths = []

    def add_if(self, if_node: cst.If):
        self.ifs.append(if_node)
        self.depth += 1

    def current_branch(self):
        return self.children[-1]
