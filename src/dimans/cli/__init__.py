from collections.abc import Callable
from functools import partial
from typing import NamedTuple

import lark
from lark import Tree
from rich.console import Console
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.command import Provider, Hits, Hit, DiscoveryHit
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.widgets import Header, Footer, Input, TextArea, Label, RichLog, \
    Static

from .parser import parser, evaluator, CalcError, get_canonical_unit, \
    ResultListType, CalcResult, get_longest_name, get_names_overview, \
    CalcOutcome, non_letter_regex, get_name_of_function
from .. import Quantity, Unit, DerivedUnit

try:
    import readline
except ModuleNotFoundError:
    pass


console = Console()
err_console = Console(stderr=True, style="red")


def represent_result(parsed_line, evaled_line) -> str:
    if isinstance(evaled_line, list):
        evaled_line = " + ".join([str(x) for x in evaled_line])
    elif isinstance(evaled_line, Quantity):
        def convert_node_finder(x: lark.Tree):
            if x.data in ("convert", "convertsum"):
                return True
            return False

        convert_nodes = list(parsed_line.find_pred(convert_node_finder))
        if not convert_nodes:
            evaled_line = evaled_line.to(get_canonical_unit(evaled_line))
    return str(evaled_line)


class Results(VerticalScroll):
    def __init__(self) -> None:
        super().__init__()
        self.results: ResultListType = []

    def add_result(self, line: str, parsed: Tree, result: CalcResult):
        self.results.append((line, parsed, result))
        self.mount_all(
            [
                Static(f"r({len(self.results)})", classes="result-id"),
                Static("=", classes="result-eq"),
                Static(
                    line + "\n" + represent_result(parsed, result),
                    classes="result-repr"
                ),
            ],
            before=0
        )

    def compose(self) -> ComposeResult:
        max_result = len(self.results) - 1
        for number, result in enumerate(reversed(self.results)):
            yield Static(f"r({max_result-number})", classes="result-id")
            yield Static("=", classes="result-eq")
            yield Static(
                result[0] + "\n" + represent_result(result[1], result[2]),
                classes="result-repr"
            )


