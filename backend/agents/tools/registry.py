class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn

    def execute(self, name):
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not registered")
        return self.tools[name]