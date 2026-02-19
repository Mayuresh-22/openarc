import json
from typing import Optional
from src.const.prompts import ALL_PROMPTS_FILE_PATH


class PromptService:
    def __init__(self):
        self.sys_prompt = None
        self.user_prompt = None
        self.tool_prompt = None

    def get_sys_prompt(
        self, 
        sys_prompt_file: str = ALL_PROMPTS_FILE_PATH.SYSTEM_PROMPT_FILE_PATH
    ) -> str:
        """
        This method returns the static system prompt that is used to instruct the OpenArc agent on how to behave and perform its tasks.
        
        :param self: Description
        :param sys_prompt_file: Path to system prompt markdown file
        :type sys_prompt_file: str
        :return: System prompt string
        :rtype: str
        """
        return self.sys_prompt or open(sys_prompt_file, "r").read()
    
    def set_sys_prompt(self, new_sys_prompt: str, sys_prompt_file: str = ALL_PROMPTS_FILE_PATH.SYSTEM_PROMPT_FILE_PATH) -> None:
        """
        This method allows updating the system prompt with a new prompt string. It overwrites the existing system prompt file with the new content.
        
        :param self: Description
        :param new_sys_prompt: The new system prompt string to be set
        :type new_sys_prompt: str
        :param sys_prompt_file: Path to system prompt markdown file
        :type sys_prompt_file: str
        """
        with open(sys_prompt_file, "w") as f:
            f.write(new_sys_prompt)
            self.sys_prompt = new_sys_prompt
    
    def get_user_prompt(
        self, 
        user_prompt_file: str = ALL_PROMPTS_FILE_PATH.USER_PROMPT_FILE_PATH,
        dynamic_values: Optional[dict] = None
    ) -> str:
        """
        This method returns the user prompt that is used to provide the OpenArc agent with user-specific information, such as user preferences, past interactions, or any other relevant context that can help the agent personalize its responses and actions. The method can also accept dynamic values that are merged into the prompt.
        
        :param self: Description
        :param user_prompt_file: Path to user prompt markdown file
        :type user_prompt_file: str
        :param dynamic_values: A dictionary of dynamic values to be merged into the user prompt
        :type dynamic_values: Optional[dict]
        :return: User prompt string
        :rtype: str
        """
        if self.user_prompt: return self.user_prompt
        with open(user_prompt_file, "r") as f:
            prompt = f.read()
            if dynamic_values:
                prompt += "\n\n### User Details:\n" + json.dumps(
                    dynamic_values, indent=2
                )
            return prompt
    
    def set_user_prompt(
        self, 
        new_user_prompt: str, 
        user_prompt_file: str = ALL_PROMPTS_FILE_PATH.USER_PROMPT_FILE_PATH
    ) -> None:
        """
        This method allows updating the user prompt with a new prompt string. 
        It overwrites the existing user prompt file with the new content.
        
        :param self: Description
        :param new_user_prompt: The new user prompt string to be set
        :type new_user_prompt: str
        :param user_prompt_file: Path to user prompt markdown file
        :type user_prompt_file: str
        """
        with open(user_prompt_file, "w") as f:
            f.write(new_user_prompt)
        self.user_prompt = new_user_prompt
        
    def get_tool_prompt(
        self, 
        tool_prompt_file: str = ALL_PROMPTS_FILE_PATH.TOOL_PROMPT_FILE_PATH
    ) -> str:
        """
        This method returns the tool prompt that is basically a static instruction provided to the OpenArc agent to guide how it should utilize the available tools to perform its tasks effectively.
        Note: This prompt doesn't include the tools defination itself, but rather works as a instruction for how the agent should use the tools.
        
        :param self: Description
        :param tool_prompt_file: Path to tool prompt markdown file
        :type tool_prompt_file: str
        :return: Tool prompt string
        :rtype: str
        """
        return self.tool_prompt or open(tool_prompt_file, "r").read()
    
    def set_tool_prompt(self, new_tool_prompt: str, tool_prompt_file: str = ALL_PROMPTS_FILE_PATH.TOOL_PROMPT_FILE_PATH) -> None:
        """
        This method allows updating the tool prompt with a new prompt string. It overwrites the existing tool prompt file with the new content.
        
        :param self: Description
        :param new_tool_prompt: The new tool prompt string to be set
        :type new_tool_prompt: str
        :param tool_prompt_file: Path to tool prompt markdown file
        :type tool_prompt_file: str
        """
        with open(tool_prompt_file, "w") as f:
            f.write(new_tool_prompt)
            self.tool_prompt = new_tool_prompt
        