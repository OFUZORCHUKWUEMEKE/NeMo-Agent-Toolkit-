"""Configuration management for NeMo agent projects."""

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from pydantic import BaseModel, Field


class YamlConfig:
    """Load and manage YAML configuration files."""

    def __init__(self, config_path: Path | str):
        """Initialize config loader.

        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = Path(config_path)
        self.data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r") as f:
            self.data = yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.

        Args:
            key: Key path (e.g., 'agent_defaults.temperature')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self.data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_section(self, section: str) -> dict[str, Any]:
        """Get entire configuration section.

        Args:
            section: Section name

        Returns:
            Section dictionary
        """
        return self.data.get(section, {})

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary."""
        return self.data.copy()

    def __repr__(self) -> str:
        return f"YamlConfig(path={self.config_path})"


class ConfiguredAgent(BaseModel):
    """Agent configuration from YAML."""

    name: str = Field(..., description="Agent name")
    description: Optional[str] = None
    model_name: str = Field(default="gpt-4")
    system_prompt: str = Field(default="You are a helpful assistant.")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(default=2048, gt=0)
    timeout: int = Field(default=30, gt=0)
    enable_history: bool = Field(default=True)
    max_history_messages: int = Field(default=100, gt=0)

    def to_agent_config(self):
        """Convert to AgentConfig for use in projects.

        Returns:
            AgentConfig instance
        """
        # Import here to avoid circular imports
        from .agent_base import AgentConfig

        return AgentConfig(
            model_name=self.model_name,
            system_prompt=self.system_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
        )


def load_agent_config(config_path: Path | str, agent_key: str) -> ConfiguredAgent:
    """Load agent configuration from YAML file.

    Args:
        config_path: Path to YAML file
        agent_key: Dot-notation key to agent config (e.g., 'projects.hello_agent')

    Returns:
        ConfiguredAgent instance
    """
    config = YamlConfig(config_path)

    # Get agent config section
    agent_data = config.get(agent_key)
    if not agent_data:
        raise ValueError(f"Agent configuration not found: {agent_key}")

    return ConfiguredAgent(**agent_data)


def load_project_config(config_path: Path | str) -> YamlConfig:
    """Load project configuration.

    Args:
        config_path: Path to YAML file

    Returns:
        YamlConfig instance
    """
    return YamlConfig(config_path)


def substitute_env_variables(value: Any) -> Any:
    """Substitute environment variables in config values.

    Supports ${VAR_NAME} syntax.

    Args:
        value: Configuration value (can be string, dict, list, etc.)

    Returns:
        Value with environment variables substituted
    """
    if isinstance(value, str):
        # Replace ${VAR_NAME} with environment variable
        import re

        pattern = r"\$\{([^}]+)\}"
        return re.sub(
            pattern, lambda m: os.environ.get(m.group(1), m.group(0)), value
        )
    elif isinstance(value, dict):
        return {k: substitute_env_variables(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [substitute_env_variables(item) for item in value]
    else:
        return value


# Example usage functions
def example_load_global_config() -> YamlConfig:
    """Example: Load global configuration."""
    config = YamlConfig(Path(__file__).parent.parent / "config.yaml")
    return config


def example_load_level_config(level: int) -> YamlConfig:
    """Example: Load level-specific configuration."""
    level_dir = Path(__file__).parent.parent / f"level_{level}_foundations"
    config = YamlConfig(level_dir / "config.yaml")
    return config


def example_print_config() -> None:
    """Example: Print configuration."""
    config = example_load_global_config()
    print("Global Configuration:")
    print(yaml.dump(config.to_dict(), default_flow_style=False))
