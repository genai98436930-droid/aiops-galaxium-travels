class V1Engine:
    def __init__(self, base_engine):
        self.engine = base_engine

    def run(self, text, payload):
        # deterministic / simple routing
        return {
            "mode": "v1",
            "input": text,
            "result": self.engine.run(text, payload)
        }