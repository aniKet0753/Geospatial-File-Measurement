from fastapi import FastAPI, UploadFile, File
from app.api.routes import router
from app.db import init_db

init_db()


app = FastAPI(
    title="Geospatial File Measurement API",
    description="API for measuring features from KML and Shapefile data.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }