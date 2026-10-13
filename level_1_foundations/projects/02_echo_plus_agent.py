"""
Level 1, Project 2: Echo Plus Agent
====================================
Learn how to customize agent behavior with system prompts and formatted responses.

What you'll learn:
- Custom system prompts for agent personality
- Response formatting and structuring
- Agent role-playing
- Advanced conversation handling

Key Concepts:
- System prompts: Define agent behavior and constraints
- Response formatting: Structure agent outputs
- Agent personality: Give agents unique characteristics
- Prompt engineering basics
"""

import asyncio
import json
import logging
from pathlib import Path
from enum import Enum
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared_utils import BaseAgent, AgentConfig, setup_logging


class AgentPersonality(Enum):
    """Different agent personalities."""

    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    PIRATE = "pirate"
    WIZARD = "wizard"
    DEBUG = "debug"


SYSTEM_PROMPTS = {
    AgentPersonality.FRIENDLY: """You are a cheerful and friendly assistant.
Always respond with warmth and enthusiasm. Use exclamation marks and emojis when appropriate.
Try to find the positive in everything.""",
    AgentPersonality.PROFESSIONAL: """You are a professional business consultant.
Respond in formal, clear language. Provide structured advice and ask clarifying questions.
Focus on practical business solutions.""",
    AgentPersonality.PIRATE: """You are a pirate who speaks like a buccaneer.
Use pirate vocabulary and expressions. Say 'Aye!', 'Yarr!', 'Shiver me timbers!' etc.
Be colorful and dramatic in your responses.""",
    AgentPersonality.WIZARD: """You are a wise wizard from a fantasy world.
Speak in mystical, poetic language. Reference magic, spells, and ancient wisdom.
Use metaphors and philosophical insights in your responses.""",
    AgentPersonality.DEBUG: """You are a debugging assistant.
When the user describes a problem, break it down into steps.
Provide diagnostic questions and potential solutions.
Format responses with clear problem analysis and next steps.""",
}


class FormattedResponse:
    """Structure for formatted agent responses."""

    def __init__(self, content: str, metadata: dict | None = None):
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = asyncio.get_event_loop().time()

    def to_dict(self) -> dict:
        """Convert response to dictionary."""
        return {
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }

    def __str__(self) -> str:
        return self.content


class EchoPlusAgent(BaseAgent):
    """Agent with customizable personality and formatted responses."""

    def __init__(self, config: AgentConfig, personality: AgentPersonality = AgentPersonality.FRIENDLY):
        super().__init__(config)
        self.personality = personality
        self.config.system_prompt = SYSTEM_PROMPTS[personality]
        self.response_count = 0

    async def _process_message(self, message: str) -> str:
        """Process message with personality-based response."""
        self.response_count += 1

        # Simulate personality-based responses
        responses = {
            AgentPersonality.FRIENDLY: f"Wow, what a great question! 😊 You asked: '{message}'. "
            f"I love this kind of interaction! Let me help you out!",
            AgentPersonality.PROFESSIONAL: f"Thank you for your inquiry: '{message}'. "
            f"I'll analyze this systematically. What specific aspect would you like me to focus on?",
            AgentPersonality.PIRATE: f"Arrr! {message.upper()}? Shiver me timbers! "
            f"That be a fine query, matey! Aye, I'll help ye navigate these treacherous waters!",
            AgentPersonality.WIZARD: f"Ah, a seeker of wisdom asks: '{message}'. "
            f"*waves staff mysteriously* The ancient tomes speak to this question... "
            f"Let me consult the crystalline orb of knowledge.",
            AgentPersonality.DEBUG: f"Problem statement: '{message}'\n"
            f"Analyzing issue... Root cause identification in progress.\n"
            f"Potential solutions being generated.",
        }

        response_text = responses[self.personality]

        # Create formatted response with metadata
        formatted = FormattedResponse(
            content=response_text,
            metadata={
                "personality": self.personality.value,
                "response_number": self.response_count,
                "character_count": len(response_text),
            },
        )

        return formatted.content

    def get_stats(self) -> dict:
        """Get agent statistics."""
        history = self.get_conversation_history()
        return {
            "personality": self.personality.value,
            "total_responses": self.response_count,
            "total_messages": len(history),
            "conversation_length": sum(len(m.content) for m in history),
            "average_message_length": sum(len(m.content) for m in history) / len(history)
            if history
            else 0,
        }


async def main():
    """Main function demonstrating Echo Plus Agent."""
    logger = setup_logging(__name__)
    logger.info("Starting Echo Plus Agent project")

    print("\n" + "=" * 70)
    print("Welcome to Echo Plus Agent!")
    print("=" * 70)
    print("\nAvailable personalities:")
    for i, personality in enumerate(AgentPersonality, 1):
        print(f"  {i}. {personality.value.upper()}")

    # Get personality choice
    while True:
        try:
            choice = input(f"\nSelect personality (1-{len(AgentPersonality)}): ").strip()
            personality = list(AgentPersonality)[int(choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")

    # Create agent with selected personality
    config = AgentConfig(
        model_name="echo-plus",
        system_prompt="",  # Will be set by personality
        temperature=0.8,
        max_tokens=512,
    )

    agent = EchoPlusAgent(config, personality)
    logger.info(f"Agent created with personality: {personality.value}")

    print(f"\n✨ Agent Personality: {personality.value.upper()}")
    print(f"✨ System Prompt: {agent.config.system_prompt[:100]}...")
    print("\n" + "-" * 70)
    print("Commands: 'quit' to exit, 'stats' to see statistics, 'reset' to clear history")
    print("-" * 70 + "\n")

    # Conversation loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "quit":
                logger.info("User quit Echo Plus Agent")
                break

            if user_input.lower() == "stats":
                stats = agent.get_stats()
                print("\n--- Agent Statistics ---")
                for key, value in stats.items():
                    if isinstance(value, float):
                        print(f"{key}: {value:.2f}")
                    else:
                        print(f"{key}: {value}")
                print("---" * 10 + "\n")
                continue

            if user_input.lower() == "reset":
                agent.clear_history()
                agent.response_count = 0
                logger.info("Agent history cleared")
                print("\n✨ History reset!\n")
                continue

            # Get response
            response = await agent.chat(user_input)
            print(f"\nAgent: {response}\n")

        except KeyboardInterrupt:
            logger.info("User interrupted Echo Plus Agent")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}")

    # Final statistics
    stats = agent.get_stats()
    print("\n" + "=" * 70)
    print("Session Summary")
    print("=" * 70)
    print(f"Personality: {stats['personality']}")
    print(f"Total Agent Responses: {stats['total_responses']}")
    print(f"Total Messages: {stats['total_messages']}")
    print(f"Total Characters: {stats['conversation_length']}")
    print(f"Average Message Length: {stats['average_message_length']:.1f}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
