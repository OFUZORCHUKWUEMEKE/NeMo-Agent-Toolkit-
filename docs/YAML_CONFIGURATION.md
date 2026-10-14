# YAML Configuration Guide 📋

## Overview

This project uses YAML configuration files to manage agent settings, tool definitions, and project structure. This approach separates configuration from code, making it easy to:

- Change settings without modifying code
- Manage multiple environments (dev, prod)
- Version control configurations separately
- Share configurations between projects
- Understand system architecture at a glance

---

## Configuration Files Structure

```
NeMo-Agent-Toolkit-/
├── config.yaml                           # Global configuration
├── level_1_foundations/
│   ├── config.yaml                       # Level 1 specific config
│   └── projects/
│       ├── 01_hello_agent.py
│       └── 01_hello_agent_with_yaml.py   # Uses config.yaml
├── level_2_tools/
│   ├── config.yaml                       # Level 2 specific config
│   └── projects/
├── level_3_advanced/
│   ├── config.yaml
│   └── projects/
└── ...
```

### Configuration Hierarchy

```
Global Config (config.yaml)
    ↓
Level Config (level_X/config.yaml)
    ↓
Project Config (embedded in level config)
    ↓
Runtime Overrides (environment variables)
```

---

## Global Configuration (`config.yaml`)

The root `config.yaml` file contains project-wide settings.

### Project Metadata

```yaml
project:
  name: "NeMo Agent Toolkit Learning Path"
  version: "0.1.0"
  description: "Progressive learning journey through AI agents"
  author: "NeMo Learner"
  created: "2024-10-13"
```

### Logging Configuration

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file:
    enabled: true
    directory: "logs"
    max_bytes: 10485760  # 10MB
    backup_count: 5
```

**What each setting does:**

| Setting | Purpose |
|---------|---------|
| `level` | Minimum log level to display |
| `format` | How log messages are formatted |
| `file.enabled` | Whether to write logs to files |
| `file.directory` | Where to store log files |
| `file.max_bytes` | Max log file size before rotation |
| `backup_count` | How many old log files to keep |

### Agent Defaults

```yaml
agent_defaults:
  model_name: "gpt-4"
  temperature: 0.7
  max_tokens: 2048
  timeout: 30
  enable_history: true
  max_history_messages: 100
```

These are used when creating agents if no specific config is provided.

### LLM Provider Configuration

```yaml
llm:
  provider: "mock"  # Which provider to use
  
  openai:
    api_key: "${OPENAI_API_KEY}"  # From environment variable
    model: "gpt-4"
    temperature: 0.7
  
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    model: "claude-3-sonnet-20240229"
  
  mock:
    enabled: true
    latency_ms: 100
    use_echo_responses: true
```

**Environment Variables:**
- `${VAR_NAME}` syntax loads from environment variables
- Useful for API keys and secrets

---

## Level Configuration (`level_X/config.yaml`)

Each level has its own configuration file that inherits and overrides global settings.

### Level Metadata

```yaml
level: 1
name: "Foundations"
description: "Learn basic agent concepts and initialization"
```

### Level-Specific Agent Defaults

```yaml
agent_defaults:
  model_name: "simple"
  temperature: 0.5
  max_tokens: 256
  enable_history: true
  max_history_messages: 50
```

Overrides global defaults for this level only.

### Project Definitions

Each project in the level is defined:

```yaml
projects:
  hello_agent:
    name: "Hello Agent"
    file: "projects/01_hello_agent.py"
    description: "Basic agent initialization and chat"
    difficulty: "Beginner"
    duration_hours: 1.5
    
    learning_objectives:
      - "Agent initialization with AgentConfig"
      - "Implementing _process_message() method"
      - "Conversation history management"
    
    config:
      model_name: "simple"
      system_prompt: "You are a simple agent..."
      temperature: 0.5
      max_tokens: 256
