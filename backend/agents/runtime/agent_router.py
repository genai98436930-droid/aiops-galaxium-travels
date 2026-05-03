from agents.llm.factory import get_llm


class AgentRouter:
    """
    Routes natural language user input to the correct backend tool.
    Can use LLM if available, but also contains deterministic fallback rules.
    """

    def __init__(self, llm_client=None, tool_registry=None):
        self.llm = llm_client or get_llm()
        self.tool_registry = tool_registry

    def route(self, user_input: str, context: dict = None) -> str:
        text = user_input.lower().strip()

        # ===============================
        # HARD RULE ROUTING FIRST
        # ===============================

        # --- flight listing / searching ---
        if any(k in text for k in [
            "show flights", "list flights", "available flights", "find flights", "search flights"
        ]):
            return "get_flights"

        # --- booking creation ---
        if any(k in text for k in [
            "book flight", "create booking", "reserve seat", "make booking"
        ]):
            return "create_booking"

        # --- show bookings ---
        if any(k in text for k in [
            "show bookings", "my bookings", "list bookings", "get bookings", "booking history"
        ]):
            return "get_bookings"

        # --- cancel booking ---
        if any(k in text for k in [
            "cancel booking", "remove booking", "void booking"
        ]):
            return "cancel_booking"

        # --- register user ---
        if any(k in text for k in [
            "register user", "create user", "new user signup"
        ]):
            return "register_user"

        # --- find user ---
        if any(k in text for k in [
            "find user", "get user", "lookup user", "search user"
        ]):
            return "get_user"

        # ===============================
        # OPTIONAL LLM FALLBACK
        # ===============================
        try:
            if self.llm:
                tool = self.llm.decide(user_input)
                if tool:
                    return tool
        except Exception as e:
            print(f"[AgentRouter] LLM fallback failed: {e}")

        # ===============================
        # DEFAULT SAFE FALLBACK
        # ===============================
        return "get_flights"