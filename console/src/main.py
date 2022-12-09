from fastapi import FastAPI
from starlette.responses import RedirectResponse

from .routers import instructions

app = FastAPI(title="Console", description="A basic Kafka producer")

app.include_router(instructions.router)


@app.get("/", include_in_schema=False)
def root():
    response = RedirectResponse(url='/docs')
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8081)
