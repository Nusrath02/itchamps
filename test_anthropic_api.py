"""
Anthropic API Key Diagnostic Tool
Run this to check your API key status and available models.

Usage:
    python test_anthropic_api.py
"""

import os
import sys

def test_anthropic_api():
    """Test Anthropic API key and list available models"""
    
    print("\n" + "="*70)
    print("ANTHROPIC API KEY DIAGNOSTIC TEST")
    print("="*70 + "\n")
    
    # Step 1: Check if anthropic library is installed
    print("1. Checking anthropic library installation...")
    try:
        import anthropic
        print(f"   ✅ anthropic library installed (version: {anthropic.__version__})")
    except ImportError:
        print("   ❌ ERROR: anthropic library not installed")
        print("   → Run: pip install anthropic")
        return
    
    # Step 2: Get API key from environment or input
    print("\n2. Checking API key...")
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("   ⚠️  No API key found in environment variable")
        api_key = input("   → Please paste your Anthropic API key: ").strip()
    
    if not api_key:
        print("   ❌ ERROR: No API key provided")
        return
    
    # Validate key format
    if not api_key.startswith('sk-ant-'):
        print(f"   ⚠️  WARNING: API key doesn't start with 'sk-ant-'")
        print(f"   → Your key starts with: {api_key[:10]}...")
    else:
        print(f"   ✅ API key format looks correct: {api_key[:15]}...")
    
    # Step 3: Test API connection
    print("\n3. Testing API connection...")
    try:
        client = anthropic.Anthropic(api_key=api_key)
        print("   ✅ Client created successfully")
    except Exception as e:
        print(f"   ❌ ERROR creating client: {str(e)}")
        return
    
    # Step 4: Test each model
    print("\n4. Testing available models...")
    
    models_to_test = [
        ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet (Oct 2024)"),
        ("claude-3-5-sonnet-20240620", "Claude 3.5 Sonnet (June 2024)"),
        ("claude-3-opus-20240229", "Claude 3 Opus"),
        ("claude-3-sonnet-20240229", "Claude 3 Sonnet"),
        ("claude-3-haiku-20240307", "Claude 3 Haiku"),
    ]
    
    working_models = []
    
    for model_id, model_name in models_to_test:
        print(f"\n   Testing: {model_name}")
        print(f"   Model ID: {model_id}")
        
        try:
            response = client.messages.create(
                model=model_id,
                max_tokens=10,
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            print(f"   ✅ SUCCESS! Model is available")
            print(f"   → Response: {response.content[0].text}")
            working_models.append((model_id, model_name))
            
        except anthropic.NotFoundError as e:
            print(f"   ❌ NOT FOUND: Model doesn't exist or not available to your key")
            print(f"   → Error: {str(e)}")
            
        except anthropic.AuthenticationError as e:
            print(f"   ❌ AUTHENTICATION ERROR: Invalid API key")
            print(f"   → Error: {str(e)}")
            return
            
        except anthropic.PermissionDeniedError as e:
            print(f"   ❌ PERMISSION DENIED: Your key doesn't have access to this model")
            print(f"   → Error: {str(e)}")
            
        except anthropic.RateLimitError as e:
            print(f"   ⚠️  RATE LIMIT: Too many requests")
            print(f"   → Error: {str(e)}")
            
        except Exception as e:
            print(f"   ❌ ERROR: {type(e).__name__}: {str(e)}")
    
    # Step 5: Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70 + "\n")
    
    if working_models:
        print(f"✅ Found {len(working_models)} working model(s):\n")
        for model_id, model_name in working_models:
            print(f"   • {model_name}")
            print(f"     Model ID: {model_id}\n")
        
        print("\n📋 RECOMMENDATION:")
        print(f"   Use this model in your llm_service.py:")
        print(f"   model=\"{working_models[0][0]}\"")
    else:
        print("❌ No working models found!")
        print("\n🔍 TROUBLESHOOTING:")
        print("   1. Verify your API key at: https://console.anthropic.com/")
        print("   2. Check if your account has credits/billing enabled")
        print("   3. Verify your API key permissions")
        print("   4. Check if you're in a supported region")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    test_anthropic_api()
