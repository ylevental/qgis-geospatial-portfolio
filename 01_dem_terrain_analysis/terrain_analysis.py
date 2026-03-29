"""
DEM Terrain Analysis — PyQGIS Processing Script
Computes slope, aspect, and hillshade from a USGS 3DEP 1/3 arc-second DEM.

Usage:
    1. Download DEM GeoTIFF from https://apps.nationalmap.gov/downloader/
       - Select "Elevation Products (3DEP)" > 1/3 arc-second
       - Choose a tile covering your area of interest
    2. Open QGIS, then open the Python Console (Plugins > Python Console)
    3. Update INPUT_DEM path below
    4. Paste and run this script
"""

import os
from qgis.core import (
    QgsProject, QgsRasterLayer, QgsCoordinateReferenceSystem
)
import processing

# === CONFIGURATION ===
BASE_DIR = os.path.expanduser("~/Desktop/qgis-portfolio/01_dem_terrain_analysis")
INPUT_DEM = os.path.join(BASE_DIR, "USGS_13_n43w078_20230227.tif")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
PROJECT_CRS = "EPSG:32618"  # UTM Zone 18N (Rochester, NY area)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load DEM
dem_layer = QgsRasterLayer(INPUT_DEM, "USGS_3DEP_DEM")
if not dem_layer.isValid():
    raise RuntimeError(f"Failed to load DEM: {INPUT_DEM}")
QgsProject.instance().addMapLayer(dem_layer)

# Reproject to UTM for metric slope/aspect calculations
reprojected = os.path.join(OUTPUT_DIR, "dem_utm.tif")
processing.run("gdal:warpreproject", {
    'INPUT': dem_layer,
    'SOURCE_CRS': dem_layer.crs(),
    'TARGET_CRS': QgsCoordinateReferenceSystem(PROJECT_CRS),
    'RESAMPLING': 1,  # Bilinear
    'OUTPUT': reprojected
})
dem_utm = QgsRasterLayer(reprojected, "DEM_UTM")
QgsProject.instance().addMapLayer(dem_utm)

# --- Slope (degrees) ---
slope_out = os.path.join(OUTPUT_DIR, "slope_degrees.tif")
processing.run("gdal:slope", {
    'INPUT': dem_utm,
    'BAND': 1,
    'SCALE': 1.0,
    'AS_PERCENT': False,
    'OUTPUT': slope_out
})
slope_layer = QgsRasterLayer(slope_out, "Slope (degrees)")
QgsProject.instance().addMapLayer(slope_layer)

# --- Aspect ---
aspect_out = os.path.join(OUTPUT_DIR, "aspect.tif")
processing.run("gdal:aspect", {
    'INPUT': dem_utm,
    'BAND': 1,
    'OUTPUT': aspect_out
})
aspect_layer = QgsRasterLayer(aspect_out, "Aspect")
QgsProject.instance().addMapLayer(aspect_layer)

# --- Hillshade ---
hillshade_out = os.path.join(OUTPUT_DIR, "hillshade.tif")
processing.run("gdal:hillshade", {
    'INPUT': dem_utm,
    'BAND': 1,
    'Z_FACTOR': 2.0,       # Vertical exaggeration
    'AZIMUTH': 315.0,
    'ALTITUDE': 45.0,
    'OUTPUT': hillshade_out
})
hillshade_layer = QgsRasterLayer(hillshade_out, "Hillshade")
QgsProject.instance().addMapLayer(hillshade_layer)

print("=== Terrain analysis complete ===")
print(f"Outputs in: {OUTPUT_DIR}")
print("Layers added: DEM_UTM, Slope, Aspect, Hillshade")
print(">> Take screenshots of each layer for the portfolio.")
