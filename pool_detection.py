import openeo
import pandas as pd
from shapely.geometry import Point
import numpy as np
from sklearn.cluster import KMeans
from geopy.geocoders import Nominatim
from tqdm import tqdm
import rasterio
import os
from datetime import date
import json
import uuid
from xml.etree import ElementTree
from urllib.parse import quote
import scipy
from openeo.extra.spectral_indices import compute_indices
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches
from rasterio.plot import show
from scipy import ndimage
from skimage import measure
import tempfile

# Define Area of Interest (AOI) (Los Angeles City boundary - approximate)
aoi = {
    "xmin": -118.6681,
    "ymin": 33.7037,
    "xmax": -118.1553,
    "ymax": 34.3373,
    "spatialReference": {"wkid": 4326}
}

# openEO backend URL
OPENEO_BACKEND = "https://openeo.dataspace.copernicus.eu"

# Client credentials (replace with your actual credentials - consider using environment variables)
CLIENT_ID = "YOUR_CLIENT_ID"  # Replace with your actual client ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # Replace with your actual client secret

def connect_openeo():
    """Connects to the openEO backend using OAuth 2.0."""
    try:
        connection = openeo.connect(OPENEO_BACKEND).authenticate_oidc()
        print("Successfully connected to openEO backend using OIDC.")
        return connection
    except Exception as e:
        raise Exception(f"Failed to connect to openEO backend: {e}")

def load_sentinel2_data(connection, aoi, start_date, end_date):
    """Loads Sentinel-2 data using openEO."""
    try:
        spatial_extent = {
            "west": aoi["xmin"],
            "south": aoi["ymin"],
            "east": aoi["xmax"],
            "north": aoi["ymax"]
        }
        s2_cube = connection.load_collection(
            "SENTINEL2_L2A",
            spatial_extent=spatial_extent,
            temporal_extent=[start_date, end_date],
            bands=["B02", "B03", "B04", "B08"]
        )
        print("Successfully loaded Sentinel-2 data.")
        return s2_cube
    except Exception as e:
        raise Exception(f"Failed to load Sentinel-2 data: {e}")

def compute_spectral_indices(s2_cube):
    """Computes spectral indices using openeo.extra.spectral_indices."""
    try:
        indices_cube = compute_indices(s2_cube, indices=["NDWI"])
        print("Successfully computed spectral indices.")
        return indices_cube
    except Exception as e:
        raise Exception(f"Failed to compute spectral indices: {e}")

def process_imagery(indices_cube):
    """Processes the imagery to detect pools using NDWI thresholding, morphological operations, and object-based analysis."""
    try:
        # Apply NDWI thresholding
        water_mask_cube = indices_cube.filter_bands("NDWI").apply(lambda x: x > 0.3)

        # Download the water mask as a GeoTIFF to a temporary file
        with tempfile.TemporaryDirectory() as tmpdir:
            water_mask_file = os.path.join(tmpdir, "water_mask.tif")
            water_mask_cube.download(water_mask_file)

            with rasterio.open(water_mask_file) as src:
                water_mask_array = src.read(1).astype(np.uint8)

        # Apply morphological opening to remove small noise and smooth boundaries
        structuring_element = np.ones((3, 3), dtype=np.uint8)  # Adjust size as needed
        opened_mask = ndimage.binary_opening(water_mask_array, structure=structuring_element).astype(np.uint8)

        # Label connected components (potential pools)
        label_image = measure.label(opened_mask, connectivity=2)
        regions = measure.regionprops(label_image)

        # Filter regions based on size (adjust min and max pixel counts based on LA City context)
        min_pool_size = 10  # Minimum number of pixels for a pool
        max_pool_size = 300 # Maximum number of pixels for a pool
        pool_mask_array = np.zeros_like(opened_mask, dtype=np.uint8)
        for region in regions:
            if min_pool_size <= region.area <= max_pool_size:
                for coord in region.coords:
                    pool_mask_array[coord[0], coord[1]] = 1

        print("Successfully processed imagery.")
        return pool_mask_array
    except Exception as e:
        raise Exception(f"Failed to process Sentinel-2 data: {e}")

