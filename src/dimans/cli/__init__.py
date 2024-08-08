try:
    import readline
except ModuleNotFoundError:
    pass

import lark
from rich.console import Console

from .parser import parser, evaluator, CalcError, get_canonical_unit
from .. import Quantity

prompt = ""
prompt_res = ""
prompt_pre = " " * len(prompt)


console = Console()
err_console = Console(stderr=True, style="red")


def read_and_process_line():
    in_line = console.input(prompt=prompt)

    try:
        parsed_line = parser.parse(in_line)
    except lark.UnexpectedInput as e:
        if isinstance(e, lark.UnexpectedToken):
            size = max(len(e.token), 1)
            message = f"Unexpected {e.token.type} token {e.token.value!r}"
            allowed_token_names = e.accepts | e.expected
        elif isinstance(e, lark.UnexpectedCharacters):
            size = 1
            message = f"No terminal matches {e.char!r}"
            allowed_token_names = e.allowed
        elif isinstance(e, lark.UnexpectedEOF):
            size = 1
            message = "Unexpected EOF"
            allowed_token_names = {t for t in e.expected}
        else:
            size = 1
            message = "Unexpected input"
            allowed_token_names = []
        allowed_token_names = list(allowed_token_names)
        allowed_token_names.sort()

        if e.column > 0:
            err_console.print(f"{prompt_pre}{' ' * (e.column - 1)}{'^' * size}")
        err_console.print(message)

        if len(allowed_token_names) == 1:
            err_console.print(f"Expected {allowed_token_names[0]}")
        else:
            err_console.print(f"Expected one of:")
            for allowed_token_name in allowed_token_names:
                err_console.print(f"\t{allowed_token_name}")
        return

    try:
        evaled_line = evaluator.transform(parsed_line)
    except lark.exceptions.VisitError as e:
        if isinstance(e.obj, lark.Tree):
            line_no = e.obj.meta.line
            column = e.obj.meta.column
            size = e.obj.meta.end_column - e.obj.meta.column
        else:
            line_no = e.obj.line
            column = e.obj.column
            size = e.obj.end_column - e.obj.column

        if isinstance(e.orig_exc, CalcError):
            message = e.orig_exc.msg
        elif isinstance(e.orig_exc, OverflowError):
            message = e.orig_exc.args[1]
        else:
            message = str(e.orig_exc)

        err_console.print(f"{prompt_pre}{' ' * (column - 1)}{'^' * size}")
        err_console.print(message)
        return

    result_repr = evaled_line
    if isinstance(evaled_line, list):
        result_repr = " + ".join([str(x) for x in evaled_line])
    elif isinstance(evaled_line, Quantity):
        def convert_node_finder(x: lark.Tree):
            if x.data in ("convert", "convertsum"):
                return True
            return False

        convert_nodes = list(parsed_line.find_pred(convert_node_finder))
        if not convert_nodes:
            result_repr = evaled_line.to(get_canonical_unit(evaled_line))

    console.print(f"{prompt_res}{result_repr}")


def main():
    while True:
        read_and_process_line()
