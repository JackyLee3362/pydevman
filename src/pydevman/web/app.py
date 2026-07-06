"""pydevman FastAPI 应用 — 统一注册各模块路由"""

from fastapi import FastAPI

from pydevman.log import config_log


def create_app() -> FastAPI:
    config_log("INFO")

    app = FastAPI(
        title="pydevman",
        description="开发工具集 Web API",
        version="0.1.7",
    )

    # ---- 注册各模块路由 ----
    from pydevman.web.json_api import router as json_router

    app.include_router(json_router, prefix="/json", tags=["JSON"])

    return app