```

### Personality Configuration (Level 1)

```yaml
echo_plus_agent:
  name: "Echo Plus Agent"
  personalities:
    friendly:
      system_prompt: "You are cheerful..."
      temperature: 0.8
    professional:
      system_prompt: "You are professional..."
      temperature: 0.5
    pirate:
      system_prompt: "You are a pirate..."
      temperature: 0.9
```

---

## Loading YAML Configurations

### In Python Code

```python
from pathlib import Path
from shared_utils import load_project_config, YamlConfig

# Load global config
global_config = load_project_config(Path("config.yaml"))

# Load level config
level_config = load_project_config(Path("level_1_foundations/config.yaml"))

# Get specific values
agent_defaults = global_config.get_section("agent_defaults")
logging_level = global_config.get("logging.level")

# Get agent config
hello_agent_config = level_config.get("projects.hello_agent")
```

### Using the YamlConfig Class

```python
from shared_utils import YamlConfig
from pathlib import Path

# Create config loader
config = YamlConfig(Path("level_1_foundations/config.yaml"))

# Get values with dot notation
temperature = config.get("projects.hello_agent.config.temperature")
# Returns: 0.5

# Get entire section
projects = config.get_section("projects")
# Returns: dict with all projects

# Get with default value
port = config.get("server.port", default=8000)
# Returns 8000 if server.port not in config
```

### Getting Entire Configurations

```python
# Get everything as a dict
all_config = config.to_dict()

# Get specific section
agent_defaults = config.get_section("agent_defaults")
logging_config = config.get_section("logging")
```

---

## Environment-Specific Configuration

### Development vs Production

```yaml
environments:
  development:
    logging_level: "DEBUG"
    llm:
      provider: "mock"
  
  production:
    logging_level: "INFO"
    llm:
      provider: "anthropic"
```

### Switching Environments

```bash
# Development (default)
python 01_hello_agent.py

# Production
export ENVIRONMENT=production
python 01_hello_agent.py
```

---

## Configuration Best Practices

### ✅ DO

```yaml
# ✅ Good: Descriptive names, clear structure
agent_defaults:
  model_name: "gpt-4"
  temperature: 0.7
  max_tokens: 2048

# ✅ Good: Use environment variables for secrets
llm:
  openai:
    api_key: "${OPENAI_API_KEY}"

# ✅ Good: Comments explaining non-obvious values
temperature: 0.7  # 0=deterministic, 1=creative
```

### ❌ DON'T

```yaml
# ❌ Bad: Hardcoded secrets
api_key: "sk-1234567890abcdef"

# ❌ Bad: Magic numbers without explanation
temp: 0.7

# ❌ Bad: Too deeply nested
a:
  b:
    c:
      d:
        e: value  # Hard to find!

# ❌ Bad: Inconsistent formatting
logging: {level: INFO, file: logs}  # Mix of styles
```

---

## Common Configuration Patterns

### Pattern 1: Base + Override

**base_config.yaml:**
```yaml
agent_defaults:
  temperature: 0.7
  max_tokens: 2048
```

**project_config.yaml:**
```yaml
agent_defaults:
  temperature: 0.5  # Override only what's needed
  # max_tokens inherited from base
```

### Pattern 2: Environment Variables

```yaml
database:
  connection_string: "${DATABASE_URL}"
  
llm:
  openai:
    api_key: "${OPENAI_API_KEY}"
```

Load from environment:
```bash
export OPENAI_API_KEY=sk-...
export DATABASE_URL=postgresql://...
python agent.py
```

### Pattern 3: Conditional Configuration

```yaml
environments:
  development:
    debug: true
    log_level: "DEBUG"
    
  production:
    debug: false
    log_level: "WARNING"
```

Load based on environment:
```python
env = os.getenv("ENVIRONMENT", "development")
config = load_config(f"config.{env}.yaml")
```

---

## YAML Syntax Quick Reference

### Basic Types

```yaml
# Strings
name: "John Doe"
description: >
  This is a multi-line
  string that wraps
  automatically

