"""Type definitions for NeMo agent toolkit learning projects."""

from typing import Any, Callable

from pydantic import BaseModel, Field


class ToolParameter(BaseModel):
    """Definition of a tool parameter."""

    name: str = Field(..., description="Parameter name")
    type: str = Field(..., description="Python type as string (int, str, float, bool, etc.)")
    description: str = Field(..., description="What this parameter does")
    required: bool = Field(default=True, description="Whether parameter is required")
    default: Any = Field(default=None, description="Default value if not required")


class ToolDefinition(BaseModel):
    """Definition of a tool that an agent can call."""

    name: str = Field(..., description="Unique tool name")
    description: str = Field(..., description="What this tool does")
    parameters: list[ToolParameter] = Field(default_factory=list, description="Tool parameters")
    return_type: str = Field(default="str", description="Return type as string")

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for LLM tool calling."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": [p.model_dump() for p in self.parameters],
            "return_type": self.return_type,
        }
