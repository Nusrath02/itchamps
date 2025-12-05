from itchamps.api.auth_service import AuthService
import frappe
import json

def test_context():
    # Simulate a user login if possible, or just pass a user ID
    user = frappe.get_all("User", filters={"email": ["like", "%@%"]}, limit=1)[0].name
    print(f"Testing context for user: {user}")
    
    context = AuthService.get_user_context(user)
    print(json.dumps(context, indent=2, default=str))

if __name__ == "__main__":
    test_context()