# Numbers
temperature: 0.7
max_tokens: 2048
port: 8000

# Booleans
enabled: true
debug: false

# Null
value: null
```

### Lists

```yaml
# List syntax
tags:
  - "agent"
  - "nlp"
  - "learning"

# Or inline
tags: ["agent", "nlp", "learning"]
```

### Dictionaries

```yaml
# Nested dictionary
agent:
  name: "MyAgent"
  config:
    temperature: 0.7
    max_tokens: 2048

# Inline
agent: {name: "MyAgent", temperature: 0.7}
```

### Comments

```yaml
# This is a comment
# Use comments to explain WHY, not WHAT
temperature: 0.7  # Higher = more creative
```

---

## Complete Example: Level 1 Config

```yaml
# Level 1: Foundations
level: 1
name: "Foundations"
description: "Learn basic agent concepts"

agent_defaults:
  model_name: "simple"
  temperature: 0.5
  max_tokens: 256

projects:
  hello_agent:
    name: "Hello Agent"
    file: "projects/01_hello_agent.py"
    difficulty: "Beginner"
    duration_hours: 1.5
    
    learning_objectives:
      - "Agent initialization"
      - "Conversation history"
      - "Message handling"
    
    config:
      model_name: "simple"
      system_prompt: "You are a simple agent that echoes input."
      temperature: 0.5
      max_tokens: 256

  echo_plus_agent:
    name: "Echo Plus Agent"
    file: "projects/02_echo_plus_agent.py"
    difficulty: "Beginner"
    duration_hours: 1.5
    
    learning_objectives:
      - "System prompts and personality"
      - "Response formatting"
      - "Agent statistics"
    
    personalities:
      friendly:
        system_prompt: "You are cheerful and friendly."
        temperature: 0.8
      professional:
        system_prompt: "You are professional and formal."
        temperature: 0.5
      pirate:
        system_prompt: "You are a pirate."
        temperature: 0.9
```

---

## Loading Configuration in Your Projects

### Example: Hello Agent with YAML

See: `level_1_foundations/projects/01_hello_agent_with_yaml.py`

```python
from pathlib import Path
from shared_utils import load_project_config

# Load level configuration
config_path = Path(__file__).parent.parent / "config.yaml"
project_config = load_project_config(config_path)

# Get specific project config
hello_agent_config = project_config.get_section("projects").get("hello_agent")

# Extract values
model_name = hello_agent_config.get("config", {}).get("model_name")
system_prompt = hello_agent_config.get("config", {}).get("system_prompt")
temperature = hello_agent_config.get("config", {}).get("temperature")
```

---

## Troubleshooting

### Problem: FileNotFoundError when loading config

**Solution**: Make sure config.yaml exists and path is correct
```python
# Check path
config_path = Path(__file__).parent.parent / "config.yaml"
print(f"Looking for config at: {config_path.absolute()}")
print(f"Exists: {config_path.exists()}")
```

### Problem: None returned when getting value

**Solution**: Use dot notation correctly
```python
# ❌ Wrong
value = config.get("llm.openai.api_key")  # Might return None

# ✅ Right
value = config.get("llm.openai.api_key", default="not-found")
```

### Problem: Environment variables not being substituted

**Solution**: Make sure variable exists in environment
```bash
# Define in shell before running
export OPENAI_API_KEY="sk-..."
python agent.py

# Or in Python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

---

## Next Steps

1. **Level 1**: Use basic YAML configs for agent settings
2. **Level 2**: Add tool definitions to YAML
3. **Level 3**: Advanced configuration with memory and state
4. **Level 4**: Multi-agent coordination via YAML
5. **Level 5**: Production configuration management
6. **Level 6**: Complete system configuration

---

## Resources

- [YAML Specification](https://yaml.org/)
- [Python yaml library docs](https://pyyaml.org/)
- [Configuration Management Best Practices](https://12factor.net/config)

---

**Configuration is crucial for production systems. Master it now!** 🎯
