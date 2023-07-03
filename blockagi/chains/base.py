import time
from typing import Dict, Any
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains.base import Chain
from langchain.chat_models.base import BaseChatModel


# HACK: LangChain doesn't support custom handlers yet, so we have to use this workaround
# TODO: Change to use on_chain_start and on_chain_end and follow LandChain's conventions
class BlockAGICallbackHandler(BaseCallbackHandler):
    # New big cycle's PRIME step starts
    def on_step_start(self, step: str, inputs: Dict[str, Any]) -> Any:
        """Run on step start."""
        pass

    # New big cycle's PRIME step ends
    def on_step_end(
        self, step: str, inputs: Dict[str, Any], outputs: Dict[str, Any]
    ) -> Any:
        """Run on step end."""
        pass

    # New big cycle starts
    def on_iteration_start(self, inputs: Dict[str, Any]) -> Any:
        """Run on step end."""
        pass

    # New big cycle ends
    def on_iteration_end(self, outputs: Dict[str, Any]) -> Any:
        """Run on step end."""
        pass

    def on_log_message(self, message: str) -> Any:
        """Run whenever there is a new log message."""
        pass


# Base class that supports custom handlers
class CustomCallbackChain(Chain):
    # HACK: LangChain doesn't support custom handlers yet, so we have to use this workaround
    def fire_callback(self, event: str, **kwargs: Any) -> None:
        for callback in self.callbacks:
            if getattr(callback, event):
                getattr(callback, event)(**kwargs)

    def fire_log(self, message: str):
        for callback in self.callbacks:
            if hasattr(callback, "on_log_message"):
                getattr(callback, "on_log_message")(message)


class CustomCallbackLLMChain(CustomCallbackChain):
    llm: BaseChatModel

    def retry_llm(self, messages, retry_count=5):
        sleep_duration = 0.5
        for _idx in range(retry_count - 1):
            try:
                return self.llm(messages)
            except Exception as e:
                self.fire_log(f"LLM failed with error: {e}; Retrying")
                time.sleep(sleep_duration)
            sleep_duration *= 2
        return self.llm(messages)
