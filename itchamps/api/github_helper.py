"""
GitHub API Helper Module
Handles interactions with GitHub API for the itchamps repository
"""
import requests
import frappe
from frappe import _

class GitHubHelper:
    """Helper class for GitHub API interactions"""

    def __init__(self, owner="Nusrath02", repo="itchamps"):
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.repo_url = f"{self.base_url}/repos/{owner}/{repo}"

        # Get GitHub token from site config or environment
        self.token = frappe.conf.get('github_token') or None
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def _make_request(self, endpoint, method="GET", data=None):
        """Make HTTP request to GitHub API"""
        url = f"{self.repo_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data, timeout=10)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"GitHub API Error: {str(e)}", "GitHub API")
            return None

    def get_repository_info(self):
        """Get basic repository information"""
        data = self._make_request("")
        if data:
            return {
                "name": data.get("name"),
                "description": data.get("description"),
                "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "open_issues": data.get("open_issues_count"),
                "language": data.get("language"),
                "url": data.get("html_url"),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at")
            }
        return None

    def get_commits(self, limit=5):
        """Get recent commits"""
        data = self._make_request(f"/commits?per_page={limit}")
        if data:
            commits = []
            for commit in data:
                commits.append({
                    "sha": commit.get("sha", "")[:7],
                    "message": commit.get("commit", {}).get("message", ""),
                    "author": commit.get("commit", {}).get("author", {}).get("name", ""),
                    "date": commit.get("commit", {}).get("author", {}).get("date", ""),
                    "url": commit.get("html_url", "")
                })
            return commits
        return []

    def get_issues(self, state="open", limit=5):
        """Get repository issues"""
        data = self._make_request(f"/issues?state={state}&per_page={limit}")
        if data:
            issues = []
            for issue in data:
                # Skip pull requests
                if "pull_request" in issue:
                    continue
                issues.append({
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "author": issue.get("user", {}).get("login", ""),
                    "created_at": issue.get("created_at"),
                    "url": issue.get("html_url"),
                    "labels": [label.get("name") for label in issue.get("labels", [])]
                })
            return issues
        return []

    def get_pull_requests(self, state="open", limit=5):
        """Get repository pull requests"""
        data = self._make_request(f"/pulls?state={state}&per_page={limit}")
        if data:
            prs = []
            for pr in data:
                prs.append({
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "state": pr.get("state"),
                    "author": pr.get("user", {}).get("login", ""),
                    "created_at": pr.get("created_at"),
                    "url": pr.get("html_url"),
                    "merged": pr.get("merged", False)
                })
            return prs
        return []

    def get_branches(self, limit=5):
        """Get repository branches"""
        data = self._make_request(f"/branches?per_page={limit}")
        if data:
            branches = []
            for branch in data:
                branches.append({
                    "name": branch.get("name"),
                    "protected": branch.get("protected", False),
                    "commit_sha": branch.get("commit", {}).get("sha", "")[:7]
                })
            return branches
        return []

    def get_contributors(self, limit=5):
        """Get repository contributors"""
        data = self._make_request(f"/contributors?per_page={limit}")
        if data:
            contributors = []
            for contributor in data:
                contributors.append({
                    "login": contributor.get("login"),
                    "contributions": contributor.get("contributions"),
                    "avatar_url": contributor.get("avatar_url"),
                    "profile_url": contributor.get("html_url")
                })
            return contributors
        return []

    def search_code(self, query, limit=5):
        """Search code in the repository"""
        search_url = f"{self.base_url}/search/code?q={query}+repo:{self.owner}/{self.repo}&per_page={limit}"
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("items"):
                results = []
                for item in data["items"]:
                    results.append({
                        "name": item.get("name"),
                        "path": item.get("path"),
                        "url": item.get("html_url")
                    })
                return results
        except requests.exceptions.RequestException as e:
            frappe.log_error(f"GitHub Code Search Error: {str(e)}", "GitHub API")
        return []

    def get_file_content(self, file_path):
        """Get content of a specific file"""
        data = self._make_request(f"/contents/{file_path}")
        if data:
            import base64
            content = data.get("content", "")
            if content:
                try:
                    decoded_content = base64.b64decode(content).decode('utf-8')
                    return {
                        "path": data.get("path"),
                        "content": decoded_content[:500],  # Limit content length
                        "size": data.get("size"),
                        "url": data.get("html_url")
                    }
                except Exception as e:
                    frappe.log_error(f"Error decoding file: {str(e)}", "GitHub API")
        return None


@frappe.whitelist()
def get_github_data(query_type, **kwargs):
    """
    Frappe whitelisted method to get GitHub data

    Args:
        query_type: Type of query (repo_info, commits, issues, prs, branches, contributors, search)
        **kwargs: Additional parameters based on query_type
    """
    try:
        github = GitHubHelper()

        if query_type == "repo_info":
            return github.get_repository_info()
        elif query_type == "commits":
            limit = kwargs.get("limit", 5)
            return github.get_commits(limit)
        elif query_type == "issues":
            state = kwargs.get("state", "open")
            limit = kwargs.get("limit", 5)
            return github.get_issues(state, limit)
        elif query_type == "prs":
            state = kwargs.get("state", "open")
            limit = kwargs.get("limit", 5)
            return github.get_pull_requests(state, limit)
        elif query_type == "branches":
            limit = kwargs.get("limit", 5)
            return github.get_branches(limit)
        elif query_type == "contributors":
            limit = kwargs.get("limit", 5)
            return github.get_contributors(limit)
        elif query_type == "search":
            query = kwargs.get("query", "")
            limit = kwargs.get("limit", 5)
            return github.search_code(query, limit)
        elif query_type == "file":
            file_path = kwargs.get("file_path", "")
            return github.get_file_content(file_path)
        else:
            return {"error": "Invalid query type"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "GitHub API Error")
        return {"error": str(e)}
