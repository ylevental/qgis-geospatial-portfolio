"""
NDVI Calculation from Landsat 8 OLI — PyQGIS Processing Script
Computes Normalized Difference Vegetation Index: (NIR - Red) / (NIR + Red)

Usage:
    1. Download a Landsat 8/9 Collection 2 Level-2 scene from
       https://earthexplorer.usgs.gov/ (free USGS account required)
       - Search for Path 16, Row 30 (Rochester, NY area)
       - Download the Surface Reflectance product
    2. Extract the tar.gz — you need Band 4 (Red) and Band 5 (NIR) GeoTIFFs
    3. Open QGIS Python Console, update paths below, paste and run
"""

import os
from qgis.core import (
    QgsProject, QgsRasterLayer, QgsRasterShader,
    QgsColorRampShader, QgsStyle, QgsSingleBandPseudoColorRenderer
)
import processing
from qgis.PyQt.QtGui import QColor

# === CONFIGURATION ===
BASE_DIR = os.path.expanduser("~/Desktop/qgis-portfolio/02_ndvi_landsat")
BAND4_RED = os.path.join(BASE_DIR, "LC09_L2SP_016030_20260323_20260325_02_T2_SR_B4.TIF")
BAND5_NIR = os.path.join(BASE_DIR, "LC09_L2SP_016030_20260323_20260325_02_T2_SR_B5.TIF")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load bands
red = QgsRasterLayer(BAND4_RED, "Landsat8_B4_Red")
nir = QgsRasterLayer(BAND5_NIR, "Landsat8_B5_NIR")

for lyr in [red, nir]:
    if not lyr.isValid():
        raise RuntimeError(f"Failed to load: {lyr.source()}")
    QgsProject.instance().addMapLayer(lyr)

# Compute NDVI using raster calculator
# Landsat Collection 2 Level-2 surface reflectance has a scale factor of 0.0000275
# and offset of -0.2, but for NDVI the ratio cancels the scaling.
ndvi_out = os.path.join(OUTPUT_DIR, "ndvi.tif")
ndvi_expression = (
    f'("{nir.name()}@1" - "{red.name()}@1") / '
    f'("{nir.name()}@1" + "{red.name()}@1")'
)

processing.run("qgis:rastercalculator", {
    'EXPRESSION': ndvi_expression,
    'LAYERS': [nir],
    'CELLSIZE': 0,        # Use input cell size
    'EXTENT': None,       # Use input extent
    'CRS': nir.crs(),
    'OUTPUT': ndvi_out
})

# Load NDVI result and apply color ramp
ndvi_layer = QgsRasterLayer(ndvi_out, "NDVI")
QgsProject.instance().addMapLayer(ndvi_layer)

# Apply a classified color ramp
shader = QgsRasterShader()
color_ramp = QgsColorRampShader()
color_ramp.setColorRampType(QgsColorRampShader.Interpolated)
color_ramp.setColorRampItemList([
    QgsColorRampShader.ColorRampItem(-1.0, QColor(165, 0, 38),    "Water / No data"),
    QgsColorRampShader.ColorRampItem(-0.1, QColor(215, 48, 39),   "Bare soil"),
    QgsColorRampShader.ColorRampItem(0.0,  QColor(244, 109, 67),  "Bare ground"),
    QgsColorRampShader.ColorRampItem(0.1,  QColor(253, 174, 97),  "Sparse vegetation"),
    QgsColorRampShader.ColorRampItem(0.2,  QColor(254, 224, 139), "Low vegetation"),
    QgsColorRampShader.ColorRampItem(0.4,  QColor(166, 217, 106), "Moderate vegetation"),
    QgsColorRampShader.ColorRampItem(0.6,  QColor(26, 152, 80),   "Dense vegetation"),
    QgsColorRampShader.ColorRampItem(1.0,  QColor(0, 104, 55),    "Very dense vegetation"),
])
shader.setRasterShaderFunction(color_ramp)
renderer = QgsSingleBandPseudoColorRenderer(ndvi_layer.dataProvider(), 1, shader)
ndvi_layer.setRenderer(renderer)
ndvi_layer.triggerRepaint()

print("=== NDVI calculation complete ===")
print(f"Output: {ndvi_out}")
print("Color ramp applied. Take a screenshot of the NDVI layer.")
