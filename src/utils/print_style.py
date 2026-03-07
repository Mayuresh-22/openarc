from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


cli_style = Style.from_dict({
    'input': 'bold #00BCD4',
    'output': '#FFFFFF',
    'output-bold': 'bold #FFFFFF',
    'progress': 'italic #FFD700',
    'confirm': 'bold #E040FB',
    'error': 'bold #FF5252',
    'warning': 'bold #FF9800',
    'success': 'bold #4CAF50',
    'header': 'bold underline #2196F3',
    'agent': 'italic #9C27B0',
    'code': '#B0BEC5',
    'feedback-success': 'bold #4CAF50',
    'feedback-info': 'bold #2196F3',
    'feedback-warning': 'bold #FFD700',
})


def print_with_frame(text, color="ansigreen", style=cli_style):
    lines = text.splitlines() or [""]
    width = max(len(line) for line in lines)
    border = f"┌{'─' * (width + 2)}┐"
    bottom = f"└{'─' * (width + 2)}┘"
    print_formatted_text(FormattedText([(color, border)]), style=style)
    for line in lines:
        print_formatted_text(FormattedText([(color, "│ ")]), end="", style=style)
        print_formatted_text(FormattedText([("white", line.ljust(width))]), end="", style=style)
        print_formatted_text(FormattedText([(color, " │")]), style=style)
    print_formatted_text(FormattedText([(color, bottom)]), "\n", style=style)
