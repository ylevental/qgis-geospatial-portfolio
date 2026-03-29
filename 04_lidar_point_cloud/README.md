# Lidar Point Cloud Visualization

Loads and renders USGS 3DEP lidar point clouds in QGIS, with elevation-based color ramps and ASPRS classification rendering.

## Connection to Thesis Work

This project connects directly to my [M.S. thesis at RIT](https://repository.rit.edu/theses/11534/) on **3D lidar voxel-based classification using deep learning**, where I developed methods for classifying airborne lidar point clouds into land cover categories using 3D convolutional neural networks. The workflows here demonstrate the upstream visualization and exploration steps that inform feature engineering for point cloud classification.

## Data Source

- **USGS 3DEP Lidar**: Download LAZ tiles from [OpenTopography](https://portal.opentopography.org/) or [USGS rockyweb](https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/)
- Rochester, NY area tiles from the NY statewide lidar collection

## Workflow

1. Load LAZ point cloud via PDAL provider (QGIS 3.32+)
2. Inspect point count, CRS, and spatial extent
3. Apply elevation (Z) color ramp renderer
4. Optionally switch to ASPRS classification renderer
5. Explore in 3D Map View

## ASPRS Classification Codes

| Code | Class |
|------|-------|
| 2 | Ground |
| 3 | Low Vegetation |
| 4 | Medium Vegetation |
| 5 | High Vegetation |
| 6 | Building |
| 9 | Water |

## Screenshots

![Lidar Point Cloud — Elevation Color Ramp](screenshots/lidar_render.png)
