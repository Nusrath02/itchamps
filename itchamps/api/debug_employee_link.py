import frappe

def execute():
    print("--- DEBUGGING USER-EMPLOYEE LINK ---")
    
    # 1. List all Users matching 'Nusrath'
    users = frappe.get_all("User", filters={"first_name": ["like", "%Nusrath%"]}, fields=["name", "email", "full_name", "enabled"])
    print(f"\nFound {len(users)} Users:")
    for u in users:
        print(f" - User: {u.name} (Email: {u.email}, Name: {u.full_name}, Enabled: {u.enabled})")

    # 2. List all Employees matching 'Nusrath'
    employees = frappe.get_all("Employee", filters={"employee_name": ["like", "%Nusrath%"]}, fields=["name", "employee_name", "user_id", "status"])
    print(f"\nFound {len(employees)} Employees:")
    for e in employees:
        print(f" - Employee: {e.name} (Name: {e.employee_name}, Linked User ID: {e.user_id}, Status: {e.status})")

    # 3. Check for specific mismatch
    if users and employees:
        print("\n--- ANALYSIS ---")
        for u in users:
            linked_emp = next((e for e in employees if e.user_id == u.name), None)
            if linked_emp:
                print(f"✅ User '{u.name}' is correctly linked to Employee '{linked_emp.name}'")
            else:
                print(f"❌ User '{u.name}' is NOT linked to any Employee found above.")
