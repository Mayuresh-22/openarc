from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def print_with_frame(text, color="ansigreen"):
    lines = text.splitlines() or [""]
    width = max(len(line) for line in lines)
    border = f"┌{'─' * (width + 2)}┐"
    bottom = f"└{'─' * (width + 2)}┘"
    print_formatted_text(FormattedText([(color, border)]))
    for line in lines:
        print_formatted_text(FormattedText([(color, "│ ")]), end="")
        print_formatted_text(FormattedText([("white", line.ljust(width))]), end="")
        print_formatted_text(FormattedText([(color, " │")]))
    print_formatted_text(FormattedText([(color, bottom)]), "\n")
