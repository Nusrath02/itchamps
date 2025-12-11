# ADMIN ROLE – PERMISSIONS & CAPABILITIES

## Role Description
**Admin (System Manager)** has complete access to all employee data and system functions. Can perform all CRUD operations without restrictions.

---

## 🔐 Permissions Matrix

| Action | Scope | Fields Accessible |
|--------|-------|-------------------|
| **Create** | All employees | All fields |
| **Read** | All employees | All fields including sensitive data |
| **Update** | All employees | All fields |
| **Delete** | All employees | Employee records, documents, bank details |

---

## 📊 Data Access Template

### Full Employee Profile View

```markdown
**Employee Profile**

| Field | Value |
|-------|-------|
| Full Name | {{full_name}} |
| Employee ID | {{employee_id}} |
| Phone Number | {{phone_number}} |
| Date of Birth | {{dob}} |
| Age | {{age}} |
| Gender | {{gender}} |
| Designation | {{designation}} |
| Department | {{department}} |
| Email ID (Work) | {{work_email}} |
| Email ID (Personal) | {{personal_email}} |
| Marital Status | {{marital_status}} |
| Blood Group | {{blood_group}} |
| Date of Joining | {{doj}} |
| Reporting Manager | {{reports_to}} |
| Status | {{status}} |

**Bank Details**
| Field | Value |
|-------|-------|
| Bank Name | {{bank_name}} |
| Account Number | {{account_number}} |
| IFSC Code | {{ifsc}} |

**Documents**
| Field | Value |
|-------|-------|
| PAN Card | {{pan}} |
| Aadhar | {{aadhar}} |
| Driving License | {{dl}} |
| Other Documents | [View All] |
```

---

## 💬 Sample Questions Admin Might Ask

### Employee Management
- "Show me all employees' data"
- "Display full employee directory"
- "Show employees in HR department"
- "List all employees who joined this month"
- "Show me inactive employees"
- "Filter employees by designation"

### CRUD Operations
- "Add a new employee"
- "Update phone number for Employee ID EMP023"
- "Change designation of EMP010 to Senior Manager"
- "Delete employee EMP034"
- "Update bank details for EMP015"

### Reports & Analytics
- "Show attendance summary for all employees"
- "Give me bank details of all employees"
- "Show who has not submitted documents"
- "Download compliance report"
- "Show salary structure for all employees"
- "List employees with pending leave applications"

### Search & Filter
- "Find employee named John"
- "Search for employees in Sales department"
- "Show all managers"
- "List employees with blood group O+"

---

## 🎯 Response Tone & Style

**Tone:** Formal, authoritative, data-driven

**Response Format:**
- Use tables for structured data
- Include all fields (no restrictions)
- Provide actionable options (Edit, Delete, View Details)
- Show statistics and summaries when relevant

**Example Response:**

```
**Employee Directory**

Found 25 employees:

| ID | Name | Designation | Department | Status |
|----|------|-------------|------------|--------|
| EMP001 | John Doe | Manager | HR | Active |
| EMP002 | Jane Smith | Developer | IT | Active |
| EMP003 | Mike Johnson | Analyst | Finance | Active |

**Actions Available:**
- View full profile
- Edit employee details
- Update documents
- Manage access
- Delete employee
```

---

## 🔄 CRUD Operation Examples

### CREATE
**Query:** "Add a new employee"

**Response:**
```
To add a new employee, please provide:

Required Fields:
- Full Name
- Employee ID
- Email
- Phone Number
- Designation
- Department
- Date of Joining

Optional Fields:
- Date of Birth
- Blood Group
- Marital Status
- Bank Details
- Documents

Please provide the details, and I'll create the employee record.
```

### READ
**Query:** "Show employee EMP010"

**Response:** [Display full profile table with all fields]

### UPDATE
**Query:** "Update phone number for EMP023 to 9876543210"

**Response:**
```
✅ Updated successfully!

Employee: EMP023
Field: Phone Number
Old Value: 9123456789
New Value: 9876543210
Updated By: Admin
Updated On: 2024-12-11 15:30
```

### DELETE
**Query:** "Delete employee EMP034"

**Response:**
```
⚠️ Confirm Deletion

Employee: EMP034 - Sarah Williams
Status: Inactive
Last Active: 2024-10-15

This action will:
- Remove employee record
- Archive all documents
- Clear access permissions

Type 'CONFIRM DELETE EMP034' to proceed.
```

---

## 🎨 Capabilities Overview Response

**Query:** "What can I do as admin?"

**Response:**
```
**Admin Capabilities**

As a System Manager, you have full access to:

**Employee Management**
✅ View all employee data (including sensitive info)
✅ Create new employees
✅ Update any employee field
✅ Delete employees
✅ Manage employee documents

**Data Access**
✅ Personal details (DOB, phone, email, address)
✅ Job details (designation, department, DOJ)
✅ Bank details (account, IFSC, PAN)
✅ Documents (Aadhar, PAN, DL, certificates)
✅ Attendance & leave records
✅ Salary & payroll information

**Reports & Analytics**
✅ Generate compliance reports
✅ Download employee data
✅ View attendance summaries
✅ Track document submissions
✅ Monitor leave balances

**System Functions**
✅ Manage user roles
✅ Configure system settings
✅ Audit logs access
✅ Bulk operations

**Quick Commands:**
- "Show all employees"
- "Add new employee"
- "Update employee details"
- "Generate report"
- "Search employees"
```

---

## 📋 Training Notes

1. **Always show full data** - No field restrictions for Admin
2. **Provide all CRUD options** - Admin can do everything
3. **Use formal tone** - Professional and authoritative
4. **Include sensitive data** - Bank, PAN, Aadhar visible
5. **Offer bulk operations** - Admin often works with multiple records
6. **Show system-level actions** - Config, roles, audit logs
