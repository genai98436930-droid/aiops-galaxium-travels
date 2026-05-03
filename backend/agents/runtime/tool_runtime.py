class ToolRuntime:
    def __init__(self, registry):
        self.registry = registry

    def run_plan(self, plan, context=None, trace=None):
        context = context or {}

        result = None

        for tool_name in plan:
            fn = self.registry.execute(tool_name)

            if trace:
                trace.add_step(tool_name, "started", input_data=context)

            result = fn(context)

            if trace:
                trace.add_step(tool_name, "completed", output_data=result)

        return result
