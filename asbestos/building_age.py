import streamlit as st
import openeo
import tempfile
import os
import rasterio
from rasterio.plot import show

# Streamlit app title
st.title("Sentinel-2 Imagery Viewer")

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

# Client credentials (replace with your actual credentials)
CLIENT_ID = "YOUR_CLIENT_ID"  # Replace with your actual client ID
CLIENT_SECRET = "YOUR_CLIENT_SECRET"  # Replace with your actual client secret

def connect_openeo():
    """Connects to the openEO backend using OAuth 2.0."""
    connection = openeo.connect(OPENEO_BACKEND).authenticate_oidc()
    return connection

def load_sentinel2_data(connection, aoi, start_date, end_date):
    """Loads Sentinel-2 data using openEO."""
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
        bands=["B04", "B03", "B02"]  # RGB bands
    )
    return s2_cube

def download_sentinel2_image(s2_cube):
    """Downloads Sentinel-2 imagery as a GeoTIFF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "sentinel2_image.tif")
        s2_cube.download(output_file)
        return output_file

# Connect to openEO backend
st.write("Connecting to openEO backend...")
try:
    connection = connect_openeo()
    st.success("Connected to openEO backend.")
except Exception as e:
    st.error(f"Failed to connect to openEO backend: {e}")
    st.stop()

# Load Sentinel-2 data
st.write("Loading Sentinel-2 data...")
try:
    start_date = "2024-12-01"
    end_date = "2025-01-09"
    s2_cube = load_sentinel2_data(connection, aoi, start_date, end_date)
    st.success("Sentinel-2 data loaded.")
except Exception as e:
    st.error(f"Failed to load Sentinel-2 data: {e}")
    st.stop()

# Download Sentinel-2 imagery
st.write("Downloading Sentinel-2 imagery...")
try:
    sentinel2_file = download_sentinel2_image(s2_cube)
    st.success("Sentinel-2 imagery downloaded.")
except Exception as e:
    st.error(f"Failed to download Sentinel-2 imagery: {e}")
    st.stop()

# Display the Sentinel-2 imagery on the map
st.write("Displaying Sentinel-2 imagery on the map...")

# Convert the GeoTIFF to a Mapbox raster tile layer
map_html = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Sentinel-2 Imagery</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.js"></script>
    <link
      href="https://api.mapbox.com/mapbox-gl-js/v2.15.0/mapbox-gl.css"
      rel="stylesheet"
    />
    <style>
      body {{
        margin: 0;
        padding: 0;
        font-family: Arial, sans-serif;
      }}
      #map {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 100%;
        height: 600px;
      }}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      mapboxgl.accessToken = "YOUR_MAPBOX_ACCESS_TOKEN";  // Replace with your Mapbox token
      var map = new mapboxgl.Map({{
        container: "map",
        style: "mapbox://styles/mapbox/light-v10",  // Light grey base map
        center: [-118.2621, 34.0267],
        zoom: 12,
      }});

      // Add Sentinel-2 imagery as a raster layer
      map.on("load", function () {{
        map.addSource("sentinel2", {{
          type: "raster",
          tiles: ["https://your-tile-server-url/{z}/{x}/{y}.png"],  // Replace with your tile server URL
          tileSize: 256,
        }});
        map.addLayer({{
          id: "sentinel2",
          type: "raster",
          source: "sentinel2",
          paint: {{}},
        }});
      }});
    </script>
  </body>
</html>
"""

# Embed the HTML in Streamlit
st.components.v1.html(map_html, height=600)
