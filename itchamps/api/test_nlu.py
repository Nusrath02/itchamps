from itchamps.api.nlu import IntentParser

def test_intents():
    test_phrases = [
        "Show my leave balance",
        "How many leaves do I have?",
        "Who is my manager?",
        "Find employee Nusrath",
        "Search for hr department",
        "Show my profile",
        "I want to apply leave",
        "Show my recent leaves"
    ]

    print(f"{'Phrase':<30} | {'Intent':<15} | {'Score'}")
    print("-" * 60)
    
    for phrase in test_phrases:
        intent, score = IntentParser.detect_intent(phrase)
        print(f"{phrase:<30} | {intent or 'None':<15} | {score}")
        
    print("\nEntity Extraction Test:")
    print(IntentParser.extract_entities("Find employees in Marketing"))
    print(IntentParser.extract_entities("sick leave"))

if __name__ == "__main__":
    test_intents()
