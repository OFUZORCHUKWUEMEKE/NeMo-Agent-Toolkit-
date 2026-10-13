# Level 1: Foundations 🚀

Welcome to the first level of the NeMo Agent Toolkit learning path! This level covers the fundamental concepts you need to understand before moving to more advanced topics.

## Learning Objectives

By completing this level, you will understand:

✅ How to initialize and configure agents  
✅ Basic agent lifecycle and interaction patterns  
✅ Conversation history management  
✅ System prompts and agent personality  
✅ Response formatting and structuring  
✅ Agent state management and serialization  

## Projects in This Level

### Project 1: Hello Agent ⭐
**Duration**: 1-2 hours  
**Difficulty**: Beginner

**File**: `projects/01_hello_agent.py`

**What You'll Build**:
A simple agent that echoes user input and maintains a conversation history. This is your "Hello World" for NeMo agents.

**Key Concepts**:
- Agent initialization with `AgentConfig`
- Creating a custom agent by extending `BaseAgent`
- Implementing the `_process_message()` method
- Conversation loop and user interaction
- History tracking and statistics

**How to Run**:
```bash
python projects/01_hello_agent.py
```

**Interactive Commands**:
- Type messages and press Enter to chat
- `history` - View full conversation history
- `quit` - Exit the program

**Expected Output**:
```
You: Hello
Agent: You said: 'Hello'. I'm a simple agent and I understand you!

You: What is your purpose?
Agent: You said: 'What is your purpose?'. I'm a simple agent and I understand you!

You: history
--- Conversation History ---
user: Hello
assistant: You said: 'Hello'. I'm a simple agent and I understand you!
user: What is your purpose?
assistant: You said: 'What is your purpose?'. I'm a simple agent and I understand you!
```

**Learning Tasks**:
1. Run the basic agent and have a simple conversation
2. Use the `history` command to examine conversation structure
3. **Modify**: Change the system prompt and observe behavior changes
4. **Modify**: Extend the response to include message count
5. **Challenge**: Add a feature to save/load conversation to JSON

---

### Project 2: Echo Plus Agent 🎭
**Duration**: 1-2 hours  
**Difficulty**: Beginner

**File**: `projects/02_echo_plus_agent.py`

**What You'll Build**:
An agent with multiple customizable personalities (Friendly, Professional, Pirate, Wizard, Debug). Learn how system prompts fundamentally change agent behavior.

**Key Concepts**:
- Multiple system prompts for different personalities
- Enum-based configuration management
- Response formatting with metadata
- Agent statistics and analytics
- Command-based interface patterns

**How to Run**:
```bash
python projects/02_echo_plus_agent.py
```

**Interactive Commands**:
- Select a personality (1-5) at startup
- Type messages and observe personality-based responses
- `stats` - View agent statistics
- `reset` - Clear conversation history and reset counters
- `quit` - Exit the program

**Personalities Available**:
1. **Friendly**: Warm, enthusiastic, emoji-using responses
2. **Professional**: Formal, business-oriented, structured advice
3. **Pirate**: Colorful pirate dialect with "Aye!" and "Yarr!"
4. **Wizard**: Mystical, poetic, metaphor-rich responses
5. **Debug**: Systematic problem-solving orientation

**Expected Output**:
```
Available personalities:
  1. FRIENDLY
  2. PROFESSIONAL
  3. PIRATE
  4. WIZARD
  5. DEBUG

Select personality (1-5): 3

✨ Agent Personality: PIRATE
✨ System Prompt: You are a pirate who speaks like a buccaneer...

You: Hello
Agent: Arrr! HELLO? Shiver me timbers! That be a fine query, matey! Aye, I'll help ye navigate these treacherous waters!

You: stats
--- Agent Statistics ---
personality: pirate
total_responses: 1
total_messages: 2
conversation_length: 150
average_message_length: 75.00
```

**Learning Tasks**:
1. Try each personality and notice how system prompts change behavior
2. Examine the stats command to understand message statistics
3. **Modify**: Add a new personality (e.g., "Helpful Teacher" or "Minimalist")
4. **Modify**: Add response quality metrics (sentiment, length distribution)
5. **Challenge**: Create a personality selector that recommends personalities based on use case

---

## Core Concepts Explained

### AgentConfig
Configuration dataclass that controls agent behavior:
```python
config = AgentConfig(
    model_name="gpt-4",              # Which LLM to use
    system_prompt="You are...",      # Defines agent behavior
    temperature=0.7,                 # Randomness (0=deterministic, 1=creative)
    max_tokens=2048,                 # Max response length
)
```

### BaseAgent Class
Abstract base class you inherit from:
```python
class MyAgent(BaseAgent):
    async def _process_message(self, message: str) -> str:
        # Your custom logic here
        return response
```

### Conversation History
Messages are tracked automatically:
```python
history = agent.get_conversation_history()  # Returns list[Message]
agent.clear_history()                       # Reset conversation
```

### System Prompts
Instructions that shape agent behavior. Better prompts = better responses.

Example system prompts:
```
"You are a helpful customer service agent. Always be polite and solve problems."
"You are a code reviewer. Provide detailed feedback on code quality."
"You are a creative writing assistant. Help users tell better stories."
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────┐
│         User Interaction                 │
│  (input -> chat -> output)               │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Agent (Your Custom Class)           │
│  - Inherits from BaseAgent               │
│  - Implements _process_message()         │
│  - Manages tools (later levels)          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Message Processing                  │
│  - system prompt                         │
│  - conversation history                  │
│  - LLM call (mock in this level)         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    Conversation History Storage          │
│  - Message objects                       │
│  - Serialization support                 │
└─────────────────────────────────────────┘
```

---

## Extension Ideas

**After completing both projects, try these extensions**:

### Difficulty: Easy
- [ ] Add email/timestamp to messages
- [ ] Add message filtering (search by keyword)
- [ ] Export conversation to Markdown file
- [ ] Add sentiment analysis for each message
- [ ] Create a personality recommendation system

### Difficulty: Medium
- [ ] Add conversation turns limit before summarization
- [ ] Implement conversation branching (save/load multiple conversations)
- [ ] Add conversation scoring (user satisfaction, agent helpfulness)
- [ ] Create a personality blend system (mix 2 personalities)
- [ ] Add role-playing scenarios with context

### Difficulty: Hard
- [ ] Implement true LLM integration (OpenAI, Anthropic, etc.)
- [ ] Add memory pruning strategies for long conversations
- [ ] Implement agent training from conversation logs
- [ ] Create a multi-agent conversation (two agents talking)
- [ ] Add async streaming responses

---

## Common Issues & Solutions

### Issue: Import errors
**Solution**: Make sure you're running from the project root and the shared_utils folder exists

### Issue: Async/await errors
**Solution**: Use `asyncio.run(main())` at the module level, not inside another async function

### Issue: Configuration not changing behavior
**Solution**: The mock agent ignores prompts. In later levels with real LLMs, you'll see actual differences

---

## Next Steps

Once you complete both Level 1 projects:

1. ✅ Make sure both projects run without errors
2. ✅ Complete at least one extension activity
3. ✅ Document your learnings
4. 📚 Move to **Level 2: Tools & Functions** (where agents get real power!)

---

## Resources

- See `shared_utils/agent_base.py` for the BaseAgent implementation
- See `shared_utils/types.py` for type definitions
- See `shared_utils/logging_utils.py` for logging setup

## Questions?

These are foundational concepts. Understanding them deeply will make everything else much easier!

---

**Created**: October 2024  
**Level**: 1 of 6  
**Estimated Time**: 2-4 hours  
**Status**: Ready to learn! 🚀
