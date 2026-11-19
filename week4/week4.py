from geopandas import read_file
from sys import exit
from math import sqrt
# open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")


# extract the UK, project, and extract the geometry
uk = world[((world["ADM0_A3"] == "GBR"))].to_crs("EPSG:27700").geometry.iloc[0]	# COMPLETE THIS LINE


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

# set the percentage of nodes that you want to remove
SIMPLIFICATION_PERC = 98

def get_effective_area(a, b, c):
	"""
	* Calculate the area of a triangle made from the points a, b and c using Heron's formula
	* 	https://en.wikipedia.org/wiki/Heron%27s_formula
	"""
	# calculate the length of each side
	side_a = distance(b[0], b[1], c[0], c[1])
	side_b = distance(a[0], a[1], c[0], c[1])
	side_c = distance(a[0], a[1], b[0], b[1])

	# calculate semi-perimeter of the triangle (perimeter / 2)
	s = (side_a + side_b + side_c) / 2

	# apply Heron's formula and return
	return sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

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

# how many nodes do we need?
n_nodes = int(len(coord_list) / 100.0 * (100 - SIMPLIFICATION_PERC))

# ensure that there are at least 3 nodes (minimum for a polygon)
if n_nodes < 3:
	n_nodes = 3 
    
    