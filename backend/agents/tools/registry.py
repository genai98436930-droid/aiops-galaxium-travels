class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn

    def execute(self, name, context):
        if name not in self.tools:
            raise Exception(f"Tool not found: {name}")

        return self.tools[name](context)