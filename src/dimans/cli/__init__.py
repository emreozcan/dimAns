import lark

from .parser import parser, evaluator, CalcError, get_canonical_unit
from .. import Quantity

prompt = ">>> "
prompt_result = "  = "
prompt_empty = " " * len(prompt)


def main():
    while True:
        in_line = input(prompt)

        try:
            parsed_line = parser.parse(in_line)
        except lark.UnexpectedInput as e:
            line = in_line.splitlines()[e.line - 1]
            if isinstance(e, lark.UnexpectedToken):
                size = max(len(e.token), 1)
                message = f"Unexpected {e.token.type} token {e.token.value!r}"
                allowed_token_names = list(e.accepts or e.expected)
            elif isinstance(e, lark.UnexpectedCharacters):
                size = 1
                message = f"No terminal matches {e.char!r}"
                allowed_token_names = list(e.allowed)
            elif isinstance(e, lark.UnexpectedEOF):
                size = 1
                message = "Unexpected EOF"
                allowed_token_names = [t.type for t in e.expected]
            else:
                size = 1
                message = "Unexpected input"
                allowed_token_names = []
            allowed_token_names.sort()

            print(f"{prompt_empty}{' ' * (e.column - 1)}{'^' * size}")
            print(message)

            if len(allowed_token_names) == 1:
                print(f"Expected {allowed_token_names[0]}")
            else:
                print(f"Expected one of:")
                for allowed_token_name in allowed_token_names:
                    print(f"\t{allowed_token_name}")
            continue

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

            line = in_line.splitlines()[line_no - 1]
            if isinstance(e.orig_exc, CalcError):
                message = e.orig_exc.msg
            elif isinstance(e.orig_exc, OverflowError):
                message = e.orig_exc.args[1]
            else:
                message = str(e.orig_exc)

            print(f"{prompt_empty}{' ' * (column - 1)}{'^' * size}")
            print(message)
            continue

        result_repr = evaled_line
        if isinstance(parsed_line, list):
            result_repr = " + ".join([str(x) for x in parsed_line])
        elif isinstance(parsed_line, Quantity):
            def convert_node_finder(x: lark.Tree):
                if x.data in ("convert", "convertsum"):
                    return True
                return False

            convert_nodes = list(parsed_line.find_pred(convert_node_finder))
            if not convert_nodes:
                result_repr = evaled_line.to(get_canonical_unit(evaled_line))

        print(f"{prompt_result}{result_repr}")
