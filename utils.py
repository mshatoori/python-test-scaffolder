from libcst._nodes.internal import CodegenState


def code_gen(node, compact=False):
    state = CodegenState(
        default_indent=" " if compact else " " * 4, default_newline=' ' if compact else '\n'
    )
    node._codegen(state)
    return "".join(state.tokens)