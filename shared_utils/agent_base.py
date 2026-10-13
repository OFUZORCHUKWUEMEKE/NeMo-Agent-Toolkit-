"""Base agent class for NeMo toolkit learning projects."""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from pydantic import BaseModel, Field


@dataclass
class AgentConfig:
    """Configuration for an agent."""

    model_name: str = "gpt-4"
    system_prompt: str = "You are a helpful assistant."
    temperature: float = 0.7
    max_tokens: int = 2048
    timeout: int = 30


class Message(BaseModel):
    """A single message in the conversation."""

    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message content")


class ToolResult(BaseModel):
    """Result of a tool execution."""

    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None


class BaseAgent:
    """Base agent class for NeMo toolkit learning."""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.conversation_history: list[Message] = []
        self.tools: dict[str, Callable] = {}

    def register_tool(self, name: str, tool: Callable) -> None:
        """Register a tool that the agent can use."""
        self.tools[name] = tool
        self.logger.debug(f"Registered tool: {name}")

    async def chat(self, user_message: str) -> str:
        """Process a user message and return agent response.

        This is the main interaction loop. Override in subclasses for custom behavior.
        """
        self.conversation_history.append(Message(role="user", content=user_message))
        self.logger.info(f"User: {user_message}")

        # Simulate agent thinking (in real implementation, call LLM)
        response = await self._process_message(user_message)

        self.conversation_history.append(Message(role="assistant", content=response))
        self.logger.info(f"Assistant: {response}")

        return response

    async def _process_message(self, message: str) -> str:
        """Process a message. Override in subclasses for LLM integration."""
        return f"Echo: {message}"

    def get_conversation_history(self) -> list[Message]:
        """Get the conversation history."""
        return self.conversation_history.copy()

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.logger.debug("Conversation history cleared")

    def to_dict(self) -> dict:
        """Serialize agent state to dict."""
        return {
            "config": {
                "model_name": self.config.model_name,
                "system_prompt": self.config.system_prompt,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
            },
            "conversation_history": [msg.model_dump() for msg in self.conversation_history],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BaseAgent":
        """Deserialize agent state from dict."""
        config = AgentConfig(**data["config"])
        agent = cls(config)
        agent.conversation_history = [Message(**msg) for msg in data["conversation_history"]]
        return agent
