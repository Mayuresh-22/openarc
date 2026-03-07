"""
This module defines the ToolRegistry class, which is a singleton that manages 
the registration and retrieval of toolkits for agents. 
It allows agents to access a centralized registry of tools that they can utilize in their operations.
"""


from agno.agent import Toolkit


class ToolRegistry:
    _instance = None
    toolkits: list[Toolkit] = []

    def __new__(cls) -> "ToolRegistry":
        if cls._instance is None:
            cls._instance = super(ToolRegistry, cls).__new__(cls)
        return cls._instance

    def register_toolkit(self, toolkit: Toolkit):
        self.toolkits.append(toolkit)
    
    def get_all_toolkits(self):
        print(f"{len(self.toolkits)} toolkits registered in the ToolRegistry.")
        return self.toolkits
