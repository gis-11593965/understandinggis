from math import sqrt
from geopandas import read_file
from shapely import STRtree
from matplotlib_scalebar.scalebar import ScaleBar
from matplotlib.pyplot import subplots, savefig, title

def distance(x1, y1, x2, y2):
        """
    	* Use Pythagoras' theorem to measure the distance. This is acceptable in this case because:
    	*	 - the CRS of the data is a local projection
    	*	 - the distances are short
    	*  - computational efficiency is important (as we are making many measurements)
    	"""
        #making a and b a variabiable
        a=(x1-x2)
        b=(y1-y2)
        
        #caculating distance using pythagorus theorem
        distance=sqrt(a**2 + b**2)
        return(distance)

        
# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp").to_crs(pop_points.crs)
gulu_district = read_file("../../data/gulu/district.shp").to_crs(pop_points.crs)

#How many well and population points there are
print(f"population points: {len(pop_points)}")
print(f"Initial wells: {len(water_points)}")

# get the geometries from the water points geodataframe as a list
geoms = water_points.geometry.to_list()

# initialise an instance of an STRtree using the geometries
idx = STRtree(geoms)

# get the one and only polygon from the district dataset
polygon = gulu_district.geometry.iloc[0]

# how many rows are we starting with?
print(f"Initial wells: {len(water_points.index)}")

# get the indexes of wells that intersect bounds of the district
possible_matches_index = idx.query(polygon)

# use those indexes to extract the possible matches from the GeoDataFrame
possible_matches = water_points.iloc[possible_matches_index]

# how many rows are left now? 
print(f"Potential wells: {len(possible_matches.index)}")

# then search the possible matches for precise matches using the slower but more precise method
precise_matches = possible_matches.loc[possible_matches.within(polygon)]

# how many rows are left now?
print(f"Filtered wells: {len(precise_matches.index)}")

# rebuild the spatial index using the new, smaller dataset
gulu_geoms=precise_matches.geometry.to_list()
idx = STRtree(gulu_geoms)

#Empty list to store distance calculations
distances=[]

for id, house in pop_points.iterrows():
    # use the spatial index to get the index of the closest well
    nearest_well_index = idx.nearest(house.geometry)
    # use the spatial index to get the closest well object from the original dataset
    nearest_well=precise_matches.iloc[nearest_well_index].geometry.geoms[0]
    # store the distance to the nearest well
    distances.append(distance(house.geometry.x, house.geometry.y, nearest_well.x, nearest_well.y))
    
#First five entries to check
print(distances[:5])

# store distance to nearest well
pop_points['nearest_well'] = distances

#print column names
print(pop_points.columns)

#calculating average
mean=sum(distances)/len(distances)

#Average, min and max calculations
print(f"Minimum distance to water in Gulu District: {min(distances):,.0f}m.")
print(f"Mean distance to water in Gulu District: {mean:,.0f}m.")
print(f"Maximum distance to water in Gulu District: {max(distances):,.0f}m.")

# create map axis object
fig, my_ax = subplots(1, 1, figsize=(16, 10))

# remove axes
my_ax.axis('off')

# add title
title("Distance to Nearest Well, Gulu District, Uganda")

# add the district boundary
gulu_district.plot(
    ax = my_ax,
    color = (0, 0, 0, 0),	# this is (red, green, blue, alpha) and means black, but transparent (alpha=0)
    linewidth = 1,
	edgecolor = 'black',		# this is just a shortcut for (0, 0, 0, 1)
    )

# plot the locations, coloured by distance to water
pop_points.plot(
    ax = my_ax,
    column = 'nearest_well',
    linewidth = 0,
	markersize = 1,
    cmap = 'RdYlBu_r',
    scheme = 'quantiles',
    legend = 'True',
    legend_kwds = {
        'loc': 'lower right',
        'title': 'Distance to Nearest Well'
        }
    )

# add north arrow
x, y, arrow_length = 0.98, 0.99, 0.1
my_ax.annotate('N', xy=(x, y), xytext=(x, y-arrow_length),
	arrowprops=dict(facecolor='black', width=5, headwidth=15),
	ha='center', va='center', fontsize=20, xycoords=my_ax.transAxes)

# add scalebar
my_ax.add_artist(ScaleBar(dx=1, units="m", location="lower left", length_fraction=0.25))

# save the result
savefig('out/3.png', bbox_inches='tight')
print("done!")