import frappe
from frappe import _
from itchamps.api.constants import UserRole
from itchamps.api.constants import UserRole
from itchamps.api.auth_service import AuthService
from itchamps.api.auth_service import AuthService
from itchamps.api.nlu import IntentParser



@frappe.whitelist()
def get_response(message):
    """
    Main chatbot endpoint - handles user messages and returns AI responses
    """
    try:
        # Get current user context (Rich Object)
        context = AuthService.get_user_context()
        
        if not context:
            return {"message": "Please log in to use the AI Assistant."}

        user_id = context['user']['id']
        user_name = context['user']['full_name']
        employee = context['employee']  # Can be None if no employee linked
        
        
        # 1. Detect Intent
        intent, confidence = IntentParser.detect_intent(message)
        entities = IntentParser.extract_entities(message)

        # 2. Route based on Intent
        if intent == "leave_balance":
            return handle_leave_query(message, employee, user_name)
        elif intent == "leave_history":
            # Add 'history' to context for handler
            return handle_leave_query("history", employee, user_name)
        elif intent == "leave_apply":
             # Placeholder for application logic (handled by same function for now or new one)
            return handle_leave_query("pending", employee, user_name)
        elif intent == "manager_info":
            return handle_manager_query(employee)
        elif intent == "employee_search":
            return handle_employee_search(message, user_id)
        elif intent == "my_info":
            return handle_my_info(employee, user_name)
        else:
            return {"message": f"Hi **{user_name}**! I'm your AI assistant.\n\n**You can ask me about:**\n\n- **Leaves**: 'Show my leave balance', 'Pending leave applications'\n- **Manager**: 'Who is my manager?'\n- **Profile**: 'Show my info'\n- **Employees**: Search for employees"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Chatbot Error")
        return {"message": f"Error: {str(e)}"}


def handle_leave_query(message, employee, user):
    """Handle leave-related queries with detailed information"""
    if not employee:
        return {"message": f"❌ **Employee record not found**\n\nNo employee record is linked to your user account: `{user}`\n\nPlease contact HR to link your employee record."}

    employee_id = employee.get("name")
    employee_name = employee.get("employee_name")
    
    response = f"**Leave Information for {employee_name}**\n\n"

    # Check if asking for pending applications
    if "pending" in message.lower() or "application" in message.lower():
        pending_leaves = frappe.get_all(
            "Leave Application",
            filters={
                "employee": employee_id,
                "status": ["in", ["Open", "Pending", "Submitted"]]
            },
            fields=["name", "leave_type", "from_date", "to_date", "total_leave_days", "status", "posting_date"],
            order_by="posting_date desc"
        )
        
        if pending_leaves:
            response += "**📋 Pending Leave Applications:**\n\n"
            for leave in pending_leaves:
                response += f"- **{leave.leave_type}**: {leave.from_date} to {leave.to_date}\n"
                response += f"  Days: {leave.total_leave_days} | Status: {leave.status}\n"
                response += f"  Application: {leave.name}\n\n"
        else:
            response += "✅ No pending leave applications.\n\n"
    
    # Show leave balance
    leaves = frappe.get_all(
        "Leave Allocation",
        filters={
            "employee": employee_id,
            "docstatus": 1  # Only approved allocations
        },
        fields=["leave_type", "total_leaves_allocated", "new_leaves_allocated", "leave_balance", "from_date", "to_date"]
    )

    if leaves:
        response += "**📊 Leave Balance:**\n\n"
        for leave in leaves:
            # Get actual leave balance
            remaining = leave.leave_balance if leave.leave_balance is not None else leave.total_leaves_allocated
            used = leave.total_leaves_allocated - remaining
            
            response += f"- **{leave.leave_type}**\n"
            response += f"  Total: {leave.total_leaves_allocated} | Used: {used} | **Remaining: {remaining}**\n"
            response += f"  Period: {leave.from_date} to {leave.to_date}\n\n"
    else:
        response += "No leave allocations found.\n\n"
    
    # Show recent leave history if requested
    if "history" in message.lower() or "recent" in message.lower():
        recent_leaves = frappe.get_all(
            "Leave Application",
            filters={
                "employee": employee_id,
                "docstatus": 1  # Submitted/Approved
            },
            fields=["leave_type", "from_date", "to_date", "status", "total_leave_days"],
            order_by="from_date desc",
            limit=5
        )
        
        if recent_leaves:
            response += "**📜 Recent Leave History:**\n\n"
            for leave in recent_leaves:
                response += f"- **{leave.leave_type}**: {leave.from_date} to {leave.to_date} ({leave.total_leave_days} days) - {leave.status}\n"

    return {"message": response}


def handle_manager_query(employee):
    """Handle manager-related queries"""
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
            return {
                "message": f"**👤 Your Reporting Manager:**\n\n"
                          f"- **Name**: {manager_details.employee_name}\n"
                          f"- **Designation**: {manager_details.designation or 'N/A'}\n"
                          f"- **Department**: {manager_details.department or 'N/A'}\n"
                          f"- **Email**: {manager_details.company_email or manager_details.user_id or 'N/A'}"
            }

    return {"message": "No reporting manager found for your profile."}


def handle_employee_search(message, user):
    """Search for employees based on message content"""
    
    # Permission Check
    allowed_roles = [UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.HR_USER, UserRole.MANAGER]
    has_permission = any(UserRole.has_role(user, role) for role in allowed_roles)
    
    if not has_permission:
        # If user is not HR/Manager, they can ONLY see themselves.
        # But 'handle_my_info' is better for that.
        # Here we just deny broad search.
        return {"message": "⛔ **Access Denied**\n\nYou are not authorized to search for other employees. You can only view your own profile."}

    # Extract search terms
    search_term = message.lower().replace("employee", "").replace("search", "").replace("find", "").strip()
    
    filters = {}
    
    # Check for department search
    if "department" in message.lower() or "dept" in message.lower():
        # Try to extract department name
        words = search_term.split()
        for word in words:
            if word.capitalize() in ["Marketing", "Sales", "HR", "IT", "Finance", "Operations"]:
                filters["department"] = word.capitalize()
    
    employees = frappe.get_all(
        "Employee",
        filters=filters,
        fields=["employee_name", "department", "designation", "user_id", "company_email"],


def handle_my_info(employee, user):
    """Show current user's profile information"""
    if not employee:
        return {"message": f"❌ **Employee record not found**\n\nNo employee record is linked to: `{user}`"}
    
    employee_id = employee.get("name")
    
    # Get full employee details (Ignore permissions because we already validated the link)
    emp_details = frappe.get_doc("Employee", employee_id, ignore_permissions=True)
    
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
    
    return {"message": response}


