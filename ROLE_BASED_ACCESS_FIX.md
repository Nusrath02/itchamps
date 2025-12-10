# Role-Based Access Control Fix

## Issue
Employers and Employees can currently search for other employees, which violates security requirements.

## Solution
Modify `chatbot.py` line 176 to remove `UserRole.EMPLOYEE` and `UserRole.EMPLOYER` from allowed roles.

## Manual Fix

Open `d:\Projects\itchamps\itchamps\api\chatbot.py` and find line 176:

**FIND THIS (line 176):**
```python
    allowed_roles = [UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.HR_USER, UserRole.MANAGER, UserRole.EMPLOYEE, UserRole.EMPLOYER]
```

**REPLACE WITH:**
```python
    allowed_roles = [UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.HR_USER, UserRole.MANAGER]
```

Also remove lines 179-180 (the implicit employee permission check):

**REMOVE THESE LINES (179-180):**
```python
    # Implicit permission if they are a valid Employee
    is_valid_employee = employee_doc is not None
```

**CHANGE LINE 182 FROM:**
```python
    if not (has_role_permission or is_valid_employee):
```

**TO:**
```python
    if not has_role_permission:
```

## Result

After this change:
- ✅ Admin, HR Manager, HR User, Manager: Can search employees
- ❌ Employer, Employee: **Cannot** search employees (Access Denied)

## Test
1. Login as Employer (like "Nusrath")
2. Try "search employee"
3. Should see: "⛔ Access Denied"

This matches your requirement from the table where Employers and Employees should only view their own data.