class HistoryInput(Input):
    BINDINGS = [
        Binding("up", "history_back", "history back", show=False),
        Binding("down", "history_forward", "history forward", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = []
        self.history_index = 0

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if not event.value:
            if self.history:
                event.stop()
                self.value = self.history[-1]
                self.post_message(Input.Submitted(self, self.value))
            return
        self.history.append(event.value)
        self.history_index = 0

    def action_history_back(self):
        if self.history_index < len(self.history):
            self.history_index += 1
            self.value = self.history[-self.history_index]
            self.action_end()
        else:
            self.action_home()

    def action_history_forward(self):
        if self.history_index > 0:
            self.history_index -= 1
            if self.history_index == 0:
                self.value = ""
            else:
                self.value = self.history[-self.history_index]
                self.action_end()



class CommandifiedIdent(NamedTuple):
    ident_name: str
    ident_value: CalcOutcome
    help_text: str



class DimansIdents(Provider):
    async def startup(self):
        self.precalculated_list: list[CommandifiedIdent] = [
            CommandifiedIdent(
                ident_name=ident_name,
                ident_value=ident_value,
                help_text=(
                    f"{get_names_overview(ident_value)}\n"
                    f"{DerivedUnit.using(ident_value)}"
                ) if isinstance(ident_value, DerivedUnit) else (
                    f"{get_names_overview(ident_value)}\n"
                    f"{str(ident_value)}"
                )
            )
            for ident_name, ident_value in evaluator.ident_map.items()
        ]

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        if len(matcher.query) < 3:
            return
        app = self.app
        assert isinstance(app, DimansApp)

        for metadata in self.precalculated_list:
            score = matcher.match(metadata.ident_name)

            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(metadata.ident_name),
                    partial(app.action_insert, metadata.ident_name),
                    text=metadata.ident_name,
                    help=metadata.help_text,
                )


                yield Hit(
                    score,
                    matcher.highlight(command_name),
                    partial(app.action_insert, ident_name),
                    text=command_name,
                    help=help_text,
                )


class DimansApp(App):
    TITLE = "Dimans CLI"
    CSS_PATH = "style.tcss"
    COMMANDS = {
        DimansIdents,
    }

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical():
                yield Results()
                yield Label(id="result-label")
                yield HistoryInput(id="line-input")
        yield Footer()

    def on_mount(self):
        self.query_one("#line-input", Input).focus()

    @on(Input.Changed, "#line-input")
    def on_line_input_changed(self, event: Input.Changed):
        in_line = event.input.value
        result_label: Label = self.query_one("#result-label", Label)

        event.input.remove_class("error", "success")
        result_label.remove_class("error")

        if not in_line:
            result_label.update("")
            return

        try:
            parsed_line = parser.parse(in_line)
        except lark.UnexpectedInput as e:
            event.input.add_class("error")
            result_label.add_class("error")
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
                allowed_token_names = set()

            error_message = f"{message}: "
            if len(allowed_token_names) == 1:
                error_message += f"Expected {list(allowed_token_names)[0]}\n"
            else:
                error_message += f"Expected one of:\n"
                ordered_allowed_token_names = list(allowed_token_names)
                ordered_allowed_token_names.sort()
                error_message += ", ".join(ordered_allowed_token_names) + "\n"
            if e.column > 0:
                error_message += (
                    f"{' ' * (e.column - 1)}{'v' * size}\n"
                )
            result_label.update(error_message.strip())
            return

        func_calls = parsed_line.find_data("func")
        for func_call in func_calls:
            func_name = func_call.children[0].value  # type: ignore
            if func_name in ["exit"]:
                event.input.add_class("success")
                result_label.update("<Submitting will exit>")
                return

        try:
            evaled_line = evaluator.transform(parsed_line)
        except lark.exceptions.VisitError as e:
            line_no: int | None
            if isinstance(e.obj, lark.Tree):
                line_no = e.obj.meta.line
                column = e.obj.meta.column
                size = e.obj.meta.end_column - e.obj.meta.column
            else:
                line_no = e.obj.line
                column = e.obj.column or 1
                if e.obj.end_column and e.obj.column:
                    size = e.obj.end_column - e.obj.column
                else:
                    size = 1

            if isinstance(e.orig_exc, CalcError):
                message = e.orig_exc.msg
            elif isinstance(e.orig_exc, OverflowError):
                message = e.orig_exc.args[1]
            else:
                message = str(e.orig_exc)

            error_message = (
                f"{message}\n{' ' * (column - 1)}{'v' * size}"
            )
            result_label.update(error_message)
            return

        event.input.add_class("success")
        result_label.update(represent_result(parsed_line, evaled_line))

    @on(Input.Submitted, "#line-input")
    async def on_line_input_submitted(self, event: Input.Submitted):
        if not event.input.has_class("success"):
            return

        in_line = event.input.value
        try:
            parsed_line = parser.parse(in_line)
        except lark.UnexpectedInput:
            return
        try:
            evaled_line = evaluator.transform(parsed_line)
        except lark.exceptions.VisitError:
            return

        results_container = self.query_one(Results)
        evaluator.results.append((in_line, parsed_line, evaled_line))
        results_container.add_result(in_line, parsed_line, evaled_line)
        event.input.clear()

    def action_insert(self, text: str, forwards: int = None):
        if forwards is None:
            forwards = len(text)
        line_input = self.query_one("#line-input", Input)
        insertion_pos = line_input.cursor_position
        line_input.value = (
            line_input.value[:insertion_pos]
            + text
            + line_input.value[insertion_pos:]
        )
        line_input.cursor_position = insertion_pos + forwards


app = DimansApp()


def main():
    app.run()
