from argparse import ArgumentParser, Namespace
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import NamedTuple

import lark
import textual.widgets
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.padding import Padding
from rich.style import Style
from rich.table import Table
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.command import Provider, Hits, Hit, DiscoveryHit
from textual.containers import Horizontal, Vertical, VerticalScroll, Container
from textual.screen import ModalScreen, Screen
from textual.widgets import Header, Footer, Input, TextArea, Label, RichLog, \
    Static, OptionList, Button
from textual.widgets.option_list import Option, Separator

from .parser import parser, evaluator, CalcError, get_canonical_unit, \
    ResultListType, CalcResult, get_longest_name, get_names_overview, \
    CalcOutcome, non_letter_regex, get_name_of_function, function_help_texts, \
    function_help_text_map, get_shortest_name
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

    def add_result(self, line: str, parsed: lark.Tree, result: CalcResult):
        self.results.append((line, parsed, result))
        self.mount_all(
            [
                Static(f"r({len(self.results) - 1})", classes="result-id"),
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
        self.placeholder = event.value

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
    async def startup(self) -> None:
        self.precalculated_list: list[CommandifiedIdent] = [
            CommandifiedIdent(
                ident_name=ident_name,
                ident_value=ident_value,
                help_text=(
                    f"{DerivedUnit.using(ident_value)} "
                    f"({get_shortest_name(ident_value)})"
                ) if isinstance(ident_value, DerivedUnit) else (
                    f"{str(ident_value)} ({get_shortest_name(ident_value)})"
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


class CommandifiedFunction(NamedTuple):
    func_name: str
    func_name_with_args: str
    func_obj: Callable
    help_text: str | None


class DimansFunctions(Provider):
    async def startup(self) -> None:
        self.precalculated_list: list[CommandifiedFunction] = [
            CommandifiedFunction(
                func_name=func_name,
                func_name_with_args=get_name_of_function(func_obj, func_name),
                func_obj=func_obj,
                help_text=function_help_text_map.get(func_name, None)
            )
            for func_name, func_obj in evaluator.func_map.items()
        ]

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, DimansApp)

        for metadata in self.precalculated_list:
            score = matcher.match(metadata.func_name_with_args)

            if score > 0.5:
                yield Hit(
                    score,
                    matcher.highlight(metadata.func_name_with_args),
                    partial(
                        app.action_insert,
                        f"{metadata.func_name}()",
                        len(metadata.func_name) + 1,
                    ),
                    text=metadata.func_name_with_args,
                    help=metadata.help_text,
                )


class Debugger(ModalScreen):
    CSS_PATH = "style/debugger.tcss"

    BINDINGS = [
        Binding("escape", "app.pop_screen", "close debugger"),
    ]

    @classmethod
    def is_open(cls, app: App) -> bool:
        return type(app.screen) is cls

    def compose(self) -> ComposeResult:
        app = self.app
        assert isinstance(app, DimansApp)
        input_element = app.screen_stack[0].query_one(HistoryInput)
        if not input_element.history:
            error_container = Container(id="error-container")
            error_container.border_title = "Debugger Error"
            with error_container:
                yield Label("No history to debug")
                with Container(id="button-container"):
                    yield Button("Close",
                                 id="close-debugger",
                                 classes="-error")
            return
        last_input = input_element.history[-1]
        debugger_container = Container(id="debugger-container")
        debugger_container.border_title = "Debugger"
        with debugger_container:
            ui_tree: textual.widgets.Tree
            ui_tree = textual.widgets.Tree(label=f"<Final result>")
            parse_tree = parser.parse(last_input)
            self.recurse_tree(parse_tree, ui_tree.root, last_input)
            ui_tree.root.expand()
            yield ui_tree

    def recurse_tree(
        self,
        parse_node: lark.Tree | lark.Token,
        ui_node: textual.widgets._tree.TreeNode,
        line: str,
    ):
        if isinstance(parse_node, lark.Tree):
            node_value = evaluator.transform(parse_node)
            t = line[parse_node.meta.column - 1:parse_node.meta.end_column - 1]
            new_node = ui_node.add(repr(t))
            new_node.add_leaf(f"{parse_node.data}")
            for child in parse_node.children:
                self.recurse_tree(child, new_node, line)
            new_node.add_leaf(f"Result: {node_value}")
        elif isinstance(parse_node, lark.Token):
            ui_node.add_leaf(f"Terminal {parse_node.type}: "
                             f"{parse_node.value!r}")

    @on(Button.Pressed, "#close-debugger")
    def on_close_debugger(self):
        self.app.pop_screen()


class FunctionSelector(ModalScreen):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "close function selector"),
    ]

    @classmethod
    def is_open(cls, app: App) -> bool:
        return type(app.screen) is cls

    def compose(self) -> ComposeResult:
        yield OptionList(id="function-list")

    @staticmethod
    def get_option_from_function(
        *,
        func_name: str,
        func_obj: Callable,
        func_help: str,
    ) -> Option:
        function_with_signature = get_name_of_function(func_obj, func_name)

        return Option(
            prompt=Group(
                Text(
                    function_with_signature,
                    Style(
                        color="#FFA800",
                        bold=True,
                    ),
                ),
                Markdown(f"{func_help}", style=Style(italic=True)),
                Text(),
            ),
            id=func_name,
        )

    def on_mount(self):
        function_list = self.query_one(OptionList)
        skipped_first_separator = False
        for category, functions in function_help_texts.items():
            if skipped_first_separator:
                function_list.add_option(Separator())
            skipped_first_separator = True
            function_list.add_option(
                Option(
                    prompt=Text(category, Style(bold=True)),
                    disabled=True,
                )
            )
            function_list.add_options([
                self.get_option_from_function(
                    func_name=func_name,
                    func_obj=evaluator.func_map[func_name],
                    func_help=func_help,
                )
                for func_name, func_help in functions.items()
            ])

    @on(OptionList.OptionSelected, "#function-list")
    def on_function_selected(self, event: OptionList.OptionSelected):
        app = self.app
        assert isinstance(app, DimansApp)
        app.pop_screen()
        app.action_insert(f"{event.option.id}()", -1)


class DimansApp(App):
    TITLE = "Dimans CLI"
    CSS_PATH = "style/app.tcss"
    COMMANDS = {
        DimansIdents,
        DimansFunctions
    }
    BINDINGS = [
        Binding("f1", "show_function_selector", "function selector"),
        Binding("f2", "show_debugger", "debugger"),
        Binding("escape", "keyboard_interrupt", "back", show=False),
        Binding("ctrl+c", "keyboard_interrupt", "back", show=False),
        Binding("ctrl+q", "quit", "quit", show=True, priority=True),
    ]

    def __init__(self):
        super().__init__()

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

    def action_insert(self, text: str, forwards: int | None = None):
        if forwards is None:
            forwards = len(text)
        line_input = self.query_one("#line-input", Input)
        insertion_pos = line_input.cursor_position
        line_input.value = (
            line_input.value[:insertion_pos]
            + text
            + line_input.value[insertion_pos:]
        )
        if forwards > 0:
            line_input.cursor_position = insertion_pos + forwards
        else:
            line_input.cursor_position = insertion_pos + len(text) - forwards

    def action_show_function_selector(self):
        self.push_screen(FunctionSelector())

    def action_show_debugger(self):
        self.push_screen(Debugger())

    async def action_keyboard_interrupt(self) -> None:
        if self.screen_stack[-1].id != "_default":
            await self.action_back()
        else:
            input = self.query_one(HistoryInput)
            with input.prevent(Input.Changed):
                input.clear()
            input.remove_class("error", "success")
            label = self.query_one("#result-label", Label)
            label.remove_class("error")
            label.update("<KeyboardInterrupt>")


app = DimansApp()


arg_parser = ArgumentParser(description="dimAns Calculator CLI")
arg_parser.add_argument("--profile", action="store_true", help="Profile the app")
arg_parser.add_argument("--profile-file", type=Path, metavar="FILE",
                        help="File to dump the profile stats to")
arg_parser.add_argument("--list-functions", action="store_true",
                        help="List all functions and exit")


def main():
    args = arg_parser.parse_args()

    if args.profile:
        import cProfile
        with cProfile.Profile() as pr:
            run(args)
            pr.dump_stats(args.profile_file or "profile.stats")
    else:
        run(args)


def run(args: Namespace):
    if args.list_functions:
        for category, functions in function_help_texts.items():
            console.print(Text(f"{category}", style="bold"))
            for func_name, func_help in functions.items():
                func_obj = evaluator.func_map[func_name]
                signature = get_name_of_function(func_obj, func_name)
                console.print(Text(f"  {signature}", style="#FFA800"))
                console.print(
                    Padding(
                        Markdown(func_help, style="italic"),
                        pad=(0, 0, 0, 4),
                    )
                )
            console.print()
        exit(0)
    app.run()
