# Geospatial File Measurement API

## Overview

A FastAPI backend that accepts KML files and
Shapefile ZIP archives and calculates measurements
for geographic features.

## Features

- KML processing
- Shapefile processing
- Polygon area calculation
- Polygon perimeter calculation
- Line length calculation
- Point coordinates
- CRS handling
- File validation
- Error handling
- REST API
- Automated tests

## Tech Stack

- Python
- FastAPI
- GeoPandas
- Shapely
- PyProj
- Pytest

## Run locally

pip install -r requirements.txt

uvicorn app.main:app --reload

## API

GET /health

POST /measure