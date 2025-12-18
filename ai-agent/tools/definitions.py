# TODO: Define Agent Tools
# Owner: AI Agent Engineer

def define_tools():
    return [
        {
            "name": "alert_caregiver",
            "description": "Triggers an emergency alert to the caregiver.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string"},
                    "urgency": {"type": "string", "enum": ["low", "high"]}
                },
                "required": ["reason"]
            }
        }
        # TODO: Add 'log_memory' tool
        # TODO: Add 'check_reminder' tool
    ]
