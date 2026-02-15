from pydantic import BaseModel


class InputType(BaseModel):
    input_type: str
    content: list[str] = []


class InputRouter:
    def route_input(self, input_string: str) -> InputType:
        if input_string.startswith("!"):
            return InputType(
                input_type="shell",
                content=self.sanitize_shell_command(input_string[1:]),
            )
        elif input_string.startswith("/"):
            return InputType(
                input_type="arc_command",
                content=[self.sanitize_arc_command(input_string[1:])],
            )
        else:
            return InputType(input_type="arc_query", content=[input_string])

    def sanitize_input(self, input_string: str) -> str:
        return input_string.strip()

    def sanitize_shell_command(self, command: str) -> list[str]:
        return list(map(self.sanitize_input, command.strip().split()))

    def sanitize_arc_command(self, command: str) -> str:
        return self.sanitize_input(command)
