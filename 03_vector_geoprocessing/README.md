# Vector Geoprocessing

Performs buffer, clip, and spatial analysis on US Census TIGER/Line shapefiles to identify census tracts within 10 km of RIT's campus.

## Data Source

- **TIGER/Line Shapefiles**: [Census Bureau](https://www.census.gov/cgi-bin/geo/shapefiles/) — 2023 Census Tracts, New York State
- **ACS Population Data** (optional): [data.census.gov](https://data.census.gov/) — Table B01003

## Workflow

1. Load NY census tract polygons
2. Reproject from NAD83 (EPSG:4269) to UTM 18N (EPSG:32618)
3. Create point feature for RIT campus (43.0846°N, 77.6744°W)
4. Buffer the point by 10 km
5. Clip census tracts to the buffer zone
6. Compute area of each clipped tract in km²

## Operations Demonstrated

- Coordinate reference system transformation (`native:reprojectlayer`)
- Memory layer creation with attributes
- Fixed-distance buffering (`native:buffer`)
- Polygon clipping (`native:clip`)
- Field calculator for derived attributes (`native:fieldcalculator`)

## Screenshots

*(Add screenshots after running the script in QGIS)*
