class OrchestrationEngine:
    """
    Main orchestration layer:
    1. Ask router which tool to use
    2. Build correct payload for that tool
    3. Execute tool from registry/runtime
    """

    def __init__(self, router, tool_runtime):
        self.router = router
        self.runtime = tool_runtime

    def run(self, user_input, context):
        tool_name = self.router.route(user_input, context)

        try:
            tool_payload = self._build_tool_payload(tool_name, context)

            result = self.runtime.run(tool_name, tool_payload)

            return {
                "tool": tool_name,
                "result": result
            }

        except Exception as e:
            return {
                "tool": tool_name,
                "error": str(e)
            }

    def _build_tool_payload(self, tool_name, context):
        """
        Normalize incoming /agent payload into exact tool arguments.
        """

        if tool_name == "get_flights":
            return {}

        if tool_name == "create_booking":
            return {
                "user_id": context["user_id"],
                "name": context["name"],
                "flight_id": context["flight_id"],
                "seat_class": context.get("seat_class", "economy")
            }

        if tool_name == "get_bookings":
            return {
                "user_id": context["user_id"]
            }

        if tool_name == "cancel_booking":
            return {
                "booking_id": context["booking_id"]
            }

        if tool_name == "register_user":
            return {
                "name": context["name"],
                "email": context["email"]
            }

        if tool_name == "get_user":
            return {
                "name": context["name"],
                "email": context["email"]
            }

        # fallback
        return context