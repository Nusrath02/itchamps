"""
Quick diagnostic test for chatbot backend issues.
Run this from bench console to see the actual error.

Usage:
    bench --site your-site-name console
    >>> from itchamps.test_chatbot_backend import test_chatbot
    >>> test_chatbot("employee")
"""

import frappe

def test_chatbot(message="employee"):
    """Test the chatbot backend and show detailed errors"""
    print("\n" + "="*60)
    print("CHATBOT BACKEND DIAGNOSTIC TEST")
    print("="*60 + "\n")
    
    # Test 1: Check if user is logged in
    print("1. Checking user session...")
    user = frappe.session.user
    if user == 'Guest':
        print("   ❌ ERROR: You are logged in as Guest")
        print("   → Please log in to a real user account")
        return
    print(f"   ✅ Logged in as: {user}")
    
    # Test 2: Check employee linkage
    print("\n2. Checking employee linkage...")
    try:
        from itchamps.api.auth_service import AuthService
        context = AuthService.get_user_context()
        
        if not context:
            print("   ❌ ERROR: Could not get user context")
            return
            
        if context.get('employee'):
            emp = context['employee']
            print(f"   ✅ Employee found: {emp.get('name')} - {emp.get('id')}")
        else:
            print("   ⚠️  WARNING: No employee record linked to this user")
            print("   → You can still test, but employee-specific queries will fail")
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        print(f"   → {frappe.get_traceback()}")
        return
    
    # Test 3: Check dependencies
    print("\n3. Checking dependencies...")
    try:
        import anthropic
        print("   ✅ anthropic library installed")
    except ImportError:
        print("   ❌ ERROR: anthropic library not installed")
        print("   → Run: bench --site your-site pip install anthropic")
    
    try:
        from itchamps.api.nlu import IntentParser
        print("   ✅ NLU module loaded")
    except Exception as e:
        print(f"   ❌ ERROR loading NLU: {str(e)}")
    
    # Test 4: Check API key
    print("\n4. Checking Anthropic API key...")
    api_key = frappe.conf.get("anthropic_api_key")
    if api_key:
        print(f"   ✅ API key found (starts with: {api_key[:10]}...)")
    else:
        print("   ⚠️  WARNING: No API key configured")
        print("   → Chatbot will use rule-based fallback only")
        print("   → To add: bench --site your-site set-config anthropic_api_key 'sk-ant-...'")
    
    # Test 5: Test the actual chatbot endpoint
    print("\n5. Testing chatbot endpoint...")
    print(f"   Message: '{message}'")
    try:
        from itchamps.api.chatbot import get_response
        response = get_response(message)
        print("\n   ✅ SUCCESS! Response:")
        print("   " + "-"*56)
        print(f"   {response.get('message', 'No message')}")
        print("   " + "-"*56)
    except Exception as e:
        print(f"\n   ❌ ERROR: {str(e)}")
        print("\n   Full traceback:")
        print("   " + "-"*56)
        traceback = frappe.get_traceback()
        for line in traceback.split('\n'):
            print(f"   {line}")
        print("   " + "-"*56)
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_chatbot()
