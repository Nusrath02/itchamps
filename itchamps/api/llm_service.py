import frappe
import json
from anthropic import Anthropic
from itchamps.api.constants import UserRole

class LLMService:
    @staticmethod
    def get_client():
        api_key = frappe.conf.get("anthropic_api_key") or frappe.db.get_value("Site Config", None, "anthropic_api_key")
        
        # Debug Log
        if not api_key:
            frappe.log_error("LLMService: API Key NOT FOUND in conf or db", "LLM Debug")
        else:
            frappe.log_error(f"LLMService: API Key FOUND (starts with {api_key[:5]}...)", "LLM Debug")

        if not api_key:
            frappe.throw("Anthropic API Key is missing. Please add 'anthropic_api_key' to site config.")
        return Anthropic(api_key=api_key)

    @staticmethod
    def get_tools():
        return [
            {
                "name": "get_leave_balance",
                "description": "Get leave balance for the current employee",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "The Employee ID (e.g., HR-EMP-00001)"}
                    },
                    "required": ["employee_id"]
                }
            },
            {
                "name": "get_employee_info",
                "description": "Get profile information for a specific employee",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "employee_id": {"type": "string", "description": "The Employee ID to fetch info for"}
                    },
                    "required": ["employee_id"]
                }
            },
            {
                "name": "search_other_employees",
                "description": "Search for other employees in the organization. Restricted to HR and Managers.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "string", "description": "Search keywords like name, department, or designation"}
                    },
                    "required": ["keywords"]
                }
            }
        ]

    @staticmethod
    def execute_tool(tool_name, tool_args, context):
        # Safely get employee and user info from context
        employee = context.get('employee') if context else None
        employee_id = employee.get('id') if employee else None
        user_id = context.get('user', {}).get('id') if context else None
        
        if tool_name == "get_leave_balance":
            # Use the verified employee_id from context/args
            target_emp = tool_args.get('employee_id', employee_id)
            if not target_emp: return "No employee record linked."
            
            leaves = frappe.get_all("Leave Allocation", 
                filters={"employee": target_emp, "docstatus": 1},
                fields=["leave_type", "leave_balance", "total_leaves_allocated"]
            )
            return json.dumps(leaves, default=str)

        elif tool_name == "get_employee_info":
            target_emp = tool_args.get('employee_id', employee_id)
            if not target_emp: return "No employee record found."
            
            doc = frappe.get_doc("Employee", target_emp)
            return json.dumps({
                "name": doc.employee_name,
                "department": doc.department,
                "designation": doc.designation,
                "status": doc.status,
                "email": doc.company_email
            }, default=str)

        elif tool_name == "search_other_employees":
            # Security Check
            allowed = [UserRole.ADMIN, UserRole.HR_MANAGER, UserRole.HR_USER, UserRole.MANAGER, UserRole.EMPLOYEE, UserRole.EMPLOYER]
            if not any(UserRole.has_role(user_id, role) for role in allowed):
                return "Access Denied: You do not have permission to search for other employees."

            query = tool_args.get('keywords', '')
            employees = frappe.get_all("Employee",
                filters={
                    "status": "Active",
                    "employee_name": ["like", f"%{query}%"]
                },
                fields=["employee_name", "department", "designation", "company_email"],
                limit=5
            )
            return json.dumps(employees, default=str)

        return "Tool not found"

    @staticmethod
    def process_message(user_message, context):
        """
        Main loop: User -> Claude -> [Tool Call] -> Tool Result -> Claude -> Response
        """
        try:
            client = LLMService.get_client()
            tools = LLMService.get_tools()
            
            # System Prompt
            user_name = context.get('user', {}).get('full_name', 'User') if context else 'User'
            user_id = context.get('user', {}).get('id', 'unknown') if context else 'unknown'
            employee = context.get('employee') if context else None
            employee_id = employee.get('id') if employee else 'Not Linked'
            
            system_prompt = f"""You are a helpful HR Assistant for ITChamps.
            Current User: {user_name} ({user_id})
            Linked Employee ID: {employee_id}
            
            Use the available tools to answer queries about leaves, profiles, and employees.
            If you cannot answer using a tool, politely explain why.
            Do not make up data.
            """

            messages = [{"role": "user", "content": user_message}]

            # 1. First Call to Claude
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                tools=tools
            )

            # 2. Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                tool_use = next(block for block in response.content if block.type == "tool_use")
                tool_name = tool_use.name
                tool_inputs = tool_use.input
                
                # Execute Tool
                tool_result = LLMService.execute_tool(tool_name, tool_inputs, context)
                
                # Append interaction to history
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_use.id,
                            "content": str(tool_result)
                        }
                    ]
                })
                
                # 3. Get Final Response with Data
                final_response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1024,
                    system=system_prompt,
                    messages=messages,
                    tools=tools
                )
                return final_response.content[0].text
            
            else:
                return response.content[0].text

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "LLM Service Error")
            # Return a friendly fallback if API fails (e.g. key missing)
            return f"I'm currently unable to access my AI brain (API Config Missing or Error). ({str(e)})"
