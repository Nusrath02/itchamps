import frappe
from frappe import _
from itchamps.api.github_helper import GitHubHelper

@frappe.whitelist()
def get_response(message):
    """
    Main chatbot endpoint - handles user messages and returns AI responses
    WITH ROLE-BASED ACCESS CONTROL
    """
    try:
        # Get current user and their roles
        user = frappe.session.user
        user_roles = frappe.get_roles(user)
        
        # Find employee record for current user
        employee = get_employee_for_user(user)

        # Handle GitHub-related queries (no RBAC needed)
        if any(keyword in message.lower() for keyword in ["github", "repo", "repository", "commit", "issue", "pull request", "pr", "branch", "contributor"]):
            return handle_github_query(message)
        
        # Handle employee-related queries with RBAC
        elif "leave" in message.lower():
            return handle_leave_query(message, employee, user, user_roles)
        elif "manager" in message.lower():
            return handle_manager_query(employee, user_roles)
        elif "employee" in message.lower() or "search" in message.lower():
            return handle_employee_search(message, employee, user_roles)
        elif "my info" in message.lower() or "my profile" in message.lower():
            return handle_my_info(employee, user)
        else:
            # Default AI response
            return {"message": get_help_message(user, user_roles)}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Chatbot Error")
        return {"message": f"Error: {str(e)}"}


def get_employee_for_user(user):
    """
    Find employee record for current user
    Tries multiple methods to link user to employee
    """
    employee = None
    
    # Method 1: Try by user_id field
    employee = frappe.db.get_value("Employee", {"user_id": user}, ["name", "employee_name", "department"], as_dict=True)
    
    # Method 2: Try by prefered_email
    if not employee:
        employee = frappe.db.get_value("Employee", {"prefered_email": user}, ["name", "employee_name", "department"], as_dict=True)
    
    # Method 3: Try by company_email
    if not employee:
        employee = frappe.db.get_value("Employee", {"company_email": user}, ["name", "employee_name", "department"], as_dict=True)
    
    # Method 4: Try by personal_email
    if not employee:
        employee = frappe.db.get_value("Employee", {"personal_email": user}, ["name", "employee_name", "department"], as_dict=True)
    
    return employee


def check_permission(user_roles, required_roles):
    """
    Check if user has any of the required roles
    
    Args:
        user_roles: List of roles user has
        required_roles: List of roles that can access this feature
    
    Returns:
        Boolean: True if user has permission
    """
    return any(role in user_roles for role in required_roles)


def can_view_all_employees(user_roles):
    """Check if user can view all employee data"""
    return check_permission(user_roles, ["HR Manager", "HR User", "System Manager", "Administrator"])


def can_edit_employees(user_roles):
    """Check if user can edit employee data"""
    return check_permission(user_roles, ["HR Manager", "System Manager", "Administrator"])


def is_manager(employee_id):
    """Check if employee is a manager (has team members)"""
    if not employee_id:
        return False
    team_count = frappe.db.count("Employee", {"reports_to": employee_id})
    return team_count > 0


def get_team_members(employee_id):
    """Get list of employee IDs reporting to this manager"""
    if not employee_id:
        return []
    return frappe.get_all("Employee", filters={"reports_to": employee_id}, pluck="name")


