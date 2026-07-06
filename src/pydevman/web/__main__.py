"""pydevman Web 入口 — FastAPI + uvicorn"""

from pydevman.web.app import create_app


def main():
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8080)


if __name__ == "__main__":
    main()
