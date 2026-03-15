from agno.workflow import Workflow
from agno.db.sqlite import SqliteDb
from typing_extensions import Self

from src.core.agents.executor.run import run_executor_agent
from src.const.workflow import WORKFLOW_MEMORY_PATH
from src.core.agents.planner.run import run_planner_agent
from src.core.handlers.base_handler import BaseHandler
from src.types.cli import CLIOutput
from src.utils.agent import build_session_id


class ArcQueryHandler(BaseHandler):
    _instance = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(ArcQueryHandler, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.workflow_session_id = build_session_id()
        self.workflow = Workflow(
            name="OpenArc AI Agent Mode",
            session_id=self.workflow_session_id,
            db=SqliteDb(WORKFLOW_MEMORY_PATH),
            steps=[run_planner_agent, run_executor_agent]
        )

    def handle(self, content: list[str]):
        workflow_response = self.workflow.run(
            content[0], stream=True
        )
        for event in workflow_response:
            if (
                event.event and 
                event.event != "WorkflowStarted" and 
                event.event != "StepOutputWorkflowCompleted" and
                event.event != "WorkflowCompleted" and
                event.event != "StepStarted" and
                event.event != "StepCompleted" and 
                event.event != "StepOutput"
                ):  # type: ignore
                print(f"{event.event}", end="", flush=True)  # type: ignore
        print("\n")
    
        return CLIOutput(stdout=None, stderr=None, exitcode=0)
