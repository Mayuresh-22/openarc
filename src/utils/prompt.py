from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


prompt_session = PromptSession(
    auto_suggest=AutoSuggestFromHistory(),
)
