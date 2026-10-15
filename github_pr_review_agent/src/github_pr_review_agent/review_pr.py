import subprocess
from pathlib import Path

import requests
from pydantic import Field

from nat.builder.builder import Builder
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.function import FunctionBaseConfig


class ReviewPRConfig(FunctionBaseConfig, name="review_pr"):
    """Config for the GitHub PR review tools."""
    github_token: str = Field(description="GitHub personal access token.")
    repo_owner: str = Field(description="Repository owner (username or org).")
    repo_name: str = Field(description="Repository name.")


class GitHubTools:
    """Tools to interact with real GitHub PRs via GitHub API."""

    def __init__(self, github_token: str, repo_owner: str, repo_name: str):
        self.token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.repo_path = Path(f"/tmp/{repo_name}")
        self.current_pr = None

    def _get(self, endpoint: str) -> dict:
        """Make a GET request to GitHub API."""
        url = f"{self.base_url}{endpoint}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 404:
            return {"error": "Not found"}
        if resp.status_code != 200:
            return {"error": f"GitHub API error: {resp.status_code}"}
        return resp.json()

    def list_open_prs(self) -> str:
        """List all open PRs available for review."""
        data = self._get("/pulls?state=open&per_page=10")
        if "error" in data:
            return data["error"]

        prs = []
        for pr in data:
            prs.append(f"PR #{pr['number']}: {pr['title']} by {pr['user']['login']}")
        return "\n".join(prs) if prs else "No open PRs found"

    def get_pr_info(self, pr_number: int) -> str:
        """Get basic info about a specific PR: title, description, author."""
        data = self._get(f"/pulls/{pr_number}")
        if "error" in data:
            return data["error"]

        return f"""PR #{data['number']}: {data['title']}
Author: {data['user']['login']}
Description: {data['body'][:500]}...
Files changed: {data['changed_files']}
Additions: {data['additions']}, Deletions: {data['deletions']}"""

    def get_pr_files(self, pr_number: int) -> str:
        """Get list of changed files in a PR with stats."""
        data = self._get(f"/pulls/{pr_number}/files?per_page=30")
        if "error" in data:
            return data["error"]

        result = []
        for f in data:
            result.append(f"{f['filename']} (+{f['additions']}/-{f['deletions']} lines)")
        return "\n".join(result) if result else "No files changed"

    def get_file_diff(self, pr_number: int, filename: str) -> str:
        """Get the diff for a specific file in a PR."""
        data = self._get(f"/pulls/{pr_number}/files?per_page=100")
        if "error" in data:
            return data["error"]

        for f in data:
            if f["filename"] == filename:
                return f.get("patch", "No patch available")
        return f"File {filename} not found in PR"

    def clone_repo(self) -> str:
        """Clone the repo (skip if already cloned)."""
        if self.repo_path.exists():
            return f"✓ Repo already cloned at {self.repo_path}"

        url = f"https://{self.token}@github.com/{self.repo_owner}/{self.repo_name}.git"
        try:
            subprocess.run(["git", "clone", url, str(self.repo_path)], check=True, capture_output=True)
            return f"✓ Cloned repo to {self.repo_path}"
        except subprocess.CalledProcessError as e:
            return f"✗ Failed to clone: {e.stderr.decode()}"

    def checkout_pr(self, pr_number: int) -> str:
        """Check out the PR branch locally."""
        try:
            pr_data = self._get(f"/pulls/{pr_number}")
            if "error" in pr_data:
                return pr_data["error"]
            branch = pr_data["head"]["ref"]
            self.current_pr = pr_number

            subprocess.run(
                ["git", "fetch", "origin", branch],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "checkout", branch],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            return f"✓ Checked out branch: {branch}"
        except subprocess.CalledProcessError as e:
            return f"✗ Failed to checkout: {e.stderr.decode()}"

    def write_file(self, filepath: str, content: str) -> str:
        """Write content to a file in the repo."""
        try:
            full_path = self.repo_path / filepath
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            return f"✓ Wrote {filepath} ({len(content)} chars)"
        except Exception as e:
            return f"✗ Failed to write file: {e}"

    def commit_and_push(self, message: str) -> str:
        """Commit all changes and push to the PR branch."""
        try:
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "push"],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            return f"✓ Committed and pushed: {message}"
        except subprocess.CalledProcessError as e:
            return f"✗ Failed to push: {e.stderr.decode()}"

    def review_file(self, pr_number: int, filename: str, comment: str) -> str:
        """Submit a review comment on a specific file."""
        # Post review comment to PR
        url = f"{self.base_url}/pulls/{pr_number}/comments"
        payload = {
            "body": comment,
            "commit_id": self._get(f"/pulls/{pr_number}")["head"]["sha"],
            "path": filename,
            "line": 1  # ponytail: simplified, would need actual line number
        }
        resp = requests.post(url, json=payload, headers=self.headers)
        if resp.status_code == 201:
            return f"✓ Posted review comment on {filename} in PR #{pr_number}"
        return f"Failed to post comment: {resp.status_code}"


@register_function(config_type=ReviewPRConfig)
async def review_pr(config: ReviewPRConfig, builder: Builder):
    """Register GitHub PR review tools with the agent."""
    tools = GitHubTools(config.github_token, config.repo_owner, config.repo_name)

    async def _list_prs() -> str:
        """List all open PRs available for review."""
        return tools.list_open_prs()

    async def _get_pr_info(pr_number: int) -> str:
        """Get PR details: title, author, description, and file statistics."""
        return tools.get_pr_info(pr_number)

    async def _get_files(pr_number: int) -> str:
        """Get list of files changed in a PR with added/deleted line counts."""
        return tools.get_pr_files(pr_number)

    async def _get_diff(pr_number: int, filename: str) -> str:
        """Get the actual code diff for a specific file in the PR."""
        return tools.get_file_diff(pr_number, filename)

    async def _submit_comment(pr_number: int, filename: str, comment: str) -> str:
        """Submit a review comment on a specific file."""
        return tools.review_file(pr_number, filename, comment)

    async def _clone() -> str:
        """Clone the GitHub repository locally to make changes."""
        return tools.clone_repo()

    async def _checkout(pr_number: int) -> str:
        """Check out the specific PR branch for editing."""
        return tools.checkout_pr(pr_number)

    async def _write(filepath: str, content: str) -> str:
        """Write code/text to a file in the cloned repo. Use relative paths like 'src/main.py'."""
        return tools.write_file(filepath, content)

    async def _commit(message: str) -> str:
        """Commit all changes and push to the PR branch."""
        return tools.commit_and_push(message)

    # Yield each tool as FunctionInfo
    yield FunctionInfo.from_fn(_list_prs, description=_list_prs.__doc__)
    yield FunctionInfo.from_fn(_get_pr_info, description=_get_pr_info.__doc__)
    yield FunctionInfo.from_fn(_get_files, description=_get_files.__doc__)
    yield FunctionInfo.from_fn(_get_diff, description=_get_diff.__doc__)
    yield FunctionInfo.from_fn(_submit_comment, description=_submit_comment.__doc__)
    yield FunctionInfo.from_fn(_clone, description=_clone.__doc__)
    yield FunctionInfo.from_fn(_checkout, description=_checkout.__doc__)
    yield FunctionInfo.from_fn(_write, description=_write.__doc__)
    yield FunctionInfo.from_fn(_commit, description=_commit.__doc__)