def handle_leave_query(message, employee, user, user_roles):
    """
    Handle leave-related queries with RBAC
    - Employees: Can only view their own leaves
    - Managers: Can view their team's leaves
    - HR/Admin: Can view all leaves
    """
    if not employee:
        return {"message": f"❌ **Employee record not found**\n\nNo employee record is linked to your user account: `{user}`\n\nPlease contact HR to link your employee record."}

    employee_id = employee.get("name")
    employee_name = employee.get("employee_name")
    
    # Check if user can view all employees
    can_view_all = can_view_all_employees(user_roles)
    is_mgr = is_manager(employee_id)
    
    # Determine what data user can access
    allowed_employees = [employee_id]  # Always can see own data
    
    if is_mgr:
        # Managers can see their team
        team = get_team_members(employee_id)
        allowed_employees.extend(team)
    
    # Check if user is trying to access restricted data
    wants_all_data = any(word in message.lower() for word in ["all", "everyone", "company"])
    wants_team_data = any(word in message.lower() for word in ["team", "department"])
    
    if wants_all_data and not can_view_all:
        return {"message": "🔒 **Access Denied**\n\nYou can only view your own leave information.\n\nFor company-wide data, please contact HR."}
    
    # Build response header
    if can_view_all and wants_all_data:
        response = f"**Leave Information - All Employees**\n\n"
        employee_filter = None  # No filter, show all
    elif is_mgr and wants_team_data:
        response = f"**Leave Information - Your Team**\n\n"
        employee_filter = allowed_employees
    else:
        response = f"**Leave Information for {employee_name}**\n\n"
        employee_filter = [employee_id]

    # Check if asking for pending applications
    if "pending" in message.lower() or "application" in message.lower():
        filters = {"status": ["in", ["Open", "Pending", "Submitted"]]}
        
        if employee_filter:
            filters["employee"] = ["in", employee_filter] if len(employee_filter) > 1 else employee_filter[0]
        
        pending_leaves = frappe.get_all(
            "Leave Application",
            filters=filters,
            fields=["name", "leave_type", "from_date", "to_date", "total_leave_days", "status", "posting_date", "employee", "employee_name"],
            order_by="posting_date desc"
        )
        
        if pending_leaves:
            response += "**📋 Pending Leave Applications:**\n\n"
            for leave in pending_leaves:
                # Show employee name if viewing multiple employees
                show_name = employee_filter is None or len(employee_filter) > 1
                emp_info = f" - {leave.employee_name}" if show_name else ""
                
                response += f"- **{leave.leave_type}**{emp_info}: {leave.from_date} to {leave.to_date}\n"
                response += f"  Days: {leave.total_leave_days} | Status: {leave.status}\n"
                response += f"  Application: {leave.name}\n\n"
        else:
            response += "✅ No pending leave applications.\n\n"
    
    # Show leave balance (only for own data)
    if not wants_all_data and not wants_team_data:
        leaves = frappe.get_all(
            "Leave Allocation",
            filters={
                "employee": employee_id,
                "docstatus": 1  # Only approved allocations
            },
            fields=["leave_type", "total_leaves_allocated", "new_leaves_allocated", "leave_balance", "from_date", "to_date"]
        )

        if leaves:
            response += "**📊 Your Leave Balance:**\n\n"
            for leave in leaves:
                remaining = leave.leave_balance if leave.leave_balance is not None else leave.total_leaves_allocated
                used = leave.total_leaves_allocated - remaining
                
                response += f"- **{leave.leave_type}**\n"
                response += f"  Total: {leave.total_leaves_allocated} | Used: {used} | **Remaining: {remaining}**\n"
                response += f"  Period: {leave.from_date} to {leave.to_date}\n\n"
        else:
            response += "No leave allocations found.\n\n"
    
    # Show recent leave history if requested
    if "history" in message.lower() or "recent" in message.lower():
        history_filters = {"employee": employee_id, "docstatus": 1}
        
        recent_leaves = frappe.get_all(
            "Leave Application",
            filters=history_filters,
            fields=["leave_type", "from_date", "to_date", "status", "total_leave_days"],
            order_by="from_date desc",
            limit=5
        )
        
        if recent_leaves:
            response += "**📜 Recent Leave History:**\n\n"
            for leave in recent_leaves:
                response += f"- **{leave.leave_type}**: {leave.from_date} to {leave.to_date} ({leave.total_leave_days} days) - {leave.status}\n"

    return {"message": response}


def handle_manager_query(employee, user_roles):
    """
    Handle manager-related queries
    All users can view their own manager
    """
    if not employee:
        return {"message": "❌ I couldn't find your employee record."}

    employee_id = employee.get("name")
    
    manager_id = frappe.db.get_value("Employee", employee_id, "reports_to")

    if manager_id:
        manager_details = frappe.db.get_value(
            "Employee",
            manager_id,
            ["employee_name", "user_id", "department", "designation", "company_email"],
            as_dict=True
        )
        
        if manager_details:
            response = f"**👤 Your Reporting Manager:**\n\n"
            response += f"- **Name**: {manager_details.employee_name}\n"
            response += f"- **Designation**: {manager_details.designation or 'N/A'}\n"
            response += f"- **Department**: {manager_details.department or 'N/A'}\n"
            response += f"- **Email**: {manager_details.company_email or manager_details.user_id or 'N/A'}\n\n"
            
            # Check if current employee is also a manager
            if is_manager(employee_id):
                team_count = frappe.db.count("Employee", {"reports_to": employee_id})
                response += f"\n**👥 You manage {team_count} team member(s)**"
            
            return {"message": response}

    return {"message": "No reporting manager found for your profile."}


