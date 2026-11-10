from geopandas import read_file

world = read_file("../../data/natural-earth/ne_50m_admin_0_countries.shp")
graticule = read_file("../../data/natural-earth/ne_110m_graticules_15.shp")
bbox = read_file("../../data/natural-earth/ne_110m_wgs84_bounding_box.shp")
print(world.columns)
# Calculate GDP per capita
world['gdp_per_capita'] = (world['GDP_MD_EST'] * 1000000) / world['POP_EST']
print(world.head())
from matplotlib.pyplot import subplots, savefig
ea_proj=("+proj=aeqd +lon_0=0 +lat_0=0 +datum=WGS84 +units=m +no_defs")
# reproject all three layers to equal earth
world = world.to_crs(ea_proj)
graticule = graticule.to_crs(ea_proj)
bbox = bbox.to_crs(ea_proj)
# create map axis object
my_fig, my_ax = subplots(1, 1, figsize=(16, 10))

# add bounding box and graticule layers
bbox.plot(
    ax = my_ax,
    color = 'darkturquoise',
    linewidth = 0,
    )

# plot the countries
world.plot(								# plot the world dataset
    ax = my_ax,						# specify the axis object to draw it to
    column = 'gdp_per_capita',		# specify the column used to style the dataset
    cmap = 'RdPu',				# specify the colour map used to style the dataset based on POP_EST
    scheme = 'quantiles',	# specify how the colour map will be mapped to the values in POP_EST
    linewidth = 0.5,			# specify the line width for the country outlines
    edgecolor = 'gray',		# specify the line colour for the country outlines
   legend = True,               #adding legend to map
legend_kwds = {
    'loc': 'lower left',
    'title': 'GDP per capita'
    } )

# plot the graticule
graticule.plot(
    ax = my_ax,
    color = 'white',
    linewidth = 0.5,
    )
# turn off the visible axes on the map
my_ax.axis('off')
#Add map Title
my_ax.set(title="GDP per capita: Equal Area Projection Coordinate Reference System")
# save the result
savefig('./out/gdp_per_capita.png')
print("done!")
