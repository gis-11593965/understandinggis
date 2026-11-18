from geopandas import read_file
from sys import exit

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# extract the UK, project, and extract the geometry
uk = world[((world["ADM0_A3"] == "GBR"))].to_crs("EPSG:27700").geometry.iloc[0]	# COMPLETE THIS LINE

# report geometry type
print(f"geometry type: {uk.geom_type}")

# quit the analysis if we are dealing with any geometry but a MultiPolygon
if uk.geom_type != 'MultiPolygon':
  print("Geometry is not a MultiPolygon, exiting...")
  exit()