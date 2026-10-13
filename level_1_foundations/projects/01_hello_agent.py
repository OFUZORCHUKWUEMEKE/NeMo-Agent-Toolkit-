"""
Level 1, Project 1: Hello Agent
================================
Learn the basics of creating and interacting with a simple agent.

What you'll learn:
- Agent initialization and lifecycle
- Basic agent configuration
- Simple conversation loop
- Agent state management

Key Concepts:
- AgentConfig: Configuration object for agents
- BaseAgent: Core agent class
- Message history: Tracking conversations
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared_utils import BaseAgent, AgentConfig, setup_logging


class SimpleAgent(BaseAgent):
    """A simple agent that echoes user input and maintains conversation history."""

    async def _process_message(self, message: str) -> str:
        """Process a message with a simple echo response."""
        response = f"You said: '{message}'. I'm a simple agent and I understand you!"
        return response


async def main():
    """Main function to demonstrate Hello Agent."""
    # Setup logging
    logger = setup_logging(__name__)
    logger.info("Starting Hello Agent project")

    # Create agent configuration
    config = AgentConfig(
        model_name="simple",
        system_prompt="You are a simple agent that echoes and acknowledges user input.",
        temperature=0.5,
        max_tokens=256,
    )

    # Create the agent
    agent = SimpleAgent(config)
    logger.info("Agent initialized")

    # Interactive conversation loop
    print("\n" + "=" * 60)
    print("Welcome to Hello Agent!")
    print("=" * 60)
    print(f"System Prompt: {config.system_prompt}")
    print("\nType 'quit' to exit, 'history' to see conversation history")
    print("-" * 60 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                logger.info("User quit the conversation")
                print("\nGoodbye!")
                break

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
    print("\n" + "=" * 60)
    print("Conversation Statistics")
    print("=" * 60)
    print(f"Total messages: {len(history)}")
    print(f"User messages: {sum(1 for m in history if m.role == 'user')}")
    print(f"Agent responses: {sum(1 for m in history if m.role == 'assistant')}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
