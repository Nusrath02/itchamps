"""
Quick script to fix role-based access control in chatbot.py
Run this to automatically apply the security fix.
"""

import re

# Read the file
with open('itchamps/api/chatbot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Remove EMPLOYEE and EMPLOYER from allowed_roles
content = re.sub(
    r'allowed_roles = \[UserRole\.ADMIN, UserRole\.HR_MANAGER, UserRole\.HR_USER, UserRole\.MANAGER, UserRole\.EMPLOYEE, UserRole\.EMPLOYER\]',
    'allowed_roles = [UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.HR_USER, UserRole.MANAGER]',
    content
)

# Fix 2: Remove the implicit employee permission check
content = re.sub(
    r'    # Implicit permission if they are a valid Employee\r?\n    is_valid_employee = employee_doc is not None\r?\n    \r?\n',
    '',
    content
)

# Fix 3: Change the permission check
content = re.sub(
    r'if not \(has_role_permission or is_valid_employee\):',
    'if not has_role_permission:',
    content
)

# Write back
with open('itchamps/api/chatbot.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Role-based access control fix applied successfully!")
print("Changes made:")
print("  1. Removed EMPLOYEE and EMPLOYER from allowed_roles")
print("  2. Removed implicit employee permission check")
print("  3. Updated permission check logic")
