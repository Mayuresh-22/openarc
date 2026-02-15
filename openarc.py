from prompt_toolkit import HTML, print_formatted_text, prompt
from src.core.handler.get_input_handler import get_input_handler
from src.core.router.router import InputRouter


def loop():
    while True:
        user_input = prompt(">>> ", complete_while_typing=True)
        if user_input.strip().lower() in ["exit"]:
            exit(0)
        input_type = InputRouter().route_input(user_input)
        print_formatted_text(HTML(f"<grey>Input Type: {input_type.input_type}, Content: {input_type.content}</grey>"))

        handler = get_input_handler(input_type.input_type)
        result = handler.handle(input_type.content)

        print_formatted_text(result.stdout)


def main():
    loop()


if __name__ == "__main__":
    main()
