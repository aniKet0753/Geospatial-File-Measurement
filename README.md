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
Architecture:

The application is divided into three main layers:
API Layer
app/api/routes.py
Handles:
- File uploads
- File information requests
- Measurement requests
- HTTP validation and error responses
Service Layer
app/services/measurement.py
Responsible for:
- Reading KML files
- Extracting Shapefile ZIP archives
- Loading geospatial data with GeoPandas
- Extracting feature geometry and properties
- CRS handling
- Measurement calculations
Database Layer
app/db.py
Uses SQLite to persist:
- Uploaded file information
- Processing status
- CRS information
- Extracted feature information
- Measurement results
Setup
Prerequisites
Make sure you have:
- Python 3.12+
- pip
- Git
1. Clone the repository
git clone https://github.com/aniKet0753/Geospatial-File-Measurement.git
cd Geospatial-File-Measurement

3. Install dependencies
pip install -r requirements.txt

4. Run the application
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

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

