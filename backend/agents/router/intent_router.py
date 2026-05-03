class IntentRouter:
    """
    Converts natural language → intent
    (Start simple, upgrade to LLM later)
    """

    def route(self, user_input: str, context: dict = None):

        text = user_input.lower()

        if "book" in text and "flight" in text:
            return "book_flight"

        if "cancel" in text:
            return "cancel_booking"

        if "user" in text:
            return "user_lookup"

        if "flight" in text:
            return "get_flights"

        return "get_flights"