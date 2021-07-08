import itertools

from libcst import *

from flow_of_control import FlowOfControl, FoCNode, FoCBranchNode, FoCSplitNode
from utils import code_gen


class TestGenerator:
    def __init__(self, foc: FlowOfControl):
        self.foc = foc

    def _process_foc_node(self, node: FoCNode):
        possible_paths = []

        if isinstance(node, FoCSplitNode):
            for ch in node.children:
                possible_paths.extend(self._process_foc_node(ch))
        else:
            node_conditions = []

            if isinstance(node, FoCBranchNode):
                node_conditions = node.conditions

                if len(node.children) == 0:
                    return [node_conditions]

            split_paths = []
            for ch in node.children:
                split_paths.append(self._process_foc_node(ch))

            for incomplete_path in itertools.product(*split_paths):
                path = []

                if node_conditions:
                    path.extend(node_conditions)

                for conditions in incomplete_path:
                    path.extend(conditions)

                possible_paths.append(path)

        return possible_paths

    def _generate_function_for_conditions(self, func_name: str, test_index: int, conditions: list) -> FunctionDef:
        conditions_help_str = f'"""This test function tests {func_name}'

        if conditions:
            conditions_help_str += ' when these conditions are met:\n'

            for c in conditions:
                conditions_help_str += f'        - {code_gen(c)}\n'

            conditions_help_str += '        '

        conditions_help_str += '"""'

        return FunctionDef(
            name=Name(
                value=f'test_{func_name}_{test_index}',
            ),
            params=Parameters(
                params=[
                    Param(
                        name=Name(
                            value='self',
                        ),
                    ),
                ],
            ),
            body=IndentedBlock(
                body=[
                    SimpleStatementLine(
                        body=[
                            Expr(
                                value=SimpleString(
                                    value=conditions_help_str,
                                ),
                            ),
                        ],
                    ),
                    SimpleStatementLine(
                        body=[
                            Assign(
                                targets=[
                                    AssignTarget(
                                        target=Name(
                                            value='in_out_list',
                                        ),
                                    ),
                                ],
                                value=List(
                                    elements=[],
                                    lbracket=LeftSquareBracket(
                                        whitespace_after=ParenthesizedWhitespace(
                                            first_line=TrailingWhitespace(
                                                whitespace=SimpleWhitespace(
                                                    value='',
                                                ),
                                                comment=None,
                                                newline=Newline(
                                                    value=None,
                                                ),
                                            ),
                                            empty_lines=[
                                                EmptyLine(
                                                    indent=True,
                                                    whitespace=SimpleWhitespace(
                                                        value='    ',
                                                    ),
                                                    comment=Comment(
                                                        value='# TODO: Fill with input output pairs in form of "((args, kwargs), return_val)"',
                                                    ),
                                                    newline=Newline(
                                                        value=None,
                                                    ),
                                                ),
                                                EmptyLine(
                                                    indent=True,
                                                    whitespace=SimpleWhitespace(
                                                        value='    ',
                                                    ),
                                                    comment=Comment(
                                                        value='# TODO: These values should cover all edge cases and stuff...',
                                                    ),
                                                    newline=Newline(
                                                        value=None,
                                                    ),
                                                ),
                                            ],
                                            indent=True,
                                            last_line=SimpleWhitespace(
                                                value='',
                                            ),
                                        ),
                                    ),
                                    rbracket=RightSquareBracket(
                                        whitespace_before=SimpleWhitespace(
                                            value='',
                                        ),
                                    ),
                                    lpar=[],
                                    rpar=[],
                                ),
                                semicolon=MaybeSentinel.DEFAULT,
                            ),
                        ],
                        leading_lines=[
                            EmptyLine(
                                indent=False,
                                whitespace=SimpleWhitespace(
                                    value='',
                                ),
                                comment=None,
                                newline=Newline(
                                    value=None,
                                ),
                            ),
                        ],
                        trailing_whitespace=TrailingWhitespace(
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                            comment=None,
                            newline=Newline(
                                value=None,
                            ),
                        ),
                    ),
                    For(
                        target=Tuple(
                            elements=[
                                Element(
                                    value=Tuple(
                                        elements=[
                                            Element(
                                                value=Name(
                                                    value='args',
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                comma=Comma(
                                                    whitespace_before=SimpleWhitespace(
                                                        value='',
                                                    ),
                                                    whitespace_after=SimpleWhitespace(
                                                        value=' ',
                                                    ),
                                                ),
                                            ),
                                            Element(
                                                value=Name(
                                                    value='kwargs',
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                comma=MaybeSentinel.DEFAULT,
                                            ),
                                        ],
                                        lpar=[
                                            LeftParen(
                                                whitespace_after=SimpleWhitespace(
                                                    value='',
                                                ),
                                            ),
                                        ],
                                        rpar=[
                                            RightParen(
                                                whitespace_before=SimpleWhitespace(
                                                    value='',
                                                ),
                                            ),
                                        ],
                                    ),
                                    comma=Comma(
                                        whitespace_before=SimpleWhitespace(
                                            value='',
                                        ),
                                        whitespace_after=SimpleWhitespace(
                                            value=' ',
                                        ),
                                    ),
                                ),
                                Element(
                                    value=Name(
                                        value='return_val',
                                        lpar=[],
                                        rpar=[],
                                    ),
                                    comma=MaybeSentinel.DEFAULT,
                                ),
                            ],
                            lpar=[],
                            rpar=[],
                        ),
                        iter=Name(
                            value='in_out_list',
                            lpar=[],
                            rpar=[],
                        ),
                        body=IndentedBlock(
                            body=[
                                SimpleStatementLine(
                                    body=[
                                        Assign(
                                            targets=[
                                                AssignTarget(
                                                    target=Name(
                                                        value='real_return_val',
                                                        lpar=[],
                                                        rpar=[],
                                                    ),
                                                    whitespace_before_equal=SimpleWhitespace(
                                                        value=' ',
                                                    ),
                                                    whitespace_after_equal=SimpleWhitespace(
                                                        value=' ',
                                                    ),
                                                ),
                                            ],
                                            value=Call(
                                                func=Name(
                                                    value=func_name,
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                args=[
                                                    Arg(
                                                        value=Name(
                                                            value='args',
                                                            lpar=[],
                                                            rpar=[],
                                                        ),
                                                        keyword=None,
                                                        equal=MaybeSentinel.DEFAULT,
                                                        comma=Comma(
                                                            whitespace_before=SimpleWhitespace(
                                                                value='',
                                                            ),
                                                            whitespace_after=SimpleWhitespace(
                                                                value=' ',
                                                            ),
                                                        ),
                                                        star='*',
                                                        whitespace_after_star=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                        whitespace_after_arg=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                    ),
                                                    Arg(
                                                        value=Name(
                                                            value='kwargs',
                                                            lpar=[],
                                                            rpar=[],
                                                        ),
                                                        keyword=None,
                                                        equal=MaybeSentinel.DEFAULT,
                                                        comma=MaybeSentinel.DEFAULT,
                                                        star='**',
                                                        whitespace_after_star=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                        whitespace_after_arg=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                    ),
                                                ],
                                                lpar=[],
                                                rpar=[],
                                                whitespace_after_func=SimpleWhitespace(
                                                    value='',
                                                ),
                                                whitespace_before_args=SimpleWhitespace(
                                                    value='',
                                                ),
                                            ),
                                            semicolon=MaybeSentinel.DEFAULT,
                                        ),
                                    ],
                                    leading_lines=[],
                                    trailing_whitespace=TrailingWhitespace(
                                        whitespace=SimpleWhitespace(
                                            value='',
                                        ),
                                        comment=None,
                                        newline=Newline(
                                            value=None,
                                        ),
                                    ),
                                ),
                                SimpleStatementLine(
                                    body=[
                                        Expr(
                                            value=Call(
                                                func=Attribute(
                                                    value=Name(
                                                        value='self',
                                                        lpar=[],
                                                        rpar=[],
                                                    ),
                                                    attr=Name(
                                                        value='assertEqual',
                                                        lpar=[],
                                                        rpar=[],
                                                    ),
                                                    dot=Dot(
                                                        whitespace_before=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                        whitespace_after=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                    ),
                                                    lpar=[],
                                                    rpar=[],
                                                ),
                                                args=[
                                                    Arg(
                                                        value=Name(
                                                            value='return_val',
                                                            lpar=[],
                                                            rpar=[],
                                                        ),
                                                        keyword=None,
                                                        equal=MaybeSentinel.DEFAULT,
                                                        comma=Comma(
                                                            whitespace_before=SimpleWhitespace(
                                                                value='',
                                                            ),
                                                            whitespace_after=SimpleWhitespace(
                                                                value=' ',
                                                            ),
                                                        ),
                                                        star='',
                                                        whitespace_after_star=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                        whitespace_after_arg=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                    ),
                                                    Arg(
                                                        value=Name(
                                                            value='real_return_val',
                                                            lpar=[],
                                                            rpar=[],
                                                        ),
                                                        keyword=None,
                                                        equal=MaybeSentinel.DEFAULT,
                                                        comma=MaybeSentinel.DEFAULT,
                                                        star='',
                                                        whitespace_after_star=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                        whitespace_after_arg=SimpleWhitespace(
                                                            value='',
                                                        ),
                                                    ),
                                                ],
                                                lpar=[],
                                                rpar=[],
                                                whitespace_after_func=SimpleWhitespace(
                                                    value='',
                                                ),
                                                whitespace_before_args=SimpleWhitespace(
                                                    value='',
                                                ),
                                            ),
                                            semicolon=MaybeSentinel.DEFAULT,
                                        ),
                                    ],
                                    leading_lines=[],
                                    trailing_whitespace=TrailingWhitespace(
                                        whitespace=SimpleWhitespace(
                                            value='',
                                        ),
                                        comment=None,
                                        newline=Newline(
                                            value=None,
                                        ),
                                    ),
                                ),
                            ],
                            header=TrailingWhitespace(
                                whitespace=SimpleWhitespace(
                                    value='',
                                ),
                                comment=None,
                                newline=Newline(
                                    value=None,
                                ),
                            ),
                            indent=None,
                            footer=[],
                        ),
                        orelse=None,
                        asynchronous=None,
                        leading_lines=[
                            EmptyLine(
                                indent=False,
                                whitespace=SimpleWhitespace(
                                    value='',
                                ),
                                comment=None,
                                newline=Newline(
                                    value=None,
                                ),
                            ),
                        ],
                        whitespace_after_for=SimpleWhitespace(
                            value=' ',
                        ),
                        whitespace_before_in=SimpleWhitespace(
                            value=' ',
                        ),
                        whitespace_after_in=SimpleWhitespace(
                            value=' ',
                        ),
                        whitespace_before_colon=SimpleWhitespace(
                            value='',
                        ),
                    ),
                ],
                header=TrailingWhitespace(
                    whitespace=SimpleWhitespace(
                        value='',
                    ),
                    comment=None,
                    newline=Newline(
                        value=None,
                    ),
                ),
                indent=None,
                footer=[],
            ),
            decorators=[],
            returns=None,
            asynchronous=None,
            leading_lines=[
                EmptyLine(
                    indent=False,
                    whitespace=SimpleWhitespace(
                        value='',
                    ),
                    comment=None,
                    newline=Newline(
                        value=None,
                    ),
                ),
            ] if test_index else [],
            lines_after_decorators=[],
            whitespace_after_def=SimpleWhitespace(
                value=' ',
            ),
            whitespace_after_name=SimpleWhitespace(
                value='',
            ),
            whitespace_before_params=SimpleWhitespace(
                value='',
            ),
            whitespace_before_colon=SimpleWhitespace(
                value='',
            ),
        )

    def _generate_functions(self):
        functions = []

        possible_paths = self._process_foc_node(self.foc.root)
        for idx, path in enumerate(possible_paths):
            print(f'!!!! {[code_gen(c) for c in path]}')

            functions.append(
                self._generate_function_for_conditions(
                    func_name=self.foc.name,
                    test_index=idx,
                    conditions=path,
                )
            )

        return functions

    def _generate_module(self) -> Module:
        test_functions = self._generate_functions()

        func_name = self.foc.name
        module_name = self.foc.module_name

        return Module(
            body=[
                SimpleStatementLine(
                    body=[
                        Import(
                            names=[
                                ImportAlias(
                                    name=Name(
                                        value='unittest',
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                SimpleStatementLine(
                    body=[
                        ImportFrom(
                            module=Name(
                                value=module_name,
                                lpar=[],
                                rpar=[],
                            ),
                            names=[
                                ImportAlias(
                                    name=Name(
                                        value=func_name,
                                        lpar=[],
                                        rpar=[],
                                    ),
                                    asname=None,
                                    comma=MaybeSentinel.DEFAULT,
                                ),
                            ],
                            relative=[],
                            lpar=None,
                            rpar=None,
                            semicolon=MaybeSentinel.DEFAULT,
                            whitespace_after_from=SimpleWhitespace(
                                value=' ',
                            ),
                            whitespace_before_import=SimpleWhitespace(
                                value=' ',
                            ),
                            whitespace_after_import=SimpleWhitespace(
                                value=' ',
                            ),
                        ),
                    ],
                    leading_lines=[
                        EmptyLine(
                            indent=True,
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                            comment=None,
                            newline=Newline(
                                value=None,
                            ),
                        ),
                    ],
                    trailing_whitespace=TrailingWhitespace(
                        whitespace=SimpleWhitespace(
                            value='',
                        ),
                        comment=None,
                        newline=Newline(
                            value=None,
                        ),
                    ),
                ),
                ClassDef(
                    name=Name(
                        value='MyTestCase',
                    ),
                    body=IndentedBlock(
                        body=test_functions,
                    ),
                    bases=[
                        Arg(
                            value=Attribute(
                                value=Name(
                                    value='unittest',
                                ),
                                attr=Name(
                                    value='TestCase',
                                ),
                            ),
                        ),
                    ],
                    leading_lines=[
                        EmptyLine(
                            indent=True,
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                            comment=None,
                            newline=Newline(
                                value=None,
                            ),
                        ),
                        EmptyLine(
                            indent=True,
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                            comment=None,
                            newline=Newline(
                                value=None,
                            ),
                        ),
                    ],
                ),
                If(
                    test=Comparison(
                        left=Name(
                            value='__name__',
                        ),
                        comparisons=[
                            ComparisonTarget(
                                operator=Equal(),
                                comparator=SimpleString(
                                    value="'__main__'",
                                ),
                            ),
                        ],
                    ),
                    body=IndentedBlock(
                        body=[
                            SimpleStatementLine(
                                body=[
                                    Expr(
                                        value=Call(
                                            func=Attribute(
                                                value=Name(
                                                    value='unittest',
                                                ),
                                                attr=Name(
                                                    value='main',
                                                ),
                                            ),
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                    leading_lines=[
                        EmptyLine(
                            indent=True,
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                            comment=None,
                            newline=Newline(
                                value=None,
                            ),
                        ),
                        EmptyLine(
                            indent=True,
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                            comment=None,
                            newline=Newline(
                                value=None,
                            ),
                        ),
                    ],
                ),
            ],
        )

    def generate(self) -> str:
        test_module = self._generate_module()

        return test_module.code
