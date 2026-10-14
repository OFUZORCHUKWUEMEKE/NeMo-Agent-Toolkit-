"""
Level 1, Project 1: Hello Agent (YAML Config Version)
======================================================
Learn how to use YAML configuration files with agents.

This is an enhanced version of 01_hello_agent.py that loads configuration
from a YAML file instead of hardcoding values.

What you'll learn:
- Loading YAML configuration files
- Separating config from code
- Using ConfiguredAgent from YAML
- Best practices for production agents
"""

import asyncio
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared_utils import BaseAgent, AgentConfig, setup_logging, load_project_config


class SimpleAgent(BaseAgent):
    """A simple agent that echoes user input and maintains conversation history."""

    async def _process_message(self, message: str) -> str:
        """Process a message with a simple echo response."""
        response = f"You said: '{message}'. I'm a simple agent and I understand you!"
        return response


async def main():
    """Main function demonstrating Hello Agent with YAML config."""
    # Load configuration from YAML
    config_path = Path(__file__).parent.parent / "config.yaml"
    project_config = load_project_config(config_path)

    # Extract Hello Agent configuration
    hello_agent_config = project_config.get_section("projects").get("hello_agent", {})

    # Setup logging
    logger = setup_logging(__name__)
    logger.info("Starting Hello Agent with YAML Config")
    logger.info(f"Loaded config from: {config_path}")

    # Create agent configuration from YAML
    config = AgentConfig(
        model_name=hello_agent_config.get("config", {}).get("model_name", "simple"),
        system_prompt=hello_agent_config.get("config", {}).get(
            "system_prompt",
            "You are a simple agent that echoes and acknowledges user input.",
        ),
        temperature=hello_agent_config.get("config", {}).get("temperature", 0.5),
        max_tokens=hello_agent_config.get("config", {}).get("max_tokens", 256),
    )

    # Create the agent
    agent = SimpleAgent(config)
    logger.info("Agent initialized")

    # Print configuration info
    print("\n" + "=" * 70)
    print("Hello Agent - YAML Configuration Version")
    print("=" * 70)
    print(f"Project: {hello_agent_config.get('name', 'Unknown')}")
    print(f"Description: {hello_agent_config.get('description', 'N/A')}")
    print(f"Difficulty: {hello_agent_config.get('difficulty', 'N/A')}")
    print(f"\nConfiguration:")
    print(f"  Model: {config.model_name}")
    print(f"  Temperature: {config.temperature}")
    print(f"  Max Tokens: {config.max_tokens}")
    print(f"  System Prompt: {config.system_prompt}")
    print("\n" + "-" * 70)
    print("Type 'quit' to exit, 'config' to see config, 'history' for history")
    print("-" * 70 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                logger.info("User quit the conversation")
                print("\nGoodbye!")
                break

            if user_input.lower() == "config":
                print("\n--- Current Configuration ---")
                print(f"Model Name: {config.model_name}")
                print(f"Temperature: {config.temperature}")
                print(f"Max Tokens: {config.max_tokens}")
                print(f"System Prompt: {config.system_prompt}")
                print("---" * 10)
                continue

            if user_input.lower() == "history":
                print("\n--- Conversation History ---")
                for msg in agent.get_conversation_history():
                    print(f"{msg.role.capitalize()}: {msg.content}")
                print("---" * 10)
                continue

            # Process the message
            response = await agent.chat(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            logger.info("User interrupted the conversation")
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            print(f"Error: {e}")

    # Print final statistics
    history = agent.get_conversation_history()
    print("\n" + "=" * 70)
    print("Conversation Statistics")
    print("=" * 70)
    print(f"Total messages: {len(history)}")
    print(f"User messages: {sum(1 for m in history if m.role == 'user')}")
    print(f"Agent responses: {sum(1 for m in history if m.role == 'assistant')}")
    print("=" * 70)

    # Log session summary
    logger.info(
        f"Session summary: {len(history)} messages, "
        f"{sum(1 for m in history if m.role == 'user')} user, "
        f"{sum(1 for m in history if m.role == 'assistant')} assistant"
    )


if __name__ == "__main__":
    asyncio.run(main())
