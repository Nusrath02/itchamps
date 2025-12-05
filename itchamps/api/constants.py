import frappe
from enum import Enum

class UserRole(Enum):
    """
    Enum for User Roles in ITChamps.
    Maps internal code constants to Frappe Role names.
    """
    ADMIN = "System Manager"
    HR_MANAGER = "HR Manager"
    HR_USER = "HR User"
    EMPLOYEE = "Employee"
    MANAGER = "Manager"

    @classmethod
    def has_role(cls, user, role):    # <--- Fetches list like ['System Manager', 'Employee']
        """
        Check if a user has a specific role.
        
        Args:
            user (str): User email/ID
            role (UserRole): The role to check against
            
        Returns:
            bool: True if user has the role, False otherwise
        """
        if not user or not role:
            return False
            
        roles = frappe.get_roles(user)
        return role.value in roles

    @classmethod
    def get_active_roles(cls, user):
        """Return a list of UserRole enums that the user possesses"""
        user_roles = frappe.get_roles(user)
        return [role for role in cls if role.value in user_roles]

    @classmethod
    def is_privileged_user(cls, user):
        """Check if user has any role that allows viewing sensitive info (HR, Admin, Manager)"""
        privileged_roles = [cls.ADMIN, cls.HR_MANAGER, cls.HR_USER, cls.MANAGER]
        return any(cls.has_role(user, role) for role in privileged_roles)
