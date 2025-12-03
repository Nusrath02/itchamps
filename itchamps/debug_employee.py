"""
Employee Chatbot Debug Script
Run this in Frappe console to check employee configuration
"""

import frappe

def debug_employee_config():
    """Debug script to check employee configuration for chatbot"""

    print("\n" + "="*60)
    print("EMPLOYEE CHATBOT CONFIGURATION DEBUG")
    print("="*60)

    # Get current user
    user = frappe.session.user
    print(f"\n1. Current Logged-in User: {user}")

    # Check Employee record by different methods
    print("\n2. Checking Employee Records:")
    print("-" * 60)

    # Method 1: user_id
    emp_by_user_id = frappe.db.get_value("Employee", {"user_id": user}, ["name", "employee_name", "user_id"], as_dict=True)
    print(f"   ✓ By user_id field: {emp_by_user_id if emp_by_user_id else '❌ Not found'}")

    # Method 2: prefered_email
    emp_by_pref_email = frappe.db.get_value("Employee", {"prefered_email": user}, ["name", "employee_name", "prefered_email"], as_dict=True)
    print(f"   ✓ By prefered_email: {emp_by_pref_email if emp_by_pref_email else '❌ Not found'}")

    # Method 3: company_email
    emp_by_company = frappe.db.get_value("Employee", {"company_email": user}, ["name", "employee_name", "company_email"], as_dict=True)
    print(f"   ✓ By company_email: {emp_by_company if emp_by_company else '❌ Not found'}")

    # Method 4: personal_email
    emp_by_personal = frappe.db.get_value("Employee", {"personal_email": user}, ["name", "employee_name", "personal_email"], as_dict=True)
    print(f"   ✓ By personal_email: {emp_by_personal if emp_by_personal else '❌ Not found'}")

    # Find the employee
    employee = emp_by_user_id or emp_by_pref_email or emp_by_company or emp_by_personal

    if not employee:
        print("\n⚠️  WARNING: No employee record found for current user!")
        print("\nPossible Solutions:")
        print("1. Create an Employee record")
        print("2. Link the Employee record to your user by setting one of these fields:")
        print("   - user_id")
        print("   - prefered_email")
        print("   - company_email")
        print("   - personal_email")
        print("\n3. Example: Go to Employee List → Open your employee record → Set 'User ID' field")
        return None

    employee_id = employee.get("name")
    print(f"\n✅ Employee Found: {employee.get('employee_name')} (ID: {employee_id})")

    # Check Leave Allocations
    print("\n3. Checking Leave Allocations:")
    print("-" * 60)
    leave_allocations = frappe.get_all(
        "Leave Allocation",
        filters={"employee": employee_id},
        fields=["name", "leave_type", "total_leaves_allocated", "leave_balance", "docstatus"],
        limit=10
    )

    if leave_allocations:
        for alloc in leave_allocations:
            status = "Approved" if alloc.docstatus == 1 else "Draft"
            print(f"   - {alloc.leave_type}: {alloc.total_leaves_allocated} total, {alloc.leave_balance} remaining [{status}]")
    else:
        print("   ❌ No leave allocations found")

    # Check Leave Applications
    print("\n4. Checking Leave Applications:")
    print("-" * 60)
    leave_apps = frappe.get_all(
        "Leave Application",
        filters={"employee": employee_id},
        fields=["name", "leave_type", "from_date", "to_date", "status", "total_leave_days"],
        order_by="posting_date desc",
        limit=10
    )

    if leave_apps:
        for app in leave_apps:
            print(f"   - {app.name}: {app.leave_type} ({app.from_date} to {app.to_date}) - {app.status}")
    else:
        print("   ❌ No leave applications found")

    # Check Pending Leave Applications
    print("\n5. Checking Pending Leave Applications:")
    print("-" * 60)
    pending_leaves = frappe.get_all(
        "Leave Application",
        filters={
            "employee": employee_id,
            "status": ["in", ["Open", "Pending", "Submitted"]]
        },
        fields=["name", "leave_type", "from_date", "to_date", "status", "total_leave_days"]
    )

    if pending_leaves:
        for leave in pending_leaves:
            print(f"   - {leave.name}: {leave.leave_type} ({leave.total_leave_days} days) - {leave.status}")
    else:
        print("   ✅ No pending leave applications")

    # Check Manager
    print("\n6. Checking Reporting Manager:")
    print("-" * 60)
    manager_id = frappe.db.get_value("Employee", employee_id, "reports_to")
    if manager_id:
        manager = frappe.db.get_value("Employee", manager_id, ["employee_name", "user_id"], as_dict=True)
        print(f"   ✅ Manager: {manager.employee_name} ({manager.user_id})")
    else:
        print("   ❌ No reporting manager set")

    print("\n" + "="*60)
    print("DEBUG COMPLETE")
    print("="*60 + "\n")

    return employee


# Run the debug
if __name__ == "__main__":
    debug_employee_config()


def fix_employee_link(employee_name):
    """
    Helper function to link an employee record to current user
    Usage in console: fix_employee_link("EMP-00001")
    """
    user = frappe.session.user

    try:
        # Update the employee record
        frappe.db.set_value("Employee", employee_name, "user_id", user)
        frappe.db.commit()
        print(f"✅ Successfully linked Employee {employee_name} to user {user}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_chatbot_response(message):
    """
    Test chatbot response directly
    Usage: test_chatbot_response("show my leaves")
    """
    from itchamps.api.chatbot import get_response

    print(f"\n📝 Testing message: '{message}'")
    print("-" * 60)

    response = get_response(message)
    print(response.get("message", "No response"))
    print("-" * 60)

    return response
