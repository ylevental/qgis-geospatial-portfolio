# NDVI from Landsat 9

Calculates Normalized Difference Vegetation Index from Landsat 9 OLI-2 surface reflectance bands, with a classified color ramp for vegetation health assessment.

## Data Source

- **Landsat 9 Collection 2 Level-2**: Download from [USGS EarthExplorer](https://earthexplorer.usgs.gov/)
- Path 16, Row 30 covers the Rochester, NY / Finger Lakes region
- Free USGS account required

## Workflow

1. Load Band 4 (Red, 0.64–0.67 µm) and Band 5 (NIR, 0.85–0.88 µm)
2. Compute NDVI via raster calculator: `(NIR - Red) / (NIR + Red)`
3. Apply classified color ramp from red (bare soil) through green (dense vegetation)

## NDVI Interpretation

| NDVI Range | Class |
|-----------|-------|
| −1.0 to −0.1 | Water |
| −0.1 to 0.1 | Bare soil / rock |
| 0.1 to 0.3 | Sparse vegetation |
| 0.3 to 0.6 | Moderate vegetation |
| 0.6 to 1.0 | Dense vegetation |

## Screenshots

![NDVI Color Ramp](screenshots/ndvi_output.png)
