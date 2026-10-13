# NeMo Agent Toolkit - Complete Learning Path 🤖

A comprehensive, hands-on learning journey through NVIDIA's NeMo Agent Toolkit. Build progressively complex AI agents, from simple echo bots to sophisticated multi-agent systems.

## Overview

This repository contains **17 progressive projects** organized into **6 learning levels**, designed to take you from complete beginner to expert in building AI agents.

### Quick Stats
- **Total Projects**: 17
- **Learning Levels**: 6
- **Estimated Duration**: 35-41 hours
- **Difficulty**: Beginner → Advanced
- **Focus**: Hands-on learning through building

## Learning Path

### 📍 Level 1: Foundations (2-4 hours)
**Status**: ✅ In Progress

Learn core concepts by building simple agents:
- Project 1: Hello Agent - Basic agent creation
- Project 2: Echo Plus Agent - Personality customization

[→ See Level 1 README](./level_1_foundations/README.md)

---

### 📍 Level 2: Tools & Functions (4-6 hours)
**Status**: 🔄 Coming Soon

Master the tool calling system:
- Project 1: Calculator Agent
- Project 2: Weather Agent  
- Project 3: Research Agent

---

### 📍 Level 3: Advanced Agent Behavior (5-7 hours)
**Status**: 🔄 Coming Soon

Build sophisticated agents:
- Project 1: Stateful Conversation Agent
- Project 2: Decision-Making Agent
- Project 3: Multi-Tool Orchestrator

---

### 📍 Level 4: Multi-Agent Systems (6-8 hours)
**Status**: 🔄 Coming Soon

Coordinate multiple agents:
- Project 1: Hierarchical Agent System
- Project 2: Collaborative Agents
- Project 3: Competitive Agents

---

### 📍 Level 5: Production Patterns (7-9 hours)
**Status**: 🔄 Coming Soon

Build production-ready systems:
- Project 1: Monitoring & Observability
- Project 2: Scalable Agent Service
- Project 3: Agent Evaluation Framework

---

### 📍 Level 6: Expert Applications (10-12 hours)
**Status**: 🔄 Coming Soon

Build real-world applications:
- Project 1: Autonomous Code Reviewer
- Project 2: Customer Service Agent
- Project 3: Data Analysis Agent

---

## Getting Started

### Prerequisites
- Python 3.10+
- pip or conda
- Basic Python async/await knowledge (helpful, not required)

### Installation

1. **Clone the repository**:
```bash
git clone <repo-url>
cd NeMo-Agent-Toolkit-
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Start Level 1**:
```bash
cd level_1_foundations
python projects/01_hello_agent.py
```

## Project Structure

```
NeMo-Agent-Toolkit-/
├── README.md                          # This file
├── pyproject.toml                     # Project configuration
├── requirements.txt                   # Python dependencies
│
├── shared_utils/                      # Shared code for all projects
│   ├── __init__.py
│   ├── agent_base.py                 # BaseAgent class
│   ├── logging_utils.py               # Logging setup
│   └── types.py                       # Type definitions
│
├── level_1_foundations/               # Level 1: Foundations
│   ├── README.md
│   └── projects/
│       ├── 01_hello_agent.py
│       └── 02_echo_plus_agent.py
│
├── level_2_tools/                     # Level 2: Tools & Functions
│   ├── README.md
│   └── projects/
│
├── level_3_advanced/                  # Level 3: Advanced Behavior
│   ├── README.md
│   └── projects/
│
├── level_4_multi_agent/               # Level 4: Multi-Agent Systems
│   ├── README.md
│   └── projects/
│
├── level_5_production/                # Level 5: Production Patterns
│   ├── README.md
│   └── projects/
│
├── level_6_expert/                    # Level 6: Expert Applications
│   ├── README.md
│   └── projects/
│
├── tests/                             # Test suite for all projects
├── docs/                              # Documentation and guides
└── logs/                              # Generated at runtime
```

## Core Concepts

### 1. Agents
Autonomous entities that can:
- Understand and process user input
- Maintain conversation context
- Call external tools/functions
- Make decisions and take actions
- Reason about problems

### 2. Tools (Level 2+)
Functions agents can call to:
- Perform calculations
- Query APIs
- Search the web
- Access databases
- Interact with external systems

### 3. State Management (Level 3+)
Agents track:
- Conversation history
- Long-term memory
- Context windows
- User profiles
- System state

### 4. Multi-Agent Systems (Level 4+)
Multiple agents:
- Communicating with each other
- Delegating tasks
- Aggregating results
- Negotiating solutions
- Competing or collaborating

### 5. Production Systems (Level 5+)
Real-world considerations:
- Monitoring and observability
- Scalability and performance
- Error handling and recovery
- Cost management
- User satisfaction metrics

## How to Use This Repository

### 1. **Sequential Learning** (Recommended)
Start with Level 1, complete all projects, then move to Level 2, etc.

```bash
# Level 1
cd level_1_foundations/projects
python 01_hello_agent.py
python 02_echo_plus_agent.py

