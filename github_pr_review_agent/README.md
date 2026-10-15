# GitHub PR Review Agent

An AI agent that automatically reviews GitHub pull requests, identifies issues, and applies fixes directly to the code. Built with NVIDIA's NeMo Agent Toolkit.

## Overview

**Status**: ✅ Complete  
**Difficulty**: Intermediate  
**Duration**: 20-30 minutes to run your first review

This agent demonstrates:
- Reading GitHub PR data via API
- Reasoning about code quality (ReAct loop)
- Writing and committing code changes
- Git operations from within an agent

## Quick Start

### Prerequisites

- Python 3.10+
- Git installed
- GitHub personal access token ([create here](https://github.com/settings/tokens))
- NeMo Agent Toolkit installed

### Setup

1. **Install dependencies**:
```bash
cd github_pr_review_agent
pip install -r requirements.txt
```

2. **Set GitHub token**:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

3. **Configure the agent** (`configs/config.yml`):
```yaml
functions:
  review_pr:
    github_token: ${GITHUB_TOKEN}
    repo_owner: your-org      # Change this
    repo_name: your-repo      # Change this
```

### Run

**Review only (give feedback)**:
```bash
nat run --config_file configs/config.yml \
  --input "Review PR #5 for security issues"
```

**Review and fix (apply changes)**:
```bash
nat run --config_file configs/config.yml \
  --input "Review PR #5 and fix any bugs"
```

## How It Works

### The Agent's Toolkit (9 Tools)

| Tool | Purpose | Type |
|------|---------|------|
| `list_prs()` | List open PRs | Read |
| `get_pr_info(number)` | Get PR title, author, description | Read |
| `get_files(number)` | List changed files with stats | Read |
| `get_diff(number, filename)` | Get code diff for a file | Read |
| `submit_comment(number, filename, comment)` | Post review feedback | Read |
| `clone()` | Clone repo locally | Write |
| `checkout(number)` | Switch to PR branch | Write |
| `write(filepath, content)` | Edit a file | Write |
| `commit(message)` | Commit and push changes | Write |

### The Reasoning Loop (ReAct)

```
1. THINK: Agent reads PR info and thinks about what needs review
2. ACT: Agent calls tools (read diffs, understand code)
3. OBSERVE: Agent gets results back
4. REPEAT: Loop continues until done

If review finds bugs:
1. THINK: "This needs fixing"
2. ACT: Call clone() → checkout() → write() → commit()
3. OBSERVE: Changes pushed to GitHub
4. DONE: Task complete
```

### Example Execution

```bash
$ nat run --config_file configs/config.yml \
    --input "Review PR #5 and fix bugs"

Thought: I need to review PR #5. Let me get its info.
Action: get_pr_info(5)
Observation: PR #5: Add authentication. 3 files changed.

Thought: What files were modified?
Action: get_files(5)
Observation: src/auth.py (+150/-20), src/jwt.py (+80/-10), tests/ ...

Thought: Let me examine the main changes.
Action: get_diff(5, "src/auth.py")
Observation: [Shows code diff]

Thought: I see a potential issue. Let me fix it.
Action: clone()
Observation: ✓ Cloned repo

Action: checkout(5)
Observation: ✓ Checked out branch

Action: write("src/jwt.py", "def validate(...)...")
Observation: ✓ Wrote file

Action: commit("Add error handling to JWT validator")
Observation: ✓ Committed and pushed

Final: Review complete. Fixed jwt.py error handling.
```

## Architecture

### File Structure

```
github_pr_review_agent/
├── src/github_pr_review_agent/
│   ├── __init__.py
│   ├── review_pr.py        # Tool definitions + GitHub/Git integration
│   └── register.py         # Registers tools with NAT
├── configs/
│   └── config.yml          # Agent configuration
├── sample_prs/
│   ├── pr_42.json          # Example PR data (for testing)
│   └── pr_43.json
├── pyproject.toml
├── requirements.txt
└── README.md               # This file
```

### Code Components

**`review_pr.py` - Core Logic**

1. **ReviewPRConfig** - Validated settings from YAML
2. **GitHubTools** - All interactions with GitHub API + Git CLI
3. **Tool functions** - Async wrappers the agent calls
4. **@register_function** - Decorator that registers tools with NAT

**`config.yml` - Agent Brain**

```yaml
functions:          # Tools available to agent
  review_pr:
    _type: review_pr
    github_token: ${GITHUB_TOKEN}
    repo_owner: anthropics
    repo_name: claude-code

llms:              # Which LLM to use
  agent_llm:
    _type: nim
    model_name: nvidia/nemotron-3.5-lightning-30b-a3b

workflow:          # How agent reasons
  _type: react_agent
  system_prompt: |
    You are an expert code reviewer and fixer...
```

## Usage Patterns

### Pattern 1: Security Review Only

```bash
nat run --config_file configs/config.yml \
  --input "Review PR #10 focusing on security vulnerabilities"
```

Agent will:
1. Get PR info
2. Examine all files
3. Post security-focused comments
4. NOT modify code

### Pattern 2: Auto-Fix Simple Issues

```bash
nat run --config_file configs/config.yml \
  --input "Review PR #10 and fix style/formatting issues"
```

Agent will:
1. Review code
2. Identify formatting issues
3. Clone repo
4. Fix formatting
5. Commit changes

### Pattern 3: Deep Review + Fixes

```bash
nat run --config_file configs/config.yml \
  --input "Thoroughly review PR #10. Identify all issues and apply fixes."
```

Agent will:
1. Deep analysis
2. Find bugs, security issues, performance problems
3. Fix what it can
4. Post comments on complex issues

## Key Concepts

### 1. Tools Are Functions

Each tool is an async function. The agent doesn't know HOW it works, only:
- Name: `get_pr_info`
- Description: "Get PR details: title, author, description..."
- Parameters: `pr_number`
- Returns: String with result

### 2. Descriptions Drive Behavior

```python
async def _get_diff(pr_number: int, filename: str) -> str:
    """Get the actual code diff for a specific file in the PR."""
    return tools.get_file_diff(pr_number, filename)
```

The LLM reads the docstring to decide WHEN to use this tool.

### 3. Two Types of Operations

**Read Operations** (GitHub API):
- Call REST API
- Stateless
- Return formatted strings

**Write Operations** (Git CLI):
- Use subprocess
- Maintain local clone
- Persist across tool calls
- Changes pushed to GitHub

### 4. The Config Drives Everything

Change behavior without code changes:
```yaml
# Change system prompt → agent thinks differently
system_prompt: |
  Focus ONLY on critical security issues.

# Change LLM → different reasoning
llms:
  agent_llm:
    _type: openai
    model_name: gpt-4

# Change repo → reviews different project
functions:
  review_pr:
    repo_owner: different-org
    repo_name: different-repo
```

## Extending the Agent

### Add a New Tool

1. Add method to `GitHubTools` class:
```python
def get_commit_info(self, pr_number: int, commit_sha: str) -> str:
    data = self._get(f"/repos/.../commits/{commit_sha}")
    return f"Commit: {data['message']}"
```

2. Create async wrapper in `review_pr()`:
```python
async def _get_commit(pr_number: int, commit_sha: str) -> str:
    """Get info about a specific commit in the PR."""
    return tools.get_commit_info(pr_number, commit_sha)

yield FunctionInfo.from_fn(_get_commit, description=_get_commit.__doc__)
```

3. Mention in system_prompt so agent knows to use it.

### Change Agent Behavior

Edit `system_prompt` in `config.yml`:
```yaml
system_prompt: |
  Focus on: performance optimization, not style issues.
  Suggest concrete improvements for every finding.
  Always check for O(n²) algorithms.
```

### Use Different LLM

```yaml
llms:
  agent_llm:
    _type: openai
    model_name: gpt-4
    api_key: ${OPENAI_API_KEY}
```

## Limitations & Improvements

### Current Limitations

- Line-level comments simplified (all at line 1)
- No merge conflict handling
- No test execution
- Simple rollback if issues
- GitHub token must have repo write access

### Future Improvements

- [ ] Semantic code analysis (understand intent, not just syntax)
- [ ] Auto-generate tests for changes
- [ ] Parallel reviews (multiple agents on same PR)
- [ ] Learn from feedback (which fixes get accepted?)
- [ ] Deploy as GitHub App (automated on new PRs)
- [ ] Conflict resolution
- [ ] Run test suite before committing

## Troubleshooting

### "Token not found" error
```bash
# Make sure environment variable is set
export GITHUB_TOKEN="ghp_xxx"
echo $GITHUB_TOKEN  # Should print your token
```

### "Repository not found"
- Check `repo_owner` and `repo_name` in config.yml
- Verify token has access to that repo
- Try: `git clone https://token@github.com/owner/repo.git`

### "Failed to push"
- Check git config: `git config --global user.email "email@example.com"`
- Check branch exists locally: `cd /tmp/repo_name && git branch`
- Check token has write access

### Agent doesn't write code
- Check system_prompt mentions "fix" or "write"
- Verify `_write` and `_commit` tools are registered
- Check agent output for "Action: write" or "Action: commit"

### Changes don't appear on GitHub
- Check git push succeeded: `✓ Committed and pushed`
- Verify `/tmp/repo_name` has the changes
- Check GitHub PR branch for new commit

## Learning Outcomes

After studying this agent, you understand:

✅ How agents call tools in a reasoning loop  
✅ How tool descriptions guide agent behavior  
✅ How to integrate GitHub API + Git CLI  
✅ How to structure async tool functions  
✅ How configuration drives agent behavior  
✅ How agents can write code and commit changes  
✅ How ReAct (Reasoning + Acting) patterns work  
✅ How to extend agents with new capabilities  

## Examples

### Real-World Use Cases

1. **Automated Security Scanning**
   - Review all PRs for SQL injection, XSS
   - Suggest fixes
   - Auto-fix common patterns

2. **Code Quality Enforcement**
   - Check for proper error handling
   - Verify test coverage
   - Fix formatting issues

3. **Performance Analysis**
   - Detect O(n²) algorithms
   - Suggest optimizations
   - Apply common speedups

4. **Dependency Updates**
   - Review version bumps
   - Check for breaking changes
   - Update code if needed

## Next Steps

1. **Run on your own repo**: Update config.yml with your GitHub org
2. **Customize the prompt**: Adjust system_prompt for your needs
3. **Add tools**: Implement new capabilities
4. **Deploy as bot**: Make it run automatically on new PRs

## References

- [NeMo Agent Toolkit Docs](https://docs.nvidia.com/nemo/agent-toolkit/)
- [GitHub API Docs](https://docs.github.com/en/rest)
- [Git Documentation](https://git-scm.com/doc)
- [ReAct Agent Pattern](https://arxiv.org/abs/2210.03629)

---

**Created**: October 2024  
**Status**: Ready for production  
**License**: Educational

Happy reviewing! 🚀
