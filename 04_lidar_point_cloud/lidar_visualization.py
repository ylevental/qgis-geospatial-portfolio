"""
Lidar Point Cloud Visualization — PyQGIS Script
Loads a USGS 3DEP LAZ tile and renders by elevation and classification.

This project connects to my M.S. thesis work at RIT on 3D lidar voxel-based
classification using deep learning.

Usage:
    1. Download a LAZ tile from USGS 3DEP via OpenTopography or the
       USGS Entwine endpoint. For Rochester, NY area:
       https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/
       Or use: https://portal.opentopography.org/
    2. Open QGIS 3.32+ (point cloud support required)
    3. Update LAZ_FILE path below
    4. Paste into QGIS Python Console and run

Note: QGIS point cloud support requires PDAL and the bundled point cloud provider.
"""

import os
from qgis.core import (
    QgsProject, QgsPointCloudLayer, QgsProviderRegistry,
    QgsPointCloudAttributeByRampRenderer,
    QgsPointCloudClassifiedRenderer,
    QgsColorRampShader, QgsStyle
)
from qgis.PyQt.QtGui import QColor

# === CONFIGURATION ===
BASE_DIR = os.path.expanduser("~/Desktop/qgis-portfolio/04_lidar_point_cloud")
LAZ_FILE = os.path.join(BASE_DIR, "points.laz")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load the LAZ point cloud ---
pc_layer = QgsPointCloudLayer(LAZ_FILE, "USGS_3DEP_Lidar", "pdal")
if not pc_layer.isValid():
    raise RuntimeError(
        f"Failed to load point cloud: {LAZ_FILE}\n"
        "Ensure QGIS was built with PDAL support (standard in 3.32+)."
    )
QgsProject.instance().addMapLayer(pc_layer)

# Print basic statistics
stats = pc_layer.statistics()
print(f"Point count: {pc_layer.pointCount():,}")
print(f"CRS: {pc_layer.crs().authid()}")
print(f"Extent: {pc_layer.extent().toString()}")

# --- Render by Elevation (Z) ---
# Create a color ramp renderer for the Z attribute
ramp_renderer = QgsPointCloudAttributeByRampRenderer()
ramp_renderer.setAttribute("Z")
ramp_renderer.setMinimum(100)   # Adjust to your data's Z range
ramp_renderer.setMaximum(250)   # Adjust to your data's Z range

color_ramp = QgsColorRampShader()
color_ramp.setColorRampType(QgsColorRampShader.Interpolated)
color_ramp.setColorRampItemList([
    QgsColorRampShader.ColorRampItem(100, QColor(0, 0, 128),    "Low"),
    QgsColorRampShader.ColorRampItem(150, QColor(0, 255, 0),    "Mid"),
    QgsColorRampShader.ColorRampItem(200, QColor(255, 255, 0),  "High"),
    QgsColorRampShader.ColorRampItem(250, QColor(255, 0, 0),    "Highest"),
])
ramp_renderer.setColorRampShader(color_ramp)

pc_layer.setRenderer(ramp_renderer)
pc_layer.triggerRepaint()
print("Renderer set to: Elevation (Z) color ramp")
print(">> SCREENSHOT 1: Take a screenshot of the elevation-colored point cloud.")

# --- Alternate: Render by ASPRS Classification ---
# Uncomment below to switch to classification rendering.
# Standard ASPRS classes: 2=Ground, 3-5=Vegetation, 6=Building, 9=Water
#
# class_renderer = QgsPointCloudClassifiedRenderer()
# class_renderer.setAttribute("Classification")
# pc_layer.setRenderer(class_renderer)
# pc_layer.triggerRepaint()
# print("Renderer switched to: ASPRS Classification")
# print(">> SCREENSHOT 2: Take a screenshot of the classified point cloud.")

print("\n=== Lidar visualization complete ===")
print("Tip: Use View > 3D Map View for an immersive 3D rendering.")
print("Adjust Z min/max in the script to match your tile's elevation range.")
