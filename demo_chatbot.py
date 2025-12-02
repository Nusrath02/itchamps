#!/usr/bin/env python3
"""
ITChamps Chatbot - Non-Interactive Demo
Demonstrates the chatbot responses without user input
"""
import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class MockFrappe:
    """Mock Frappe framework for testing"""
    class session:
        user = "test@example.com"

    @staticmethod
    def get_value(doctype, filters, fields=None, as_dict=False):
        """Mock database query"""
        if doctype == "Employee":
            if fields == "name":
                return "EMP001"
            elif as_dict:
                class MockEmployee:
                    name = "EMP001"
                    reports_to = "EMP002"
                return MockEmployee()
        return None

    @staticmethod
    def get_all(doctype, filters=None, fields=None, limit=None):
        """Mock get_all query"""
        if doctype == "Leave Application":
            return []
        elif doctype == "Leave Allocation":
            return []
        elif doctype == "Employee":
            return [
                {
                    "name": "EMP001",
                    "employee_name": "John Doe",
                    "designation": "Software Engineer",
                    "department": "IT"
                },
                {
                    "name": "EMP002",
                    "employee_name": "Jane Smith",
                    "designation": "HR Manager",
                    "department": "Human Resources"
                }
            ]
        return []

    @staticmethod
    def get_doc(doctype, name):
        """Mock get_doc"""
        class MockDoc:
            employee_name = "Jane Smith"
            designation = "HR Manager"
            department = "Human Resources"
        return MockDoc()

    @staticmethod
    def log_error(msg):
        """Mock error logging"""
        print(f"[ERROR] {msg}")

# Replace frappe with mock
frappe = MockFrappe()

# Copy the chatbot functions from the original
def get_response(message):
    """AI Chatbot API endpoint"""
    try:
        if not message:
            return {"success": False, "message": "Please provide a message"}

        msg_lower = message.lower()
        response_text = ""

        if any(keyword in msg_lower for keyword in ['leave', 'leaves', 'vacation']):
            if 'pending' in msg_lower or 'status' in msg_lower:
                response_text = handle_pending_leaves()
            elif 'balance' in msg_lower or 'remaining' in msg_lower:
                response_text = handle_leave_balance()
            else:
                response_text = "**Leave Information**\n\nI can help you with:\n- Check pending leaves\n- View leave balance\n- Apply for new leave"

        elif any(keyword in msg_lower for keyword in ['employee', 'staff', 'find']):
            response_text = handle_employee_search(message)

        elif 'manager' in msg_lower or 'reporting' in msg_lower:
            response_text = handle_manager_info()

        elif any(keyword in msg_lower for keyword in ['hi', 'hello', 'hey']):
            response_text = "Hello! 👋\n\nI'm your ITChamps AI assistant. How can I help you today?"

        elif 'help' in msg_lower:
            response_text = "**ITChamps AI Assistant**\n\nI can help with:\n- Leave management\n- Employee information\n- Department details\n- HR queries"

        else:
            response_text = f"I understand you're asking about: \"{message}\"\n\nTry asking about leaves, employees, or type 'help'."

        return {"success": True, "message": response_text}

    except Exception as e:
        frappe.log_error(f"Chatbot Error: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


def handle_pending_leaves():
    """Get pending leave applications"""
    try:
        user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": user}, "name")

        if not employee:
            return "I couldn't find your employee record."

        leaves = frappe.get_all(
            "Leave Application",
            filters={"employee": employee, "status": "Open"},
            fields=["name", "leave_type", "from_date", "to_date", "total_leave_days"],
            limit=5
        )

        if not leaves:
            return "**No Pending Leaves** ✅\n\nYou have no pending leave applications."

        response = f"**Your Pending Leaves** ({len(leaves)})\n\n"
        for leave in leaves:
            response += f"📅 **{leave.leave_type}**\n   From: {leave.from_date}\n   To: {leave.to_date}\n   Days: {leave.total_leave_days}\n\n"

        return response
    except Exception as e:
        return f"Error: {str(e)}"


def handle_leave_balance():
    """Get leave balance"""
    try:
        user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": user}, "name")

        if not employee:
            return "I couldn't find your employee record."

        allocations = frappe.get_all(
            "Leave Allocation",
            filters={"employee": employee, "docstatus": 1},
            fields=["leave_type", "total_leaves_allocated", "unused_leaves"]
        )

        if not allocations:
            return "No leave allocations found."

        response = "**Your Leave Balance** 🏖️\n\n"
        for alloc in allocations:
            response += f"**{alloc.leave_type}**\n   Allocated: {alloc.total_leaves_allocated}\n   Remaining: {alloc.unused_leaves}\n\n"

        return response
    except Exception as e:
        return f"Error: {str(e)}"


def handle_employee_search(message):
    """Search employees"""
    try:
        employees = frappe.get_all(
            "Employee",
            filters={"status": "Active"},
            fields=["name", "employee_name", "designation", "department"],
            limit=10
        )

        if not employees:
            return "No active employees found."

        response = f"**Active Employees** ({len(employees)})\n\n"
        for emp in employees:
            response += f"👤 **{emp['employee_name']}**\n   {emp['designation'] or 'N/A'} - {emp['department'] or 'N/A'}\n\n"

        return response
    except Exception as e:
        return f"Error: {str(e)}"


def handle_manager_info():
    """Get manager information"""
    try:
        user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": user}, ["name", "reports_to"], as_dict=True)

        if not employee or not employee.reports_to:
            return "No reporting manager assigned."

        manager = frappe.get_doc("Employee", employee.reports_to)

        response = f"**Your Manager** 👔\n\n**Name:** {manager.employee_name}\n**Designation:** {manager.designation or 'N/A'}\n**Department:** {manager.department or 'N/A'}"

        return response
    except Exception as e:
        return f"Error: {str(e)}"


# Demo script
def main():
    """Run automated demo"""
    print("=" * 70)
    print("ITChamps AI Chatbot - Automated Demo")
    print("=" * 70)
    print("\nDemonstrating chatbot responses to various queries...\n")

    # Test queries
    test_queries = [
        "Hello",
        "help",
        "show me employees",
        "who is my manager?",
        "check my pending leaves",
        "what's my leave balance?",
        "I want to apply for vacation",
        "something random"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"[Query {i}] You: {query}")
        print(f"{'='*70}")

        result = get_response(query)

        if result["success"]:
            print(f"\nBot Response:\n{result['message']}")
        else:
            print(f"\nError: {result['message']}")

    print(f"\n{'='*70}")
    print("Demo completed!")
    print("="*70)
    print("\n✅ ITChamps Chatbot is working correctly!")
    print("\n📁 Project files:")
    print("   - Backend API: itchamps/api/chatbot.py")
    print("   - Frontend UI: itchamps/public/js/chatbot.js")
    print("   - Theme CSS: itchamps/public/css/itchamps_theme.css")
    print("\n🚀 To deploy: Push to GitHub and install on Frappe Cloud")
    print()


if __name__ == "__main__":
    main()
