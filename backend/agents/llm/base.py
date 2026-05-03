class BaseLLMClient:
    def decide(self, user_input: str):
        raise NotImplementedError