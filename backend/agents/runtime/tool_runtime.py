class ToolRuntime:
    """
    Safe execution boundary between LLM and backend services
    """

    def __init__(self, registry):
        self.registry = registry

    def run(self, tool_name: str, context: dict):
        return self.registry.execute(tool_name, context)