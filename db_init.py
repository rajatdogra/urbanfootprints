# Gen AI Used to add comments to script and make it clean (used a notebook to develop 
# which was not the cleanest code, so asked AI to make it a bit clean, remove all print/debugging 
# related statements.)

import osmnx as ox
import warnings
import pandas as pd
from shapely.geometry import Polygon, box
from geopandas import GeoDataFrame
import random
import sqlite3
from faker import Faker


# Step 1: Get Warsaw street data
graph = ox.graph_from_place("Warsaw, Poland", network_type="drive")
streets = ox.graph_to_gdfs(graph, nodes=False, edges=True).dropna(subset=['name']).reset_index()

# If we drop other lanes, we have 37531 streets to choose from
streets = streets.dropna(subset=['name']).reset_index()

# Step 2: Divide the city into 9 parts
polygons = []
bounds = ox.geocode_to_gdf("Warsaw, Poland").total_bounds  # Warsaw coordinates
for latitude in range(3):
    for longitude in range(3):
        lat_start = bounds[1] + (bounds[3] - bounds[1]) / 3 * latitude
        lon_start = bounds[0] + (bounds[2] - bounds[0]) / 3 * longitude
        lat_end = bounds[1] + (bounds[3] - bounds[1]) / 3 * (latitude + 1)
        lon_end = bounds[0] + (bounds[2] - bounds[0]) / 3 * (longitude + 1)

        polygon = Polygon([(lon_start, lat_start), (lon_end, lat_start),
                           (lon_end, lat_end), (lon_start, lat_end)])
        polygons.append(polygon)

# Step 3: Assign streets to polygons
streets['Index'] = streets.index
streets['Polygon'] = None

for i in streets.index:
    for polygon in polygons:
        if streets.loc[i, 'geometry'].within(polygon):
            streets.loc[i, 'Polygon'] = polygons.index(polygon)
            break  # Stop once the polygon is found

# Step 4: Create a DataFrame with columns for 37531 streets and 10 users
df = pd.DataFrame(columns=range(37531), index=range(1, 11))

# Assign 'User_id' column as integers
df['user_id'] = df.index.astype(int)

# Simulate street assignment
for user in range(1, 11):  # User IDs are from 1 to 10
    p = random.randint(1, 7)
    p2 = p + 1
    data = streets[streets['Polygon'].isin([p, p2])]
    s = random.randint(2000, 2500)
    n = data['Index'].sample(s)
    for i in n:
        df.loc[user, i] = 1

# Step 5: Reshape the DataFrame from wide to long format
long_df = (
    df.set_index("user_id")
    .stack()
    .reset_index()
    .rename(columns={"level_1": "street_index", 0: "Assigned"})
)

# Filter rows where streets are assigned (value is 1)
long_df = long_df[long_df["Assigned"] == 1].drop(columns=["Assigned"])

warnings.filterwarnings("ignore")

# Save to SQLite
conn = sqlite3.connect("streets_assignment.db")
long_df.to_sql("user_street_assignment", conn, if_exists="replace", index=False)

# Generate user data
fake = Faker()
df = pd.DataFrame(columns=['user_id', 'name', 'user_name', 'age', 'days_from_start'], index=range(10))

# Populate the DataFrame
for user in range(10):
    name = fake.name()
    df.loc[user, 'user_id'] = user + 1
    df.loc[user, 'name'] = name
    df.loc[user, 'user_name'] = name.replace(" ", "")
    df.loc[user, 'age'] = fake.random_int(min=18, max=80)
    df.loc[user, 'days_from_start'] = fake.random_int(min=14, max=150)

# Ensure correct data types
df['user_id'] = df['user_id'].astype(int)
df['age'] = df['age'].astype(int)
df['days_from_start'] = df['days_from_start'].astype(int)

# Save user details to SQLite
df.to_sql("user_details", conn, if_exists="replace", index=False)

# Step 7: Save street mapping
streets_geometry = streets[["geometry", "Index", "name"]]
streets_geometry["name"] = streets_geometry["name"].astype(str)
streets_geometry = streets_geometry.rename(columns={"Index": "street_id"})

# Print the list of usernames
print("Generated Usernames:")
print(df['user_name'].tolist())

# Convert geometries to WKT format
streets_geometry["geometry"] = streets_geometry["geometry"].apply(lambda geom: geom.wkt)

# Save to SQLite
streets_geometry.to_sql("street_mapping", conn, if_exists="replace", index=False)

# Close the SQLite connection
conn.close()
