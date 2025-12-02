# -*- coding: utf-8 -*-
# Copyright (c) 2024, ITChamps and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist()
def get_response(message):
    """
    AI Chatbot API endpoint
    """
    try:
        if not message:
            return {"success": False, "message": "Please provide a message"}
        
        msg_lower = message.lower()
        response_text = ""
        
        # Leave queries
        if any(keyword in msg_lower for keyword in ['leave', 'leaves', 'vacation']):
            if 'pending' in msg_lower or 'status' in msg_lower:
                response_text = handle_pending_leaves()
            elif 'balance' in msg_lower or 'remaining' in msg_lower:
                response_text = handle_leave_balance()
            else:
                response_text = "**Leave Information**\n\nI can help you with:\n- Check pending leaves\n- View leave balance\n- Apply for new leave"
        
        # Employee queries
        elif any(keyword in msg_lower for keyword in ['employee', 'staff', 'find']):
            response_text = handle_employee_search(message)
        
        # Manager queries
        elif 'manager' in msg_lower or 'reporting' in msg_lower:
            response_text = handle_manager_info()
        
        # Greeting
        elif any(keyword in msg_lower for keyword in ['hi', 'hello', 'hey']):
            response_text = "Hello! 👋\n\nI'm your ITChamps AI assistant. How can I help you today?"
        
        # Help
        elif 'help' in msg_lower:
            response_text = "**ITChamps AI Assistant**\n\nI can help with:\n- Leave management\n- Employee information\n- Department details\n- HR queries"
        
        else:
            response_text = f"I understand you're asking about: \"{message}\"\n\nTry asking about leaves, employees, or type 'help'."
        
        return {"success": True, "message": response_text}
    
    except Exception as e:
        frappe.log_error(f"Chatbot Error: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


def handle_pending_leaves():
    """Get pending leave applications"""
    try:
        user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": user}, "name")
        
        if not employee:
            return "I couldn't find your employee record."
        
        leaves = frappe.get_all(
            "Leave Application",
            filters={"employee": employee, "status": "Open"},
            fields=["name", "leave_type", "from_date", "to_date", "total_leave_days"],
            limit=5
        )
        
        if not leaves:
            return "**No Pending Leaves** ✅\n\nYou have no pending leave applications."
        
        response = f"**Your Pending Leaves** ({len(leaves)})\n\n"
        for leave in leaves:
            response += f"📅 **{leave.leave_type}**\n   From: {leave.from_date}\n   To: {leave.to_date}\n   Days: {leave.total_leave_days}\n\n"
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"


def handle_leave_balance():
    """Get leave balance"""
    try:
        user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": user}, "name")
        
        if not employee:
            return "I couldn't find your employee record."
        
        allocations = frappe.get_all(
            "Leave Allocation",
            filters={"employee": employee, "docstatus": 1},
            fields=["leave_type", "total_leaves_allocated", "unused_leaves"]
        )
        
        if not allocations:
            return "No leave allocations found."
        
        response = "**Your Leave Balance** 🏖️\n\n"
        for alloc in allocations:
            response += f"**{alloc.leave_type}**\n   Allocated: {alloc.total_leaves_allocated}\n   Remaining: {alloc.unused_leaves}\n\n"
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"


def handle_employee_search(message):
    """Search employees"""
    try:
        employees = frappe.get_all(
            "Employee",
            filters={"status": "Active"},
            fields=["name", "employee_name", "designation", "department"],
            limit=10
        )
        
        if not employees:
            return "No active employees found."
        
        response = f"**Active Employees** ({len(employees)})\n\n"
        for emp in employees:
            response += f"👤 **{emp.employee_name}**\n   {emp.designation or 'N/A'} - {emp.department or 'N/A'}\n\n"
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"


def handle_manager_info():
    """Get manager information"""
    try:
        user = frappe.session.user
        employee = frappe.get_value("Employee", {"user_id": user}, ["name", "reports_to"], as_dict=True)
        
        if not employee or not employee.reports_to:
            return "No reporting manager assigned."
        
        manager = frappe.get_doc("Employee", employee.reports_to)
        
        response = f"**Your Manager** 👔\n\n**Name:** {manager.employee_name}\n**Designation:** {manager.designation or 'N/A'}\n**Department:** {manager.department or 'N/A'}"
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"