def handle_employee_search(message, employee, user_roles):
    """
    Search for employees based on message content WITH RBAC
    - Employees: Can only see self, manager, and team
    - HR/Admin: Can search all employees
    """
    # Check permissions
    can_view_all = can_view_all_employees(user_roles)
    
    if not can_view_all:
        # Regular employees have limited visibility
        if not employee:
            return {"message": "❌ Employee record not found."}
        
        employee_id = employee.get("name")
        
        # Build allowed employee list
        allowed_employees = [employee_id]  # Self
        
        # Add manager
        manager_id = frappe.db.get_value("Employee", employee_id, "reports_to")
        if manager_id:
            allowed_employees.append(manager_id)
        
        # Add team members if manager
        team_members = get_team_members(employee_id)
        allowed_employees.extend(team_members)
        
        # Search only within allowed list
        employees = frappe.get_all(
            "Employee",
            filters={"name": ["in", allowed_employees]},
            fields=["employee_name", "department", "designation", "user_id", "company_email", "name"],
            limit=10
        )
        
        if not employees:
            return {"message": "🔒 **Limited Access**\n\nYou can only view:\n- Your profile\n- Your manager\n- Your team members (if you're a manager)\n\nFor other employees, please contact HR."}
        
        response = "**👥 Employees (Your Network):**\n\n"
        
        # Format response with relationships
        for emp in employees:
            email = emp.company_email or emp.user_id or "No email"
            
            # Show relationship
            relationship = ""
            if emp.name == employee_id:
                relationship = " (You)"
            elif emp.name == manager_id:
                relationship = " (Your Manager)"
            elif emp.name in team_members:
                relationship = " (Your Team)"
            
            response += f"- **{emp.employee_name}**{relationship}\n"
            response += f"  {emp.designation or 'N/A'} - {emp.department or 'N/A'}\n"
            response += f"  📧 {email}\n\n"
        
    else:
        # HR/Admin can search all employees
        # Extract search terms
        search_term = message.lower().replace("employee", "").replace("search", "").replace("find", "").strip()
        
        filters = {}
        
        # Check for department search
        if "department" in message.lower() or "dept" in message.lower():
            words = search_term.split()
            for word in words:
                dept = word.capitalize()
                if dept in ["Marketing", "Sales", "HR", "IT", "Finance", "Operations", "Engineering", "Support"]:
                    filters["department"] = dept
        
        employees = frappe.get_all(
            "Employee",
            filters=filters,
            fields=["employee_name", "department", "designation", "user_id", "company_email", "name"],
            limit=10
        )
        
        if not employees:
            return {"message": "No employees found matching your criteria."}
        
        response = "**👥 Employees Found:**\n\n"
        
        for emp in employees:
            email = emp.company_email or emp.user_id or "No email"
            response += f"- **{emp.employee_name}**\n"
            response += f"  {emp.designation or 'N/A'} - {emp.department or 'N/A'}\n"
            response += f"  📧 {email}\n\n"

    return {"message": response}


def handle_my_info(employee, user):
    """
    Show current user's profile information
    Always allowed - users can see their own data
    """
    if not employee:
        return {"message": f"❌ **Employee record not found**\n\nNo employee record is linked to: `{user}`"}
    
    employee_id = employee.get("name")
    
    # Get full employee details
    emp_details = frappe.get_doc("Employee", employee_id)
    
    response = f"**👤 Your Profile Information**\n\n"
    response += f"- **Name**: {emp_details.employee_name}\n"
    response += f"- **Employee ID**: {emp_details.name}\n"
    response += f"- **Department**: {emp_details.department or 'N/A'}\n"
    response += f"- **Designation**: {emp_details.designation or 'N/A'}\n"
    response += f"- **Date of Joining**: {emp_details.date_of_joining or 'N/A'}\n"
    response += f"- **Email**: {emp_details.company_email or emp_details.user_id or 'N/A'}\n"
    response += f"- **Status**: {emp_details.status}\n"
    
    if emp_details.reports_to:
        manager_name = frappe.db.get_value("Employee", emp_details.reports_to, "employee_name")
        response += f"- **Reports To**: {manager_name}\n"
    
    # Check if manager
    if is_manager(employee_id):
        team_count = frappe.db.count("Employee", {"reports_to": employee_id})
        response += f"- **Team Size**: {team_count} member(s)\n"
    
    return {"message": response}


def get_help_message(user, user_roles):
    """
    Return help message based on user's roles
    """
    can_view_all = can_view_all_employees(user_roles)
    
    base_help = f"Hi! I'm your AI assistant.\n\n**You can ask me about:**\n\n"
    base_help += "- **Your Leaves**: 'Show my leave balance', 'Pending leave applications'\n"
    base_help += "- **Your Manager**: 'Who is my manager?'\n"
    base_help += "- **Your Profile**: 'Show my info'\n"
    
    if can_view_all:
        base_help += "- **All Employees**: 'Search employees in IT', 'Show all pending leaves'\n"
        base_help += "- **Reports**: 'Show team leaves', 'Department statistics'\n"
    else:
        base_help += "- **Your Network**: 'Show my team', 'Find my manager'\n"
    
    base_help += "- **GitHub**: Repository info, commits, issues, PRs\n\n"
    base_help += f"**Current User:** {user}\n"
    base_help += f"**Your Roles:** {', '.join(user_roles)}"
    
    return base_help


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