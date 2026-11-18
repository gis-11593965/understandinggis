from math import sqrt
from geopandas import read_file
from shapely import STRtree

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


