#!/usr/bin/env python3
"""
ITChamps Chatbot - Standalone Test Script
This demonstrates the chatbot logic without requiring full Frappe setup
"""

class MockFrappe:
    """Mock Frappe framework for testing"""
    class session:
        user = "test@example.com"

    @staticmethod
    def whitelist():
        """Decorator mock"""
        def decorator(func):
            return func
        return decorator

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

# Import the chatbot functions (modified to work standalone)
def get_response(message):
    """
    AI Chatbot API endpoint
    """
    try:
        if not message:
            return {"success": False, "message": "Please provide a message"}

        msg_lower = message.lower()
        response_text = ""

        # Leave queries
        if any(keyword in msg_lower for keyword in ['leave', 'leaves', 'vacation']):
            if 'pending' in msg_lower or 'status' in msg_lower:
                response_text = handle_pending_leaves()
            elif 'balance' in msg_lower or 'remaining' in msg_lower:
                response_text = handle_leave_balance()
            else:
                response_text = "**Leave Information**\n\nI can help you with:\n- Check pending leaves\n- View leave balance\n- Apply for new leave"

        # Employee queries
        elif any(keyword in msg_lower for keyword in ['employee', 'staff', 'find']):
            response_text = handle_employee_search(message)

        # Manager queries
        elif 'manager' in msg_lower or 'reporting' in msg_lower:
            response_text = handle_manager_info()

        # Greeting
        elif any(keyword in msg_lower for keyword in ['hi', 'hello', 'hey']):
            response_text = "Hello! 👋\n\nI'm your ITChamps AI assistant. How can I help you today?"

        # Help
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


# Interactive test interface
def main():
    """Run interactive chatbot demo"""
    import sys
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print("ITChamps AI Chatbot - Standalone Demo")
    print("=" * 60)
    print("\nThis is a demonstration of the chatbot logic.")
    print("Type 'quit' or 'exit' to stop.\n")

    # Test queries
    test_queries = [
        "Hello",
        "help",
        "show me employees",
        "who is my manager",
        "pending leaves",
        "leave balance"
    ]

    print("Sample queries you can try:")
    for i, query in enumerate(test_queries, 1):
        print(f"   {i}. {query}")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nGoodbye! Thanks for testing the ITChamps chatbot.\n")
                break

            # Get response
            result = get_response(user_input)

            if result["success"]:
                print(f"\nBot:\n{result['message']}\n")
            else:
                print(f"\nError: {result['message']}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!\n")
            break
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}\n")


if __name__ == "__main__":
    main()
