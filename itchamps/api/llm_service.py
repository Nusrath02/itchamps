import frappe
import anthropic
import json
from itchamps.api.auth_service import AuthService
from itchamps.api.constants import UserRole

class LLMService:
    """
    Service to handle interactions with Anthropic's Claude API.
    Manages the conversation loop and executes tools (function calling).
    """
    
    MODEL_NAME = "claude-3-5-sonnet-20240620"
    
    @staticmethod
    def get_api_key():
        """Retrieve API key from site config or settings"""
        return frappe.conf.get("anthropic_api_key") or frappe.db.get_value("Chatbot Settings", None, "api_key")

    @classmethod
    def get_tools(cls):
        """Define the tools available to Claude"""
        return [
            {
                "name": "get_leave_balance",
                "description": "Get the current leave balance for the user. Use this when user asks about remaining leaves or leave quota.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                         "employee_id": {"type": "string", "description": "The Employee ID (e.g., HR-EMP-001)"}
                    },
                    "required": ["employee_id"]
                }
            },
            {
                "name": "get_employee_info",
                "description": "Get details about the current user's employee profile (designation, department, manager).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                         "employee_id": {"type": "string", "description": "The Employee ID"}
                    },
                    "required": ["employee_id"]
                }
            },
            {
                "name": "search_other_employees",
                "description": "Search for other employees in the organization. Restricted to HR/Managers.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "keywords": {"type": "string", "description": "Search terms like name or department"}
                    },
                    "required": ["keywords"]
                }
            }
        ]

    @classmethod
    def process_message(cls, user_message, context):
        """
        Main entry point.
        1. Sends message to Claude with Tools.
        2. if Claude calls tool -> execute -> send result back.
        3. Return final text.
        """
        api_key = cls.get_api_key()
        if not api_key:
            return "⚠️ **Configuration Error**: Anthropic API Key is missing. Please ask Admin to set it in site config."

        client = anthropic.Anthropic(api_key=api_key)
        
        # Prepare system prompt with context
        system_prompt = f"""You are a helpful HR Assistant for ITChamps.
        Current User: {context['user']['full_name']} ({context['user']['id']})
        Employee ID: {context.get('employee', {}).get('id', 'Unknown')}
        Roles: {', '.join(context['roles']['list'])}
        
        Use the available tools to answer questions accurately. 
        If you don't have enough info, ask the user.
        Do not make up facts.
        """

        messages = [{"role": "user", "content": user_message}]

        try:
            # First Call: Ask Claude
            response = client.messages.create(
                model=cls.MODEL_NAME,
                max_tokens=1024,
                system=system_prompt,
                messages=messages,
                tools=cls.get_tools()
            )

            # Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                # Create a list to hold tool results
                tool_results = []
                
                # Append Claude's "thought" (tool use request) to history
                messages.append(response.content)

                for block in response.content:
                    if block.type == "tool_use":
                        result = cls.execute_tool(block.name, block.input, context)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(result, default=str)
                        })

                # Append results to history
                messages.append({"role": "user", "content": tool_results})

                # Second Call: Get Final Answer
                final_response = client.messages.create(
                    model=cls.MODEL_NAME,
                    max_tokens=1024,
                    system=system_prompt,
                    messages=messages,
                    tools=cls.get_tools()
                )
                return final_response.content[0].text
            
            else:
                # No tool used, just return text
                return response.content[0].text

        except Exception as e:
            frappe.log_error(f"Claude AI Error: {str(e)}")
            return f"⚠️ **AI Error**: {str(e)}"

    @classmethod
    def execute_tool(cls, tool_name, args, context):
        """Map tool names to actual Python functions"""
        try:
            if tool_name == "get_leave_balance":
                return cls._tool_get_leave_balance(args['employee_id'])
            elif tool_name == "get_employee_info":
                return context['employee']  # We already have this in context!
            elif tool_name == "search_other_employees":
                # Permission check logic is repeated here or we can reuse chatbot method?
                # For safety, let's keep it tight.
                if not context['roles']['is_hr'] and not context['roles']['is_manager']:
                    return {"error": "Access Denied: You do not have permission to search employees."}
                return cls._tool_search_employees(args['keywords'])
            return {"error": "Unknown tool"}
        except Exception as e:
             return {"error": f"Tool execution failed: {str(e)}"}

    # --- Tool Implementations ---
    
    @staticmethod
    def _tool_get_leave_balance(employee_id):
        allocations = frappe.get_all("Leave Allocation", 
            filters={"employee": employee_id, "docstatus": 1},
            fields=["leave_type", "total_leaves_allocated", "leave_balance", "to_date"]
        )
        return allocations

    @staticmethod
    def _tool_search_employees(keywords):
         return frappe.get_all("Employee",
            filters={"employee_name": ["like", f"%{keywords}%"]},
            fields=["employee_name", "department", "company_email"],
            limit=5
        )
