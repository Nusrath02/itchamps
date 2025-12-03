import frappe
from frappe import _
from itchamps.api.github_helper import GitHubHelper

@frappe.whitelist()
def get_response(message):
    """
    Main chatbot endpoint - handles user messages and returns AI responses
    """
    try:
        # Get current user
        user = frappe.session.user

        # Example: Fetch user's employee record
        employee = frappe.get_value("Employee", {"user_id": user}, ["name", "employee_name", "department"])

        # Handle GitHub-related queries
        if any(keyword in message.lower() for keyword in ["github", "repo", "repository", "commit", "issue", "pull request", "pr", "branch", "contributor"]):
            return handle_github_query(message)
        # Handle employee-related queries
        elif "leave" in message.lower():
            return handle_leave_query(message, employee)
        elif "manager" in message.lower():
            return handle_manager_query(employee)
        elif "employee" in message.lower():
            return handle_employee_search(message)
        else:
            # Default AI response (you can integrate OpenAI/Claude here)
            return {"message": "I understand you're asking about: " + message + "\n\nYou can ask me about:\n- GitHub repository info, commits, issues, PRs\n- Leave balance and applications\n- Manager information\n- Employee search"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Chatbot Error")
        return {"message": f"Error: {str(e)}"}


def handle_leave_query(message, employee):
    """Handle leave-related queries"""
    if not employee:
        return {"message": "I couldn't find your employee record."}

    # You can use message parameter for more specific queries
    # Example: check if user is asking for specific leave type
    # if "sick" in message.lower(): filter by sick leave

    # Fetch leave balance
    leaves = frappe.get_all(
        "Leave Allocation",
        filters={"employee": employee[0]},
        fields=["leave_type", "total_leaves_allocated", "leaves_taken"]
    )

    response = f"**Your Leave Balance:**\n\n"
    for leave in leaves:
        remaining = leave.total_leaves_allocated - leave.leaves_taken
        response += f"- **{leave.leave_type}**: {remaining} days remaining\n"

    return {"message": response}


def handle_manager_query(employee):
    """Handle manager-related queries"""
    if not employee:
        return {"message": "I couldn't find your employee record."}

    manager = frappe.get_value(
        "Employee",
        employee[0],
        ["reports_to"],
        as_dict=True
    )

    if manager and manager.reports_to:
        manager_details = frappe.get_doc("Employee", manager.reports_to)
        return {
            "message": f"**Your Reporting Manager:**\n\n"
                      f"- **Name**: {manager_details.employee_name}\n"
                      f"- **Email**: {manager_details.user_id}\n"
                      f"- **Department**: {manager_details.department}"
        }

    return {"message": "No reporting manager found."}


def handle_employee_search(message):
    """Search for employees"""
    # Extract department or name from message
    employees = frappe.get_all(
        "Employee",
        fields=["employee_name", "department", "designation", "user_id"],
        limit=5
    )

    response = "**Employees Found:**\n\n"
    for emp in employees:
        response += f"- **{emp.employee_name}** ({emp.designation}) - {emp.department}\n"

    return {"message": response}


def handle_github_query(message):
    """Handle GitHub-related queries"""
    try:
        github = GitHubHelper(owner="Nusrath02", repo="itchamps")
        message_lower = message.lower()

        # Repository information
        if any(word in message_lower for word in ["repo info", "repository info", "about repo", "repo details"]):
            info = github.get_repository_info()
            if info:
                response = f"""**Repository Information:**

- **Name**: {info['name']}
- **Description**: {info['description'] or 'No description'}
- **Language**: {info['language']}
- **Stars**: ⭐ {info['stars']}
- **Forks**: 🍴 {info['forks']}
- **Open Issues**: 🐛 {info['open_issues']}
- **URL**: [View on GitHub]({info['url']})
- **Created**: {info['created_at'][:10]}
- **Last Updated**: {info['updated_at'][:10]}"""
                return {"message": response}

        # Recent commits
        elif any(word in message_lower for word in ["commit", "recent commit", "latest commit"]):
            commits = github.get_commits(limit=5)
            if commits:
                response = "**Recent Commits:**\n\n"
                for commit in commits:
                    response += f"- **{commit['sha']}** by {commit['author']}\n"
                    response += f"  {commit['message'].split(chr(10))[0]}\n"
                    response += f"  [{commit['date'][:10]}]({commit['url']})\n\n"
                return {"message": response}

        # Issues
        elif "issue" in message_lower:
            state = "closed" if "closed" in message_lower else "open"
            issues = github.get_issues(state=state, limit=5)
            if issues:
                response = f"**{state.capitalize()} Issues:**\n\n"
                for issue in issues:
                    labels = ", ".join(issue['labels']) if issue['labels'] else "No labels"
                    response += f"- **#{issue['number']}**: {issue['title']}\n"
                    response += f"  By {issue['author']} | Labels: {labels}\n"
                    response += f"  [View Issue]({issue['url']})\n\n"
                return {"message": response}
            else:
                return {"message": f"No {state} issues found."}

        # Pull Requests
        elif any(word in message_lower for word in ["pull request", "pr", "pull requests", "prs"]):
            state = "closed" if "closed" in message_lower else "open"
            prs = github.get_pull_requests(state=state, limit=5)
            if prs:
                response = f"**{state.capitalize()} Pull Requests:**\n\n"
                for pr in prs:
                    status = "✅ Merged" if pr['merged'] else f"📝 {pr['state'].capitalize()}"
                    response += f"- **#{pr['number']}**: {pr['title']}\n"
                    response += f"  By {pr['author']} | {status}\n"
                    response += f"  [View PR]({pr['url']})\n\n"
                return {"message": response}
            else:
                return {"message": f"No {state} pull requests found."}

        # Branches
        elif "branch" in message_lower:
            branches = github.get_branches(limit=10)
            if branches:
                response = "**Repository Branches:**\n\n"
                for branch in branches:
                    protected = "🔒 Protected" if branch['protected'] else ""
                    response += f"- **{branch['name']}** {protected}\n"
                    response += f"  Latest commit: {branch['commit_sha']}\n\n"
                return {"message": response}

        # Contributors
        elif "contributor" in message_lower:
            contributors = github.get_contributors(limit=10)
            if contributors:
                response = "**Top Contributors:**\n\n"
                for contributor in contributors:
                    response += f"- **{contributor['login']}**: {contributor['contributions']} contributions\n"
                    response += f"  [Profile]({contributor['profile_url']})\n\n"
                return {"message": response}

        # Default GitHub help
        else:
            return {"message": """**GitHub Commands:**

I can help you with the following GitHub queries:

- "Show repo info" - Repository details
- "Show recent commits" - Latest commits
- "Show open issues" - Open issues
- "Show closed issues" - Closed issues
- "Show pull requests" - Open PRs
- "Show branches" - Repository branches
- "Show contributors" - Top contributors

Just ask me anything about the itchamps GitHub repository!"""}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "GitHub Query Error")
        return {"message": f"GitHub Error: {str(e)}\n\nMake sure GitHub API is accessible."}