def download_results(pool_mask, file_path="pool_mask.tif"):
    """Downloads the processed data."""
    try:
        with rasterio.open(
            file_path, 'w',
            driver='GTiff',
            height=pool_mask.shape[0],
            width=pool_mask.shape[1],
            count=1,
            dtype=rasterio.uint8,
            crs='EPSG:4326',  # Assuming your AOI is in WGS 84
            transform=rasterio.transform.from_bounds(aoi["xmin"], aoi["ymin"], aoi["xmax"], aoi["ymax"], pool_mask.shape[1], pool_mask.shape[0])
        ) as dst:
            dst.write(pool_mask, 1)

        print(f"Successfully downloaded pool mask to {file_path}")
        return file_path
    except Exception as e:
        raise Exception(f"Failed to download results: {e}")

def geolocate_pools(file_path):
    """Generate pool points with geolocation and water volume estimates."""
    geolocator = Nominatim(user_agent="pool_detector")
    pool_data = []

    try:
        with rasterio.open(file_path) as src:
            pool_mask = src.read(1)
            transform = src.transform
            rows, cols = pool_mask.shape

            for row in tqdm(range(rows)):
                for col in range(cols):
                    if pool_mask[row, col] == 1:
                        x, y = rasterio.transform.xy(transform, row, col, offset='center')
                        point = Point(x, y)

                        # Reverse geocoding for address
                        try:
                            location = geolocator.reverse((y, x), language="en")
                            address = location.address if location else "Unknown"
                        except Exception:
                            address = "Unknown"

                        # Calculate pool volume (assuming pixel represents an average pool)
                        pixel_width = abs(transform[0])
                        pixel_height = abs(transform[4])
                        area_per_pixel = pixel_width * pixel_height  # Each pixel area in square meters
                        depth_meters = 1.5  # Average pool depth
                        gallons_per_pixel = area_per_pixel * depth_meters * 264.172  # Convert to gallons

                        pool_data.append({
                            "Latitude": y,
                            "Longitude": x,
                            "Address": address,
                            "Estimated Volume (Gallons)": gallons_per_pixel
                        })

    except rasterio.errors.RasterioIOError as e:
        print(f"Failed to open GeoTIFF file {file_path}: {e}")
    except Exception as e:
        print(f"Error processing imagery {file_path}: {e}")

    return pd.DataFrame(pool_data)

def visualize_results(file_path):
    """Visualizes the results using matplotlib."""
    try:
        with rasterio.open(file_path) as src:
            pool_mask = src.read(1)
            fig, ax = plt.subplots(figsize=(10, 10))
            show(pool_mask, ax=ax, cmap='viridis')
            ax.set_title("Pool Mask")
            plt.show()
            print("Successfully visualized pool mask.")
    except rasterio.errors.RasterioIOError as e:
        print(f"Failed to open GeoTIFF file {file_path} for visualization: {e}")
    except Exception as e:
        print(f"Error visualizing results: {e}")

def main():
    try:
        print("Connecting to openEO backend...")
        connection = connect_openeo()

        print("Loading Sentinel-2 data for Los Angeles City...")
        start_date = "2024-12-01"
        end_date = "2025-01-09"
        s2_cube = load_sentinel2_data(connection, aoi, start_date, end_date)

        print("Computing spectral indices...")
        indices_cube = compute_spectral_indices(s2_cube)

        print("Processing imagery to detect pools...")
        pool_mask_array = process_imagery(indices_cube)

        print("Downloading results...")
        file_path = download_results(pool_mask_array)

        print("Geolocating detected pools...")
        pool_data = geolocate_pools(file_path)

        print("\nDetected Pools in Los Angeles City:")
        print(pool_data.head())

        # Save the results
        pool_data.to_csv("detected_pools_la_city.csv", index=False)
        print("\nResults saved to 'detected_pools_la_city.csv'.")

        print("Visualizing results...")
        visualize_results(file_path)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
