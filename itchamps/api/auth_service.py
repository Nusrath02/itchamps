import frappe
from itchamps.api.constants import UserRole

class AuthService:
    """
    Service to handle user context retrieval and validation.
    Acts as a centralized place to gather User + Employee + Roles data.
    """

    @staticmethod
    def get_user_context(user_id=None):
        """
        Get rich user context including Employee details and Roles.
        
        Args:
            user_id (str, optional): User email/ID. Defaults to frappe.session.user.
            
        Returns:
            dict: Structured user data object
        """
        if not user_id:
            user_id = frappe.session.user

        if user_id == 'Guest':
            return None

        # 1. Basic User Data
        user_doc = frappe.db.get_value("User", user_id, 
            ["name", "email", "first_name", "last_name", "full_name", "user_image"], 
            as_dict=True
        )
        
        if not user_doc:
            return None

        # 2. Fetch Employee Record
        # Logic matches the previous chatbot.py logic but centralized here
        employee = AuthService._get_employee_record(user_id)
        
        # 3. Fetch Roles
        roles = UserRole.get_active_roles(user_id)
        role_values = [r.value for r in roles] # List of strings for frontend
        is_privileged = UserRole.is_privileged_user(user_id)

        # 4. Construct Rich Object
        context = {
            "user": {
                "id": user_doc.name,
                "email": user_doc.email,
                "full_name": user_doc.full_name,
                "first_name": user_doc.first_name,
                "image": user_doc.user_image
            },
            "roles": {
                "list": role_values,
                "is_privileged": is_privileged,
                "is_admin": UserRole.ADMIN in roles,
                "is_hr": UserRole.HR_MANAGER in roles or UserRole.HR_USER in roles,
                "is_manager": UserRole.MANAGER in roles,
                "is_employee": UserRole.EMPLOYEE in roles
            },
            "employee": None
        }

        if employee:
            context["employee"] = {
                "id": employee.name,
                "name": employee.employee_name,
                "department": employee.department,
                "designation": employee.designation,
                "company_email": employee.company_email,
                "reports_to": employee.reports_to
            }

        return context

    @staticmethod
    def _get_employee_record(user_id):
        """Try multiple fields to find the linked Employee record"""
        employee = frappe.db.get_value("Employee", {"user_id": user_id}, ["*"], as_dict=True)
        
        if not employee:
            employee = frappe.db.get_value("Employee", {"prefered_email": user_id}, ["*"], as_dict=True)
            
        if not employee:
            employee = frappe.db.get_value("Employee", {"company_email": user_id}, ["*"], as_dict=True)
            
        if not employee:
            employee = frappe.db.get_value("Employee", {"personal_email": user_id}, ["*"], as_dict=True)
            
        return employee
