from typing import Dict, Any
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains.base import Chain


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


# Base class that supports custom handlers
class CustomCallbackChain(Chain):
    # HACK: LangChain doesn't support custom handlers yet, so we have to use this workaround
    def fire_callback(self, event: str, **kwargs: Any) -> None:
        for callback in self.callbacks:
            if getattr(callback, event):
                getattr(callback, event)(**kwargs)