# When ready, move to Level 2
cd ../../level_2_tools/projects
# ... continue
```

### 2. **Targeted Learning**
Jump to a specific level based on your current knowledge:
- Know basics? → Start at Level 2
- Can build tools? → Start at Level 3
- Need multi-agent? → Start at Level 4

### 3. **Experimental Learning**
Pick projects that interest you most and build from there, then circle back to fill gaps.

## Key Learning Outcomes

By completing this learning path, you will be able to:

✅ **Build**: Create AI agents from scratch  
✅ **Configure**: Customize agent behavior with prompts  
✅ **Extend**: Add tools and functions to agents  
✅ **Orchestrate**: Coordinate multiple agents  
✅ **Deploy**: Run agents in production  
✅ **Scale**: Handle complex multi-agent systems  
✅ **Evaluate**: Measure agent performance  
✅ **Troubleshoot**: Debug agent behavior  

## Tips for Success

1. **Code Along**: Don't just read - actually run the code
2. **Experiment**: Modify projects and see what breaks
3. **Ask Questions**: Why does X work? What if I change Y?
4. **Document**: Keep notes on patterns and solutions
5. **Build on Concepts**: Each level builds on the previous
6. **Don't Rush**: Understanding > Speed

## Troubleshooting

### Python Version Issues
```bash
python --version  # Should be 3.10+
# If not, install from python.org
```

### Import Errors
```bash
# Make sure you're in the right directory
pwd  # Should end with NeMo-Agent-Toolkit-

# And shared_utils is accessible
python -c "from shared_utils import BaseAgent"
```

### Async Errors
Make sure you're using `asyncio.run(main())` at the module level:
```python
if __name__ == "__main__":
    asyncio.run(main())  # ✅ Correct
    # await main()       # ❌ Wrong
```

## Contributing & Feedback

Have suggestions? Found issues? Want to add projects?

- Check existing issues first
- Create detailed bug reports
- Propose new projects or enhancements
- Share what you learned!

## License

This project is provided as an educational resource.

## Roadmap

- [ ] Level 1: Foundations (Current)
- [ ] Level 2: Tools & Functions
- [ ] Level 3: Advanced Behavior
- [ ] Level 4: Multi-Agent Systems
- [ ] Level 5: Production Patterns
- [ ] Level 6: Expert Applications
- [ ] Integration with real NeMo toolkit
- [ ] Video tutorials for each level
- [ ] Community project showcase

## Resources

### Official Documentation
- [NVIDIA NeMo Docs](https://docs.nvidia.com/nemo/)
- [NeMo Agent Toolkit](https://docs.nvidia.com/nemo/agent-toolkit/)

### Learning Materials
- Prompting best practices (in `docs/`)
- Architecture guides (in each level)
- Example implementations (all projects)

### External Resources
- LLM API Documentation (OpenAI, Anthropic, etc.)
- Async Python Guide
- Agent Design Patterns

## Getting Help

**Stuck on something?**
1. Re-read the project README
2. Check code comments
3. Review the shared_utils modules
4. Try a simpler variation
5. Look at similar projects in the same level

**Want to discuss?**
- Create an issue with detailed context
- Include code snippets and error messages
- Explain what you expected vs. what happened

## Citation

If you use this learning path, feel free to reference it:

```bibtex
@misc{nemo-agent-toolkit-learning,
  title={NeMo Agent Toolkit: Complete Learning Path},
  author={Your Name},
  year={2024},
  url={https://github.com/ofuzorchukwuemeke/nemo-agent-toolkit-}
}
```

---

## Quick Links

- 📖 [Level 1 README](./level_1_foundations/README.md)
- 📚 [Shared Utils](./shared_utils/)
- 🧪 [Tests](./tests/)
- 📝 [Documentation](./docs/)

---

**Happy Learning! 🚀**

Start with Level 1 and enjoy the journey of mastering AI agents!

*Last Updated: October 13, 2024*
