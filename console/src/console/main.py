from fastapi import FastAPI

from .routers import instructions

app = FastAPI(title="Console",
              description="A basic Kafka producer",
              docs_url="/")

app.include_router(instructions.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=8081)
