from src.core.handlers.base_handler import BaseHandler
from src.types.cli import CLIOutput


class ArcQueryHandler(BaseHandler):
    def handle(self, content: list[str]):
        return CLIOutput(stdout=None, stderr=None, exitcode=0)
