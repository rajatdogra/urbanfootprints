import os
import sqlite3
import folium
import warnings
import geopandas as gpd
from shapely.wkt import loads

def generate_maps(db_path="streets_assignment.db"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Ensure the data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Fetch distinct users and their details
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT user_id, user_name FROM user_details")
    users = cursor.fetchall()

    warnings.filterwarnings("ignore")

    for user_id, user_name in users:
        # Query streets visited by the user
        query = f"""
        SELECT sm.geometry
        FROM user_street_assignment usa
        JOIN street_mapping sm ON usa.street_index = sm.street_id
        WHERE usa.user_id = {user_id}
        """
        cursor.execute(query)
        streets = cursor.fetchall()

        if not streets:
            # print(f"No streets found for user {user_name}")
            continue

        # Convert WKT geometries to Shapely objects
        geometries = [loads(row[0]) for row in streets]

        # Create a GeoDataFrame for easier spatial operations
        gdf = gpd.GeoDataFrame({"geometry": geometries}, crs="EPSG:4326")

        # Generate a folium map centered on the user's streets
        center = [
            gdf.geometry.centroid.y.mean(),
            gdf.geometry.centroid.x.mean(),
        ]
        m = folium.Map(location=center, zoom_start=12)

        # Add streets to the map
        for geom in geometries:
            if geom.geom_type == "LineString":
                folium.PolyLine([(pt[1], pt[0]) for pt in geom.coords], color="blue", weight=2.5).add_to(m)

        # Save the map to an HTML file
        html_path = f"data/{user_name}_map.html"
        m.save(html_path)
        # print(f"Map for {user_name} saved to {html_path}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    generate_maps()
