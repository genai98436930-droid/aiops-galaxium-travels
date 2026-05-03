class AgentRouter:
    """
    MUST return: (tool_name, context_dict)
    """

    def __init__(self, llm_client=None, tool_registry=None):
        self.llm = llm_client
        self.tool_registry = tool_registry

    def route(self, user_input: str, context: dict = None):
        text = (user_input or "").lower().strip()
        context = context or {}

        if any(k in text for k in ["list flights", "show flights", "find flights"]):
            return "list_flights", context

        if "book flight" in text:
            return "book_flight", context

        if any(k in text for k in ["show bookings", "my bookings"]):
            return "get_bookings", context

        if "cancel booking" in text:
            return "cancel_booking", context

        if "register user" in text:
            return "register_user", context

        if "get user" in text:
            return "get_user", context

        return "list_flights", context