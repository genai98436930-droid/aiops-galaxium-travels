import os
from runtime.engine_factory import build_engine
from runtime.engine_v1 import V1Engine
from runtime.engine_v2 import V2Engine


def get_engine():
    base = build_engine()
    mode = os.getenv("SYSTEM_VERSION", "v1")

    if mode == "v2":
        return V2Engine(base)

    return V1Engine(base)