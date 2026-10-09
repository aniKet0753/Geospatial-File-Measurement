from fastapi import APIRouter, File, HTTPException, UploadFile

from app.db import create_file_record, get_file_record, get_measurements
from app.services.measurement import process_geospatial_file

router = APIRouter(prefix="/api", tags=["Geospatial Files"])
MAX_FILE_SIZE = 25 * 1024 * 1024
ALLOWED_EXTENSIONS = {".kml", ".zip"}


@router.post("/files/", status_code=201)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    filename = file.filename
    extension = f'.{filename.rsplit(".", 1)[-1].lower()}' if "." in filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail="Unsupported file format. Upload a .kml or a .zip containing a Shapefile.",
        )

    contents = await file.read(MAX_FILE_SIZE + 1)
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large. Maximum allowed size is 25 MB.")

    try:
        parsed = process_geospatial_file(filename, contents)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to process geospatial file: {exc}") from exc

    file_id = create_file_record(filename, parsed)
    return {
        "id": file_id,
        "filename": filename,
        "feature_count": parsed["feature_count"],
        "crs": parsed["original_crs"],
        "status": "COMPLETED",
    }


@router.get("/files/{file_id}/")
def file_information(file_id: str):
    record = get_file_record(file_id)
    if record is None:
        raise HTTPException(status_code=404, detail="File not found.")
    return record


@router.get("/files/{file_id}/measurements/")
def file_measurements(file_id: str):
    record = get_file_record(file_id)
    if record is None:
        raise HTTPException(status_code=404, detail="File not found.")

    return {
        "file_id": file_id,
        "filename": record["filename"],
        "crs": record["crs"],
        "measurement_crs": record["measurement_crs"],
        "features": get_measurements(file_id),
    }
