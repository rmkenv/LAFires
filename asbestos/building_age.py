import streamlit as st

# Streamlit app title
st.title("Age of Los Angeles")

# Mapbox access token
mapbox_access_token = "pk.eyJ1IjoiY3J1emluNzN2dyIsImEiOiI3RDdhUi1NIn0.jaEqREZw7QQMRafKPNBdmA"

# HTML code for the Mapbox map
map_html = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Age of Los Angeles</title>
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
      #legend {{
        position: absolute;
        bottom: 10px;
        right: 10px;
        background: rgba(255, 255, 255, 0.8);
        padding: 10px;
        font-size: 14px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
      }}
      .legend-item {{
        display: flex;
        align-items: center;
        margin-bottom: 5px;
      }}
      .legend-color {{
        width: 20px;
        height: 20px;
        margin-right: 10px;
        border-radius: 3px;
      }}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <div id="legend">
      <h4>Legend</h4>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #d7d4d4;"></div>
        <span>1890-1899</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #22ecf0;"></div>
        <span>1900-1909</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #19d1fd;"></div>
        <span>1910-1919</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #14b1fd;"></div>
        <span>1920-1929</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #2c7fdb;"></div>
        <span>1930-1939</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #3d52bf;"></div>
        <span>1940-1949</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #6539b3;"></div>
        <span>1950-1959</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #a032b2;"></div>
        <span>1960-1969</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #d124a9;"></div>
        <span>1970-1979</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #fd4dab;"></div>
        <span>1980-1989</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #fea7d4;"></div>
        <span>1990-1999</span>
      </div>
      <div class="legend-item">
        <div class="legend-color" style="background-color: #ff7911;"></div>
        <span>2000-2009</span>
      </div>
    </div>
    <script>
      mapboxgl.accessToken = "{mapbox_access_token}";
      var map = new mapboxgl.Map({{
        container: "map",
        style: "mapbox://styles/mapbox/streets-v11",
        center: [-118.2621, 34.0267],
        zoom: 12,
      }});

      // Add vector tile layers
      map.on("load", function () {{
        map.addSource("tileset1890", {{
          type: "vector",
          tiles: ["https://builtla.planninglabs.la/1890-1899/{{z}}/{{x}}/{{y}}.pbf"],
        }});
        map.addLayer({{
          id: "tileset1890",
          type: "fill",
          source: "tileset1890",
          "source-layer": "1890-1899",
          paint: {{
            "fill-color": "#d7d4d4",
            "fill-opacity": 0.6,
          }},
        }});

        map.addSource("tileset1900", {{
          type: "vector",
          tiles: ["https://builtla.planninglabs.la/1900-1909/{{z}}/{{x}}/{{y}}.pbf"],
        }});
        map.addLayer({{
          id: "tileset1900",
          type: "fill",
          source: "tileset1900",
          "source-layer": "1900-1909",
          paint: {{
            "fill-color": "#22ecf0",
            "fill-opacity": 0.6,
          }},
        }});

        map.addSource("tileset1910", {{
          type: "vector",
          tiles: ["https://builtla.planninglabs.la/1910-1919/{{z}}/{{x}}/{{y}}.pbf"],
        }});
        map.addLayer({{
          id: "tileset1910",
          type: "fill",
          source: "tileset1910",
          "source-layer": "1910-1919",
          paint: {{
            "fill-color": "#19d1fd",
            "fill-opacity": 0.6,
          }},
        }});
      }});
    </script>
  </body>
</html>
"""

# Embed the HTML in Streamlit
st.components.v1.html(map_html, height=600)
