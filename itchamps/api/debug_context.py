import frappe
from itchamps.api.auth_service import AuthService

def execute():
    # Simulate the user, assuming 'nusrath.s@gmail.com' based on screenshots
    user_id = "nusrath.s@gmail.com"
    
    print(f"--- Debugging Context for {user_id} ---")
    try:
        context = AuthService.get_user_context(user_id)
        if not context:
            print("Context is None!")
        else:
            print("User:", context['user']['full_name'])
            print("Employee Data:", context['employee'])
            if context['employee']:
                print("Employee ID (Primary Key):", context['employee'].get('id'))
                print("Employee Name:", context['employee'].get('name'))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    frappe.connect()
    execute()
