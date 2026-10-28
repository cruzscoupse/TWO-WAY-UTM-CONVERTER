# Two-Way UTM Coordinate Converter

A Python command-line program for converting between WGS 84 geographic coordinates (latitude/longitude) and Universal Transverse Mercator (UTM) coordinates.

## Features
- Latitude/longitude to UTM easting and northing
- UTM easting/northing to latitude and longitude
- Conversion between UTM zones and hemispheres
- Input validation and a repeatable menu

## Requirements
- Python 3.9 or newer
- `pyproj`

## Installation and running
```bash
python -m pip install -r requirements.txt
python utm_converter.py
```

## Example
Input:
- Latitude: `36`
- Longitude: `30`
- UTM zone: press Enter for automatic selection

Expected result (WGS 84 / UTM zone 36N):
- Easting: approximately `229578.630 m`
- Northing: approximately `3988111.962 m`

## Important surveying note
The program uses WGS 84 (EPSG:4326) and WGS 84 UTM CRS definitions. Use the datum and coordinate reference system specified by your survey control or coursework. UTM zone selection matters: a point can be projected into a specified zone, but that does not mean the zone is the most appropriate one for the location.

## GitHub deployment
1. Create a GitHub repository, e.g. `two-way-utm-converter`.
2. Upload `utm_converter.py`, `requirements.txt`, `README.md`, and the report.
3. Commit the files and copy the repository URL for submission.
