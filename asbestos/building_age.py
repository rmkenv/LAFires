import streamlit as st

# Streamlit app title
st.title("Age of Los Angeles")

# Mapbox access token
mapbox_access_token = "pk.eyJ1IjoiY3J1emluNzN2dyIsImEiOiI3RDdhUi1NIn0.jaEqREZw7QQMRafKPNBdmA"

# Sidebar for filtering
st.sidebar.title("Filter Options")
show_pre_1980 = st.sidebar.checkbox("Show buildings built before 1980", value=True)

# HTML code for the Mapbox map
map_html = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Age of Los Angeles</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link
      rel="stylesheet"
      href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"
    />
    <link
      href="https://fonts.googleapis.com/css?family=Lato:400,700,400italic"
      rel="stylesheet"
      type="text/css"
    />
    <script src="https://code.jquery.com/jquery-2.1.1.min.js"></script>
    <script src="https://api.mapbox.com/mapbox-gl-js/v0.32.1/mapbox-gl.js"></script>
    <link
      href="https://api.mapbox.com/mapbox-gl-js/v0.32.1/mapbox-gl.css"
      rel="stylesheet"
    />
    <style>
      body {{
        margin: 0;
        padding: 0;
        font-family: "Lato", sans-serif;
      }}
      #map {{
        position: absolute;
        top: 0;
        bottom: 0;
        width: 100%;
        height: 600px;
      }}
      #builtbox {{
        position: absolute;
        bottom: 10px;
        left: 10px;
        background: rgba(255, 255, 255, 0.8);
        padding: 10px;
        font-size: 14px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
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
    <div id="builtbox">Hover over a building for year built</div>
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
      var tileset1890 = "https://builtla.planninglabs.la/1890-1899/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1900 = "https://builtla.planninglabs.la/1900-1909/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1910 = "https://builtla.planninglabs.la/1910-1919/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1920 = "https://builtla.planninglabs.la/1920-1929/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1930 = "https://builtla.planninglabs.la/1930-1939/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1940 = "https://builtla.planninglabs.la/1940-1949/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1950 = "https://builtla.planninglabs.la/1950-1959/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1960 = "https://builtla.planninglabs.la/1960-1969/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1970 = "https://builtla.planninglabs.la/1970-1979/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1980 = "https://builtla.planninglabs.la/1980-1989/{{z}}/{{x}}/{{y}}.pbf";
      var tileset1990 = "https://builtla.planninglabs.la/1990-1999/{{z}}/{{x}}/{{y}}.pbf";
      var tileset2000 = "https://builtla.planninglabs.la/2000-2009/{{z}}/{{x}}/{{y}}.pbf";

      var mapStyle = {{
        version: 8,
        sources: {{
          tileset1890: {{
            type: "vector",
            tiles: [tileset1890],
          }},
          tileset1900: {{
            type: "vector",
            tiles: [tileset1900],
          }},
          tileset1910: {{
            type: "vector",
            tiles: [tileset1910],
          }},
          tileset1920: {{
            type: "vector",
            tiles: [tileset1920],
          }},
          tileset1930: {{
            type: "vector",
            tiles: [tileset1930],
          }},
          tileset1940: {{
            type: "vector",
            tiles: [tileset1940],
          }},
          tileset1950: {{
            type: "vector",
            tiles: [tileset1950],
          }},
          tileset1960: {{
            type: "vector",
            tiles: [tileset1960],
          }},
          tileset1970: {{
            type: "vector",
            tiles: [tileset1970],
          }},
          tileset1980: {{
            type: "vector",
            tiles: [tileset1980],
          }},
        }},
        layers: [
          {{
            id: "tileset1890",
            source: "tileset1890",
            "source-layer": "1890-1899",
            paint: {{
              "fill-color": "#d7d4d4",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1900",
            source: "tileset1900",
            "source-layer": "1900-1909",
            paint: {{
              "fill-color": "#22ecf0",
            }},
            type: "fill",
          }},
        ],
      }};
    </script>
  </body>
</html>
"""

# Embed the HTML in Streamlit
st.components.v1.html(map_html, height=600)
