from agents.tools.registry import ToolRegistry
from agents.tools.register import register_tools
from agents.runtime.tool_runtime import ToolRuntime
from agents.runtime.agent_router import AgentRouter
from orchestration.engine import OrchestrationEngine


def build_engine():
    tool_registry = ToolRegistry()
    register_tools(tool_registry)

    tool_runtime = ToolRuntime(tool_registry)

    router = AgentRouter(
        llm_client=None,
        tool_registry=tool_registry
    )

    return OrchestrationEngine(router, tool_runtime)