from functools import wraps

def safe_tool(fn):
    """
    Wraps every tool so NOTHING can crash the runtime.
    """

    @wraps(fn)
    def wrapper(context: dict):
        try:
            return fn(context)
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_code": "TOOL_EXECUTION_ERROR",
                "tool": fn.__name__
            }

    return wrapper