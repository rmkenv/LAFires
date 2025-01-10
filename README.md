# Swimming Pool Detection using Sentinel-2 Imagery

Automated swimming pool detection and analysis using Sentinel-2 satellite imagery and openEO. Features NDWI-based water detection, geolocation, and volume estimation for water management applications.

## Project Overview

This project uses Sentinel-2 satellite imagery and the openEO platform to detect swimming pools in Los Angeles County. It calculates pool locations and estimates water volumes using spectral indices and geospatial analysis.

## Features

- Automated swimming pool detection using Sentinel-2 satellite imagery
- NDWI (Normalized Difference Water Index) calculation for water feature detection
- Reverse geocoding to obtain pool addresses
- Water volume estimation for detected pools
- Visualization of results using matplotlib
- Export of results to CSV format

## Prerequisites

- Python 3.7+
- Access to Copernicus Data Space Ecosystem (CDSE)
- CDSE Client ID and Secret

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rmkenv/LAFires.git
   cd LAFires
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your CDSE credentials:
   ```python
   CLIENT_ID = "YOUR_CLIENT_ID"  # Replace with your CDSE client ID
   CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # Replace with your CDSE client secret
   ```

4. The default Area of Interest (AOI) is set to Los Angeles County:
   ```python
   aoi = {
       "xmin": -118.9448,
       "ymin": 33.7037,
       "xmax": -118.1213,
       "ymax": 34.3373,
       "spatialReference": {"wkid": 4326}
   }
   ```

## Usage

Run the main script:

```bash
python pool_detection.py
```

The script will:

1. Connect to the openEO backend
2. Load Sentinel-2 data
3. Compute spectral indices
4. Process imagery to detect pools
5. Generate pool locations and volume estimates
6. Save results and create visualizations

## Output Files

The script generates two main output files:

1. `pool_mask.tif` - GeoTIFF containing the binary pool detection mask
2. `detected_pools.csv` - CSV file containing:
   - Latitude
   - Longitude
   - Address
   - Estimated Volume (Gallons)

## Functions

- `connect_openeo()` - Establishes connection to openEO backend
- `load_sentinel2_data()` - Loads Sentinel-2 imagery
- `compute_spectral_indices()` - Calculates NDWI
- `process_imagery()` - Processes imagery to detect pools
- `geolocate_pools()` - Generates location data for detected pools
- `visualize_results()` - Creates visualization of detected pools

## Dependencies

- `openeo` - Interface to Copernicus Data Space Ecosystem
- `pandas` - Data manipulation and analysis
- `shapely` - Geometric operations
- `numpy` - Numerical computing
- `scikit-learn` - Machine learning utilities
- `geopy` - Geocoding operations
- `tqdm` - Progress bar
- `rasterio` - Raster data handling
- `matplotlib` - Data visualization

## Limitations

- Detection accuracy depends on Sentinel-2 image quality and cloud cover
- Pool volume estimates are approximations based on pixel size
- Reverse geocoding may not always return accurate addresses
- Processing large areas may require significant computational resources

## Contributing

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## License

This project is licensed under the GPL-3.0 license.

## Acknowledgments

- European Space Agency (ESA) for Sentinel-2 data
- openEO platform for cloud processing capabilities
- Copernicus Data Space Ecosystem for data access

## Contact

- **Ryan Kmetz** - [@yourgithub](https://github.com/rmkenv)
- **Project Link:** [https://github.com/yourusername/pool-detection](https://github.com/yourusername/pool-detection)
