from geopandas import read_file
from sys import exit

# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

#checking the columns
print(world.columns)
print((world["ADM0_A3"]=="GBR").head())

# extract the UK, project, and extract the geometry
uk = world[((world["ADM0_A3"] == "GBR"))].to_crs("EPSG:27700").geometry.iloc[0]	# COMPLETE THIS LINE

# report geometry type
print(f"geometry type: {uk.geom_type}")

# quit the analysis if we are dealing with any geometry but a MultiPolygon
if uk.geom_type != 'MultiPolygon':
  print("Geometry is not a MultiPolygon, exiting...")
  exit()
  
# initialise variables to hold the coordinates and area of the largest polygon
biggest_area = 0
coord_list = []

# loop through each polygon in the multipolygon and find the biggest (mainland Great Britain)
for poly in uk.geoms:

    # if it is the biggest so far
    if poly.area>biggest_area:
       
        # store the new value for biggest area
        biggest_area = poly.area
        # store the coordinates of the polygon
        coord_list= list(poly.boundary.coords)	
#print largest area and number of coords
print(biggest_area)
print(len(coord_list))