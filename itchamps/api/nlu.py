import re

class IntentParser:
    """
    Rule-based Natural Language Understanding (NLU) parser.
    Detects user intent using regex patterns and extracts simple entities.
    """

    # Intent Definitions
    INTENTS = {
        "leave_balance": {
            "patterns": [
                r"leave balance", r"remaining leaves", r"how many leaves", 
                r"leave quota", r"my leaves",r"check leave", r"leave status"
            ],
            "score": 1.0
        },
        "leave_apply": {
            "patterns": [
                r"apply leave", r"request leave", r"take leave", 
                r"book leave", r"want leave", r"need leave"
            ],
            "score": 1.0
        },
        "leave_history": {
            "patterns": [
                r"leave history", r"past leaves", r"recent leaves", 
                r"previous leaves", r"history of leave"
            ],
            "score": 1.0
        },
        "manager_info": {
            "patterns": [
                r"who is my manager", r"reporting manager", r"my boss", 
                r"who do i report to", r"manager details"
            ],
            "score": 1.0
        },
        "employee_search": {
            "patterns": [
                r"find employee", r"search employee", r"who works in", 
                r"employee in", r"search for", r"find"
            ],
            # Context-specific: Only if followed by employee-like terms, handled in code
            "score": 0.8
        },
        "my_info": {
            "patterns": [
                r"my profile", r"my info", r"my details", 
                r"about me", r"employee id"
            ],
            "score": 1.0
        }
    }

    @classmethod
    def detect_intent(cls, message):
        """
        Identify the intent of the message.
        Returns: (intent_name, confidence_score)
        """
        message = message.lower().strip()
        best_intent = None
        best_score = 0.0

        # Check explicit patterns
        for intent, data in cls.INTENTS.items():
            for pattern in data["patterns"]:
                if re.search(pattern, message):
                    # If match found, return immediately for now (simple first-match priority)
                    # We could implement scoring if patterns overlap
                    return intent, 1.0

        # Fallback/Context Heuristics
        # If "leave" is mentioned but no specific action, default to 'leave_balance'
        if "leave" in message:
             if any(w in message for w in ["apply", "take", "request", "want"]):
                 return "leave_apply", 0.7
             else:
                 return "leave_balance", 0.6
        
        # If "manager" mentioned
        if "manager" in message:
            return "manager_info", 0.8

        return None, 0.0

    @classmethod
    def extract_entities(cls, message):
        """
        Extract basic entities like dates, leave types, etc.
        """
        message = message.lower()
        entities = {}

        # 1. Leave Type
        leave_types = {
            "casual": "Casual Leave",
            "sick": "Sick Leave",
            "privilege": "Privilege Leave",
            "earned": "Privilege Leave"
        }
        for key, value in leave_types.items():
            if key in message:
                entities["leave_type"] = value
                break

        # 2. Dept (Basic)
        departments = ["marketing", "sales", "hr", "it", "finance", "operations", "production"]
        for dept in departments:
            if dept in message:
                entities["department"] = dept.capitalize()

        return entities
