from typing import List
from langchain.schema import BaseMessage
from langchain.prompts import ChatPromptTemplate

def pretty_prompt(messages: List[BaseMessage]) -> str:
    """Return pretty prompt."""
    return ChatPromptTemplate.from_messages(messages).format()