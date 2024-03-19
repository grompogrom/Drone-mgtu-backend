from fastapi import FastAPI
from app.routers import controllCenter, maps, settings, stats


def get_app():
    app = FastAPI()
    app.include_router(controllCenter.router)
    app.include_router(maps.router)
    # app.include_router(settings.router)
    app.include_router(stats.router)
    return app


app = get_app()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.head("/")
async def root_head():
    return {"message": "Hello Bigger Applications!"}
