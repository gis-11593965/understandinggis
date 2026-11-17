from geopandas import read_file, GeoSeries
from matplotlib.pyplot import subplots, savefig, title
from pyproj import Geod

# load the shapefile of countries - this gives a table of 12 columns and 246 rows (one per country)
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")

# print a list of all of the columns in the shapefile
print(world.columns)

# extract the country rows as a GeoDataFrame object with 1 row
usa = world.loc[(world.ISO_A3 == 'USA')]

print(type(usa))

# extract the geometry columns as a GeoSeries object
usa_col = usa.geometry

print(type(usa_col))

# extract the geometry objects themselves from the GeoSeries
usa_geom = usa_col.iloc[0]

print(type(usa_geom))

# extract the country rows as a GeoDataFrame object with 1 row
mex= world.loc[(world.ISO_A3=='MEX')]

print(type(mex))

# extract the geometry colums as a Geoseries object
mex_col=mex.geometry

print(type(mex_col))

# extract the geometry objects themselves from the GeoSeries
mex_geom= mex_col.iloc[0]

# calculate the intersection of the geometry objects
border = usa_geom.intersection(mex_geom)

# Displaying border
print(border)

# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# plot the border
GeoSeries(border).plot(
  ax = my_ax
	)

# save the image
savefig('./out/first-border.png')

# set which ellipsoid you would like to use
g = Geod(ellps='WGS84')

print(border)

# loop through each segment in the line and print the coordinates
for segment in border.geoms:
	print(f"from:{segment.coords[0]}\tto:{segment.coords[1]}")
    
# initialise a variable to hold the cumulative length
cumulative_length = 0

# loop through each segment in the line
for segment in border.geoms:

	# THIS LINE NEEDS COMPLETING
	distance = g.inv(
        segment.coords[0][0],
        segment.coords[0][1],
        segment.coords[1][0],
        segment.coords[1][1]
        )[2]

	# add the distance to our cumulative total
	cumulative_length += distance
    
#total cumulative border distance
print(cumulative_length)