from typing import Any, Dict


class Trace:
    def __init__(self):
        self.steps = []

    def add_step(self, tool, status, input_data=None, output_data=None):
        self.steps.append({
            "tool": tool,
            "status": status,
            "input": input_data,
            "output": output_data,
        })


class OrchestrationEngine:
    def __init__(self, router, tool_runtime):
        self.router = router
        self.tool_runtime = tool_runtime

    def run(self, text: str, payload: Dict[str, Any]):
        tool_name, context = self.router.route(text, payload)

        plan = [tool_name]

        return self.tool_runtime.run_plan(
            plan=plan,
            context=context,
            trace=self._trace()
        )

    def _trace(self):
        return Trace()