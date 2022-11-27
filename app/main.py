from fastapi import FastAPI
from app.models import metadata
from app.database.database import engine
from app.api.router import api_router

app = FastAPI(
    title="Hotel API", openapi_url="/api/openapi.json", docs_url="/api/docs"
)


@app.on_event("startup")
async def startup_event():
    metadata.bind = engine

app.include_router(api_router, prefix="/api")

@app.on_event("shutdown")
def shutdown_event():
    pass