# Geospatial File Measurement API

A production-oriented FastAPI backend for uploading, processing, and measuring geospatial files.

The API accepts:

- KML files (`.kml`)
- Shapefile ZIP archives (`.zip` containing a `.shp` file and its required companion files)

It extracts geospatial features, preserves geometry and properties, handles coordinate reference systems (CRS), and calculates measurements for supported geometries.

---

## Features

- KML file processing
- Shapefile ZIP processing
- Polygon area calculation
- Polygon perimeter calculation
- LineString length calculation
- Point geometry handling
- Feature geometry and properties extraction
- CRS detection and handling
- Geographic CRS transformation before measurement
- File validation
- ZIP path-traversal protection
- Graceful handling of unsupported geometries
- SQLite persistence
- RESTful API
- Automated tests
- Docker support
- Interactive Swagger API documentation

---

## Tech Stack

- **Python 3.12+**
- **FastAPI**
- **GeoPandas**
- **Shapely**
- **PyProj**
- **SQLite**
- **Pytest**
- **Uvicorn**
- **Docker**

---

## Project Structure

```text
Geospatial File Measurement/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   └── services/
│       ├── __init__.py
│       └── measurement.py
│
├── sample_data/
│   └── sample.kml
│
├── tests/
│   ├── test_health.py
│   ├── test_invalid_file.py
│   ├── test_kml.py
│   ├── test_measurement.py
│   └── test_shapefile.py
│
├── .gitignore
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
