"""
Vector Geoprocessing — PyQGIS Processing Script
Buffer, clip, and spatial join on Census TIGER/Line shapefiles.

Identifies census tracts within 10 km of a point of interest (RIT campus)
and joins population data from an ACS table.

Usage:
    1. Download TIGER/Line shapefiles from https://www.census.gov/cgi-bin/geo/shapefiles/
       - Select year 2023, layer type "Census Tracts", state "New York"
       - Download tl_2023_36_tract.zip
    2. Download ACS 5-Year population table (B01003) from https://data.census.gov/
       - Geography: All Census Tracts in New York
       - Export as CSV
    3. Update paths below, paste into QGIS Python Console, run
"""

import os
from qgis.core import (
    QgsProject, QgsVectorLayer, QgsPointXY, QgsGeometry,
    QgsFeature, QgsField, QgsCoordinateReferenceSystem
)
from qgis.PyQt.QtCore import QVariant
import processing

# === CONFIGURATION ===
BASE_DIR = os.path.expanduser("~/Desktop/qgis-portfolio/03_vector_geoprocessing")
TRACTS_SHP = f"/vsizip/{os.path.join(BASE_DIR, 'tl_2023_36_tract.zip')}/tl_2023_36_tract.shp"
POP_CSV = ""  # Optional — set path if you downloaded ACS data
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Point of interest: RIT campus (WGS 84)
POI_LAT = 43.0846
POI_LON = -77.6744
BUFFER_KM = 10
PROJECT_CRS = "EPSG:32618"  # UTM 18N

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load census tracts
tracts = QgsVectorLayer(TRACTS_SHP, "NY_Census_Tracts", "ogr")
if not tracts.isValid():
    raise RuntimeError(f"Failed to load: {TRACTS_SHP}")
QgsProject.instance().addMapLayer(tracts)

# Reproject tracts to UTM for metric buffering
tracts_utm_path = os.path.join(OUTPUT_DIR, "tracts_utm.shp")
processing.run("native:reprojectlayer", {
    'INPUT': tracts,
    'TARGET_CRS': QgsCoordinateReferenceSystem(PROJECT_CRS),
    'OUTPUT': tracts_utm_path
})
tracts_utm = QgsVectorLayer(tracts_utm_path, "Tracts_UTM", "ogr")
QgsProject.instance().addMapLayer(tracts_utm)

# Create a point layer for the POI and reproject
poi_layer = QgsVectorLayer("Point?crs=EPSG:4326", "POI_RIT", "memory")
pr = poi_layer.dataProvider()
pr.addAttributes([QgsField("name", QVariant.String)])
poi_layer.updateFields()
feat = QgsFeature()
feat.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(POI_LON, POI_LAT)))
feat.setAttributes(["RIT Campus"])
pr.addFeature(feat)
poi_layer.updateExtents()
QgsProject.instance().addMapLayer(poi_layer)

# Reproject POI to UTM
poi_utm_path = os.path.join(OUTPUT_DIR, "poi_utm.shp")
processing.run("native:reprojectlayer", {
    'INPUT': poi_layer,
    'TARGET_CRS': QgsCoordinateReferenceSystem(PROJECT_CRS),
    'OUTPUT': poi_utm_path
})
poi_utm = QgsVectorLayer(poi_utm_path, "POI_UTM", "ogr")

# Buffer the POI by 10 km
buffer_path = os.path.join(OUTPUT_DIR, "buffer_10km.shp")
processing.run("native:buffer", {
    'INPUT': poi_utm,
    'DISTANCE': BUFFER_KM * 1000,
    'SEGMENTS': 64,
    'DISSOLVE': True,
    'OUTPUT': buffer_path
})
buffer_layer = QgsVectorLayer(buffer_path, "10km_Buffer", "ogr")
QgsProject.instance().addMapLayer(buffer_layer)

# Clip tracts to buffer
clipped_path = os.path.join(OUTPUT_DIR, "tracts_clipped.shp")
processing.run("native:clip", {
    'INPUT': tracts_utm,
    'OVERLAY': buffer_layer,
    'OUTPUT': clipped_path
})
clipped = QgsVectorLayer(clipped_path, "Tracts_Within_10km", "ogr")
QgsProject.instance().addMapLayer(clipped)

# Compute area of clipped tracts in sq km
area_path = os.path.join(OUTPUT_DIR, "tracts_with_area.shp")
processing.run("native:fieldcalculator", {
    'INPUT': clipped,
    'FIELD_NAME': 'area_sqkm',
    'FIELD_TYPE': 0,  # Float
    'FIELD_LENGTH': 12,
    'FIELD_PRECISION': 4,
    'FORMULA': '$area / 1e6',
    'OUTPUT': area_path
})
area_layer = QgsVectorLayer(area_path, "Tracts_Area", "ogr")
QgsProject.instance().addMapLayer(area_layer)

feature_count = area_layer.featureCount()
print("=== Vector geoprocessing complete ===")
print(f"Census tracts within {BUFFER_KM} km of RIT: {feature_count}")
print(f"Outputs in: {OUTPUT_DIR}")
print("Layers: Tracts_UTM, 10km_Buffer, Tracts_Within_10km, Tracts_Area")
print(">> Style the clipped tracts by area_sqkm for a nice screenshot.")
