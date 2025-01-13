import streamlit as st
import folium

# Streamlit app title
st.title("LA Fires")

# Create a Folium map
m = folium.Map(location=[34.0267, -118.2621], zoom_start=12)

# Add a base layer (optional)
folium.TileLayer('cartodbpositron').add_to(m)

# Add custom JavaScript to load all PBF tiles
custom_js = """
<script src="https://unpkg.com/leaflet.vectorgrid/dist/Leaflet.VectorGrid.min.js"></script>
<script>
    // Initialize the map
    var map = L.map('map').setView([34.0267, -118.2621], 12);

    // Add vector tile layers for each time period
    var tileset1890 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1890-1899/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1890-1899': {
                    fill: true,
                    fillColor: '#d7d4d4',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1900 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1900-1909/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1900-1909': {
                    fill: true,
                    fillColor: '#22ecf0',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1910 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1910-1919/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1910-1919': {
                    fill: true,
                    fillColor: '#19d1fd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1920 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1920-1929/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1920-1929': {
                    fill: true,
                    fillColor: '#14b1fd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1930 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1930-1939/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1930-1939': {
                    fill: true,
                    fillColor: '#0f91fd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1940 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1940-1949/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1940-1949': {
                    fill: true,
                    fillColor: '#0a71fd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1950 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1950-1959/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1950-1959': {
                    fill: true,
                    fillColor: '#0551fd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1960 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1960-1969/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1960-1969': {
                    fill: true,
                    fillColor: '#0031fd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1970 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1970-1979/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1970-1979': {
                    fill: true,
                    fillColor: '#0011dd',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1980 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1980-1989/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1980-1989': {
                    fill: true,
                    fillColor: '#0000bb',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset1990 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/1990-1999/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '1990-1999': {
                    fill: true,
                    fillColor: '#000099',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tileset2000 = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/2000-2009/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                '2000-2009': {
                    fill: true,
                    fillColor: '#000077',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    var tilesetcities = L.vectorGrid.protobuf(
        'https://builtla.planninglabs.la/cities/{z}/{x}/{y}.pbf',
        {
            vectorTileLayerStyles: {
                'cities': {
                    fill: true,
                    fillColor: '#ff0000',
                    fillOpacity: 0.5,
                    stroke: true,
                    color: '#000',
                    weight: 1
                }
            }
        }
    );

    // Add layer control to toggle between time periods
    var overlayMaps = {
        "1890-1899": tileset1890,
        "1900-1909": tileset1900,
        "1910-1919": tileset1910,
        "1920-1929": tileset1920,
        "1930-1939": tileset1930,
        "1940-1949": tileset1940,
        "1950-1959": tileset1950,
        "1960-1969": tileset1960,
        "1970-1979": tileset1970,
        "1980-1989": tileset1980,
        "1990-1999": tileset1990,
        "2000-2009": tileset2000,
        "Cities": tilesetcities
    };

    L.control.layers(null, overlayMaps).addTo(map);
</script>
"""

# Add the custom JavaScript to the Folium map
folium.Element(custom_js).add_to(m)

# Render the Folium map in Streamlit
st.components.v1.html(m._repr_html_(), height=600)
