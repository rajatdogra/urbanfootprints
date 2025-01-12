import os
import osmnx as ox
import folium
import geopandas as gpd

def fetch_streets():
    """Fetch streets data for Warsaw, Poland from OpenStreetMap."""
    graph = ox.graph_from_place("Warsaw, Poland", network_type="drive")
    streets = ox.graph_to_gdfs(graph, nodes=False, edges=True)
    return streets

def generate_maps():
    # Fetch streets data
    gdf = fetch_streets()
    gdf.set_crs('EPSG:4326', inplace=True)  # Ensure it's set to WGS84

    # Make sure data folder exists
    if not os.path.exists('data'):
        os.makedirs('data')

    # User-specific settings (simulated by shifting bounding box coordinates)
    for user_id in range(1, 11):
        minx, miny = 21.0 + 0.01 * user_id, 52.15 + 0.01 * user_id
        maxx, maxy = 21.1 + 0.01 * user_id, 52.20 + 0.01 * user_id

        # Filter data
        gdf['midpoint'] = gdf.geometry.apply(lambda x: x.interpolate(0.5, normalized=True))
        filtered_gdf = gdf[gdf['midpoint'].apply(lambda point: minx <= point.x <= maxx and miny <= point.y <= maxy)]

        # Create map centered around the mean of the points
        center = [filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()]
        m = folium.Map(location=center, zoom_start=12)
        for _, row in filtered_gdf.iterrows():
            folium.PolyLine([(pt[1], pt[0]) for pt in row.geometry.coords[:]], color='blue', weight=2.5).add_to(m)

        # Save to HTML specific to the user
        html_path = f'data/user{user_id}_map.html'
        m.save(html_path)
        print(f'Map for user{user_id} saved to {html_path}')

if __name__ == "__main__":
    generate_maps()
