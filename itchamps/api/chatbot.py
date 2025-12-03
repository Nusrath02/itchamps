import frappe
from frappe import _

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

        # Example queries you can handle:
        if "leave" in message.lower():
            return handle_leave_query(message, employee)
        elif "manager" in message.lower():
            return handle_manager_query(employee)
        elif "employee" in message.lower():
            return handle_employee_search(message)
        else:
            # Default AI response (you can integrate OpenAI/Claude here)
            return {"message": "I understand you're asking about: " + message}

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
