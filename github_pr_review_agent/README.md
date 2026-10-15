# GitHub PR Review Agent

An automated code review agent built with NVIDIA's NeMo Agent Toolkit. This agent reviews pull requests by analyzing code changes, checking for best practices, and providing constructive feedback.

## Overview

The PR Review Agent demonstrates a complete AI agent workflow:
- **Tools** - Functions the agent can call (list PRs, get diffs, submit comments, write code, commit)
- **Reasoning** - ReAct pattern (think → act → observe → repeat)
- **Integration** - Works with real GitHub PRs, clones the repo, edits code, and pushes commits

The agent can both **review** PRs (give feedback) and **fix** bugs (write code and commit).

## Architecture

### Key Components

#### 1. **Tools** (`review_pr.py`)
The agent has access to 9 tools:

**Read Tools** (GitHub API):
```python
_list_prs()                          # List open PRs
_get_pr_info(pr_number)              # Get PR title, author, description
_get_files(pr_number)                # List changed files with stats
_get_diff(pr_number, filename)       # Get code diff for a file
_submit_comment(pr_number, ...)      # Post review feedback
```

**Write Tools** (Git operations):
```python
_clone()                             # Clone repo locally
_checkout(pr_number)                 # Check out PR branch
_write(filepath, content)            # Write/edit a file
_commit(message)                     # Commit and push changes
```

Each tool:
- Returns a status message (string)
- Handles errors gracefully
- Read tools use GitHub API; write tools use git CLI

#### 2. **Authentication** (`GitHubTools`)
Uses GitHub personal access token:
```python
headers = {"Authorization": f"token {github_token}"}
requests.get(url, headers=headers)  # All API calls authenticated
```

#### 3. **Configuration** (`config.yml`)
Specifies:
- GitHub credentials (token, repo owner, repo name)
- LLM to use (Nemotron)
- Workflow (ReAct reasoning loop)
- System prompt for the agent

## How It Works

### Step-by-Step Flow

1. **User Input**: "Review PR #42"

2. **Agent Reasoning Loop** (ReAct):
   ```
   Thought: I need to review PR #42. First, let me get its info.
   Action: Use _get_pr_info tool with pr_number=42
   Observation: PR is "Add user authentication module" with 4 files
   
   Thought: Now I'll check what files changed
   Action: Use _get_files tool with pr_number=42
   Observation: jwt_handler.py, auth_middleware.py, test_auth.py, requirements.txt
   
   Thought: Let me examine the JWT handler code
   Action: Use _get_diff tool with pr_number=42, filename="src/auth/jwt_handler.py"
   Observation: [code diff shown]
   
   Thought: This looks solid but missing input validation...
   Action: Use _submit_comment to post feedback
   [repeat for each file]
   ```

3. **Output**: Structured review with comments

### Key Concepts

**Tools as Agent Actions**
- Each tool is registered with a description
- Agent reads descriptions and decides which tool to call
- Tools return structured data (strings, JSON)

**ReAct Workflow**
- **Reason**: LLM thinks about what to do next
- **Act**: LLM calls a tool
- **Observe**: Agent sees tool output
- **Repeat**: Loop until task is complete

**Configuration-Driven**
- Agents defined entirely in YAML
- No code changes needed to swap models or tools
- Easy to experiment with different prompts

## Setup

### 1. Get a GitHub Token

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes: `repo` (for PR access)
4. Copy the token

### 2. Configure the Agent

Edit `config.yml`:
```yaml
functions:
  review_pr:
    github_token: ${GITHUB_TOKEN}  # Set via env var
    repo_owner: your-org            # Your GitHub org/user
    repo_name: your-repo            # Your repo name
```

### 3. Set Environment Variable

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

## Run the Agent

```bash
# From repo root
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Review PR #1"
```

### Available Commands

**Review-Only (Give Feedback)**
```bash
# Review a PR and post comments
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Review PR #5 for security issues and suggest improvements"

# List open PRs
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "What PRs are open? Which one should I focus on?"
```

**Write-and-Fix (Apply Code Changes)**
```bash
# Fix a bug in the PR
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Review PR #5 and fix any obvious bugs"

# Add a missing feature
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "PR #5 is missing error handling. Add proper error checks."

# Apply linting fixes
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Review PR #5 and fix any style or formatting issues"
```

**Combined (Review Then Fix)**
```bash
# Full workflow: understand, review, then fix
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Thoroughly review PR #5. Identify issues and apply fixes directly to the code."
```

## Understanding the Code

### 1. Tool Registration (`review_pr.py`)

```python
@register_function(config_type=ReviewPRConfig)
async def review_pr(config: ReviewPRConfig, builder: Builder):
    # Define tool functions
    async def _get_pr_info(pr_number: int) -> str:
        """Get PR details: title, author, description, and file statistics."""
        return tools.get_pr_info(pr_number)
    
    # Register tool with description
    yield FunctionInfo.from_fn(_get_pr_info, description=_get_pr_info.__doc__)
```

**Key points:**
- `@register_function` decorator registers with NAT
- `config` contains settings from YAML
- `builder` is the agent framework
- `yield FunctionInfo` makes tools available to agent
- Tool descriptions come from docstrings (LLM reads these!)

### 2. Config Wiring (`config.yml`)

```yaml
functions:
  review_pr:              # Tool group name
    _type: review_pr      # Matches @register_function name
    pr_data_dir: ...      # Passed to ReviewPRConfig

workflow:
  _type: react_agent      # ReAct reasoning pattern
  tool_names: [review_pr] # Which tools to use
```

**Config flow:**
1. Config loads `review_pr` tool
2. Calls `ReviewPRConfig` with `pr_data_dir`
3. Passes config to `review_pr()` function
4. Function yields tools
5. Workflow makes tools available

