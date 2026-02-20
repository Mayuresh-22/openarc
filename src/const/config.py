from enum import Enum


class ConfigMenuOptionsValue(Enum):
    OPTION_ADD_PROVIDER = "1"
    OPTION_SWITCH_PROVIDER = "2"
    OPTION_MOD_SYS_PROMPT = "3"
    OPTION_MOD_USER_PROMPT = "4"
    OPTION_MOD_TOOL_PROMPT = "5"
    OPTION_CANCEL = "x"


CONFIG_MENU_VAL_LABEL_MAP = {
    ConfigMenuOptionsValue.OPTION_ADD_PROVIDER.value: "Add LLM Provider",
    ConfigMenuOptionsValue.OPTION_SWITCH_PROVIDER.value: "Switch LLM Provider/LLM Model",
    ConfigMenuOptionsValue.OPTION_MOD_SYS_PROMPT.value: "Modify System Prompt",
    ConfigMenuOptionsValue.OPTION_MOD_USER_PROMPT.value: "Modify User Prompt",
    ConfigMenuOptionsValue.OPTION_MOD_TOOL_PROMPT.value: "Modify Tool Prompt",
    ConfigMenuOptionsValue.OPTION_CANCEL.value: "Back to Main Menu",
}