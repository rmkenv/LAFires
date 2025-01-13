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
    </style>
  </head>
  <body>
    <div id="map"></div>
    <div id="builtbox">Hover over a building for year built</div>
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
          tileset1990: {{
            type: "vector",
            tiles: [tileset1990],
          }},
          tileset2000: {{
            type: "vector",
            tiles: [tileset2000],
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
          {{
            id: "tileset1910",
            source: "tileset1910",
            "source-layer": "1910-1919",
            paint: {{
              "fill-color": "#19d1fd",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1920",
            source: "tileset1920",
            "source-layer": "1920-1929",
            paint: {{
              "fill-color": "#14b1fd",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1930",
            source: "tileset1930",
            "source-layer": "1930-1939",
            paint: {{
              "fill-color": "#2c7fdb",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1940",
            source: "tileset1940",
            "source-layer": "1940-1949",
            paint: {{
              "fill-color": "#3d52bf",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1950",
            source: "tileset1950",
            "source-layer": "1950-1959",
            paint: {{
              "fill-color": "#6539b3",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1960",
            source: "tileset1960",
            "source-layer": "1960-1969",
            paint: {{
              "fill-color": "#a032b2",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1970",
            source: "tileset1970",
            "source-layer": "1970-1979",
            paint: {{
              "fill-color": "#d124a9",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1980",
            source: "tileset1980",
            "source-layer": "1980-1989",
            paint: {{
              "fill-color": "#fd4dab",
            }},
            type: "fill",
          }},
          {{
            id: "tileset1990",
            source: "tileset1990",
            "source-layer": "1990-1999",
            paint: {{
              "fill-color": "#fea7d4",
            }},
            type: "fill",
          }},
          {{
            id: "tileset2000",
            source: "tileset2000",
            "source-layer": "2000-2009",
            paint: {{
              "fill-color": "#ff7911",
            }},
            type: "fill",
          }},
        ],
      }};

      mapboxgl.accessToken = "{mapbox_access_token}";
      var map = new mapboxgl.Map({{
        container: "map",
        style: mapStyle,
        center: [-118.2621, 34.0267],
        zoom: 12,
      }});

      map.on("mousemove", (e) => {{
        const features = map.queryRenderedFeatures(e.point);
        if (features[0]) {{
          document.getElementById("builtbox").innerHTML =
            features[0].properties.address +
            " was built in " +
            features[0].properties.YearBuilt;
        }}
      }});
    </script>
  </body>
</html>
"""

# Embed the HTML in Streamlit
st.components.v1.html(map_html, height=600)
