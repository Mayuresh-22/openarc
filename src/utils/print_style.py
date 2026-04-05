from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()


CLI_COLORS = {
    # Core palette (blue-first system)
    "input": "bold bright_blue",
    "output": "white",
    "output-bold": "bold white",

    "progress": "italic bright_blue",
    "system": "bold bright_blue",
    "system-muted": "grey62",

    "confirm": "bold cyan",
    "error": "bold red3",
    "warning": "bold yellow3",
    "success": "bold green3",

    "header": "bold underline bright_blue",
    "agent": "italic cyan",

    # Code + surfaces
    "code": "cyan on grey11",

    # Feedback
    "feedback-success": "bold green3",
    "feedback-info": "bold bright_blue",
    "feedback-warning": "bold yellow3",
}

# Panel / border styling
PANEL_BORDER = "bright_blue"
PANEL_BORDER_DIM = "grey35"
PANEL_TITLE_STYLE = "bold bright_blue"

box_map = {
    "round": box.ROUNDED,
    "rounded": box.ROUNDED,
    "square": box.SQUARE,
    "ascii": box.ASCII,
    "double": box.DOUBLE,
    "minimal": box.MINIMAL,
    "heavy": box.HEAVY,
    "simple": box.SIMPLE,
    "horizontals": box.HORIZONTALS,
}


def print_with_frame(text, color="blue", style="output", title=None, box_style="round"):
    """Print text in a professional blue TUI frame using rich Panel."""

    box_obj = box_map.get(box_style, box.ROUNDED)

    panel = Panel(
        Text(text, style=CLI_COLORS.get(style, style)),
        box=box_obj,
        border_style=PANEL_BORDER,
        padding=(0, 1),
        title=Text(title, style=PANEL_TITLE_STYLE) if title else None,
    )

    console.print(panel)


def print_system_message(text: str):
    console.print(
        Text("● ", style=CLI_COLORS["system"]) +
        Text(text, style=CLI_COLORS["system"])
    )


def print_system_detail(label: str, value: str):
    label_text = Text(label + ": ", style="bright_blue")
    value_text = Text(value, style=CLI_COLORS["system-muted"])
    console.print(label_text.append(value_text))


def print_stream_chunk(
    text: str,
    style="cyan",
    box_style="round",
    title=None,
    is_code=False,
    is_markdown=False
):
    """
    Print a chunk of output in a styled TUI panel.
    - style: main text color (default cyan)
    - box_style: panel border style (str or Box)
    - title: optional panel title
    - is_code: render as code block
    - is_markdown: render as markdown
    """

    # Markdown block (rich + framed)
    if is_markdown:
        md = Markdown(text)
        console.print(
            Panel(
                md,
                border_style=PANEL_BORDER,
                padding=(0, 1),
                title=Text(title, style=PANEL_TITLE_STYLE) if title else None,
            )
        )

    # Code block (highlighted + strong border)
    elif is_code:
        code_text = Text(text, style=CLI_COLORS["code"])
        console.print(
            Panel(
                code_text,
                border_style="bright_blue",
                padding=(0, 1),
                title=Text(title or "Code", style=PANEL_TITLE_STYLE),
            )
        )

    # Streaming inline text (no panel)
    else:
        main_text = Text(text, style=CLI_COLORS.get("output", style))
        console.print(main_text, end="")

