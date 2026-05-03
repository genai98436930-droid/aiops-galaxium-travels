class ToolPlanner:
    """
    Converts intent → execution plan (tool chain)
    """

    def __init__(self, tool_registry):
        self.registry = tool_registry

    def create_plan(self, intent: str, context: dict):
        """
        Returns ordered list of tools
        """

        # 🔵 V2 SIMPLE RULE-BASED START (NO LLM YET)
        if intent == "get_flights":
            return ["get_flights"]

        if intent == "book_flight":
            return [
                "get_flights",
                "create_booking"
            ]

        if intent == "cancel_booking":
            return ["cancel_booking"]

        if intent == "user_lookup":
            return ["get_user"]

        # fallback
        return ["get_flights"]