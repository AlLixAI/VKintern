import importlib.util
import os

from fastapi import FastAPI

app = FastAPI()

def include_router_from_file(app, router_file):
    spec = importlib.util.spec_from_file_location("module.name", router_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "router"):
        app.include_router(module.router)

def scan_and_include_routes(app, routes_directory):
    for root, _, files in os.walk(routes_directory):
        for file in files:
            if file.endswith("_controllers.py"):
                router_file = os.path.join(root, file)
                include_router_from_file(app, router_file)

routes_directory = os.path.join(os.path.dirname(__file__), "routes")
scan_and_include_routes(app, routes_directory)


@app.get("/")
async def hello():
    return {"hello": "world"}

import platform
print(platform.python_version())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)