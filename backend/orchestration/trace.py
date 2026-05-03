import time
import uuid

class ExecutionTrace:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())
        self.steps = []
        self.start_time = time.time()

    def add_step(self, tool_name, status, input_data=None, output_data=None):
        self.steps.append({
            "tool": tool_name,
            "status": status,
            "input": input_data,
            "output": output_data,
            "timestamp": time.time()
        })

    def result(self):
        return {
            "trace_id": self.trace_id,
            "execution_time": time.time() - self.start_time,
            "steps": self.steps
        }