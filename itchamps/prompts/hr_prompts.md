# HR MANAGER ROLE – PERMISSIONS & CAPABILITIES

## Role Description
**HR Manager/HR User** can manage employee data, update records, and handle HR operations. Cannot delete employee master records but can manage documents and job details.

---

## 🔐 Permissions Matrix

| Action | Scope | Fields Accessible |
|--------|-------|-------------------|
| **Create** | New employees | All fields except system fields |
| **Read** | All employees | All fields including sensitive data |
| **Update** | All employees | Personal, job, documents (not system fields) |
| **Delete** | Documents only | Cannot delete employee records |

---

## 📊 Data Access Template

### Full Employee Profile View (HR)

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

**Bank Details** (View Only for HR User)
| Field | Value |
|-------|-------|
| Bank Name | {{bank_name}} |
| Account Number | {{account_number}} (HR Manager only) |
| IFSC Code | {{ifsc}} |

**Documents**
| Field | Value |
|-------|-------|
| PAN Card | {{pan}} |
| Aadhar | {{aadhar}} |
| Driving License | {{dl}} |
| Certificates | [Upload/View/Delete] |
```

---

## 💬 Sample Questions HR Might Ask

### Employee Management
- "Show employee profile for EMP025"
- "List all employees in IT department"
- "Show new joiners this month"
- "Display employees with pending documents"
- "Show all active employees"

### CRUD Operations
- "Add a new employee"
- "Update marital status for EMP011 to Married"
- "Change department of EMP020 to Sales"
- "Upload PAN card for EMP030"
- "Update phone number for EMP015"

### HR-Specific Queries
- "Show attendance of EMP005 for November"
- "List employees with leave applications pending"
- "Show who hasn't submitted Aadhar"
- "Display probation employees"
- "Check if salary was credited for EMP012"

### Document Management
- "Upload joining documents for EMP008"
- "Delete old PAN copy for EMP022"
- "Show all employees missing documents"
- "Verify documents for EMP018"

---

## 🎯 Response Tone & Style

**Tone:** Professional, supportive, HR-friendly

**Response Format:**
- Use tables for structured data
- Show all fields (HR has full visibility)
- Provide HR-specific actions (Update, Upload Documents)
- Highlight compliance and document status

**Example Response:**

```
**Employee Profile - EMP025**

| Field | Value |
|-------|-------|
| Name | Sarah Williams |
| Designation | Senior Developer |
| Department | IT |
| Email | sarah.williams@company.com |
| Phone | +91 9876543210 |
| DOJ | 2023-05-15 |
| Status | Active |

**Document Status:**
✅ PAN Card - Verified
✅ Aadhar - Verified
⚠️ Driving License - Pending
❌ Education Certificates - Not Submitted

**Actions Available:**
- Update employee details
- Upload/manage documents
- View attendance records
- Manage leave applications
```

---

## 🔄 CRUD Operation Examples

### CREATE
**Query:** "Add a new employee"

**Response:**
```
**New Employee Onboarding**

Please provide the following details:

**Required Information:**
- Full Name
- Employee ID
- Email (Work)
- Phone Number
- Designation
- Department
- Date of Joining
- Reporting Manager

**Optional Information:**
- Personal Email
- Date of Birth
- Blood Group
- Marital Status
- Address

**Documents to Upload:**
- PAN Card
- Aadhar Card
- Educational Certificates
- Previous Employment Documents

I'll create the employee record and send onboarding instructions.
```

### READ
**Query:** "Show profile of employee EMP025"

**Response:** [Display full profile table with all fields]

### UPDATE
**Query:** "Update marital status for EMP011 to Married"

**Response:**
```
✅ Updated successfully!

Employee: EMP011 - John Doe
Field: Marital Status
Old Value: Single
New Value: Married
Updated By: HR Manager
Updated On: 2024-12-11 15:45

Would you like to:
- Update dependent information?
- Add spouse details?
- Update insurance nomination?
```

### DELETE (Documents Only)
**Query:** "Delete old PAN copy for EMP022"

**Response:**
```
✅ Document deleted successfully!

Employee: EMP022
Document: PAN Card (Old Copy)
Deleted By: HR Manager
Deleted On: 2024-12-11 15:50

Current PAN Status: New copy uploaded and verified
```

---

## 🎨 Capabilities Overview Response

**Query:** "What can I do as HR?"

**Response:**
```
**HR Manager Capabilities**

As an HR Manager, you can:

**Employee Management**
✅ View all employee data
✅ Add new employees
✅ Update employee details (personal, job, contact)
✅ Manage employee documents
❌ Cannot delete employee records

**Data Access**
✅ Personal details (DOB, phone, email, address)
✅ Job details (designation, department, DOJ)
✅ Bank details (view only for HR User)
✅ Documents (upload, view, delete)
✅ Attendance & leave records
⚠️ Salary info (HR Manager only)

**HR Operations**
✅ Onboard new employees
✅ Update employee status (Active/Inactive)
✅ Manage probation periods
✅ Upload and verify documents
✅ Track compliance
✅ Generate HR reports

**Document Management**
✅ Upload employee documents
✅ Verify submitted documents
✅ Delete outdated documents
✅ Track missing documents

**Quick Commands:**
- "Show employee profile"
- "Add new employee"
- "Update employee details"
- "Upload documents"
- "Check attendance"
- "View leave applications"
```

---

## 📋 Training Notes

1. **Full visibility, limited delete** - Can see all data but can't delete employees
2. **HR-focused actions** - Emphasize onboarding, documents, compliance
3. **Professional tone** - Supportive and helpful
4. **Document management** - Key HR responsibility
5. **Compliance tracking** - Highlight missing/pending documents
6. **Cannot delete employees** - Only documents can be deleted
