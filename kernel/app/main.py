from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.routers import instructions

app = FastAPI(
    title="Kernel",
    description="Kernel API - A Kafka consumer microservice",
)

app.include_router(instructions.router)


@app.get("/", include_in_schema=False)
def root():
    response = RedirectResponse(url='/docs')
    return response