## Understanding the Code

### 1. Tool Registration (`review_pr.py`)

```python
@register_function(config_type=ReviewPRConfig)
async def review_pr(config, builder):
    tools = GitHubTools(config.github_token, config.repo_owner, config.repo_name)
    
    # Read tool example
    async def _get_pr_info(pr_number: int) -> str:
        """Get PR details: title, author, description, and file statistics."""
        return tools.get_pr_info(pr_number)
    
    # Write tool example
    async def _write(filepath: str, content: str) -> str:
        """Write code/text to a file in the cloned repo. Use relative paths like 'src/main.py'."""
        return tools.write_file(filepath, content)
    
    # Register tools
    yield FunctionInfo.from_fn(_get_pr_info, description=_get_pr_info.__doc__)
    yield FunctionInfo.from_fn(_write, description=_write.__doc__)
```

**Key points:**
- Tool descriptions (docstrings) are read by the LLM to decide when to call each tool
- Read tools call GitHub API with authentication
- Write tools use git CLI (subprocess) to clone, checkout, edit, and push
- All tools are async functions

### 2. The Git Workflow (Write Tools)

When the agent decides to fix code, it:

```python
# 1. Clone the repo
clone() → subprocess.run(["git", "clone", url, repo_path])

# 2. Check out the PR branch
checkout(42) → subprocess.run(["git", "checkout", branch_name])

# 3. Write corrected code
write("src/main.py", new_code) → file.write_text(new_code)

# 4. Commit and push
commit("Fix security bug") → 
  subprocess.run(["git", "add", "-A"])
  subprocess.run(["git", "commit", "-m", message])
  subprocess.run(["git", "push"])
```

The code gets added to the PR branch automatically.

## Extending the Agent

### Add a New Tool

1. **Define the tool function** in `review_pr.py`:
```python
async def _estimate_review_time(pr_number: int) -> str:
    """Estimate how long this PR will take to review."""
    return tools.estimate_time(pr_number)
```

2. **Register it**:
```python
yield FunctionInfo.from_fn(_estimate_review_time, 
                            description=_estimate_review_time.__doc__)
```

3. **Update config** (optional):
```yaml
system_prompt: |
  You now have access to review time estimates...
```

### Change the Review Logic

Edit `system_prompt` in `config.yml`:
```yaml
system_prompt: |
  Focus only on security issues, ignore style.
  Be very strict about SQL injection vulnerabilities.
```

No code changes needed!

### Use a Different LLM

```yaml
llms:
  agent_llm:
    _type: openai          # Change from 'nim' to 'openai'
    model_name: gpt-4
    api_key: ${OPENAI_API_KEY}
```

## How It Uses GitHub API

The agent calls the real GitHub API v3:

```python
# Get open PRs
GET /repos/{owner}/{repo}/pulls?state=open

# Get PR details
GET /repos/{owner}/{repo}/pulls/{number}

# Get PR files
GET /repos/{owner}/{repo}/pulls/{number}/files

# Post review comment
POST /repos/{owner}/{repo}/pulls/{number}/comments
```

Each request includes the GitHub token in the Authorization header for authentication.

## Learning Outcomes

After building this agent, you understand:

✅ How to register tools with NeMo Agent Toolkit  
✅ How ReAct agents reason and take actions  
✅ How to configure agents with YAML  
✅ How tool descriptions guide agent behavior  
✅ How to structure async tool functions  
✅ How to handle tool outputs  
✅ How to extend agents with new tools  
✅ How to swap LLMs and prompts  
✅ How agents can read AND write code  
✅ How to integrate GitHub API + git CLI  
✅ How to let agents automatically commit changes  
✅ How to design multi-step workflows (read → analyze → fix → commit)  

## Troubleshooting

### Agent doesn't use a tool
- Check tool description (in docstring)
- Verify tool is in `tool_names` in config
- Check system prompt mentions the capability

### Git operations fail (clone/checkout/push)
- Ensure git is installed: `git --version`
- Check GITHUB_TOKEN has repo access (need `repo` scope)
- Verify repo exists and is accessible
- Check git config: `git config --global user.email "you@example.com"`

### Write tool doesn't commit
- Check git is initialized: `ls -la /tmp/repo_name/.git`
- Verify branch was checked out: `git status` in `/tmp/repo_name`
- Check commit message isn't empty

### API rate limits
- GitHub allows 5000 API calls/hour
- Add delays between agent calls if hitting limits
- Use personal token instead of OAuth token

### Wrong LLM response
- Adjust `temperature` in config (0 = deterministic, 1 = creative)
- Update `system_prompt` with clearer instructions
- Try a different model

## Common Workflows

**Review and Suggest**
```bash
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Review PR #10. Identify 3 main issues and suggest fixes."
# Agent reviews, posts comments (no code changes)
```

**Review and Auto-Fix**
```bash
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Review PR #10 and automatically fix all issues you find."
# Agent reviews, writes code, commits changes
```

**Fix Specific Issue**
```bash
nat run --config_file github_pr_review_agent/configs/config.yml \
  --input "Fix the missing error handling in PR #10."
# Agent identifies and fixes, adds test cases
```

## Next Steps

1. **Better code analysis**: Add semantic understanding (AST parsing, linting)
2. **Test suite generation**: Auto-generate tests for changes
3. **Conflict handling**: Handle merge conflicts intelligently
4. **Rollback capability**: Revert commits if tests fail
5. **Multi-agent reviews**: Different agents for security, performance, style
6. **Feedback loop**: Learn from accepted/rejected fixes
7. **Production bot**: Deploy as a GitHub App

---

**Happy reviewing and fixing! 🚀**
