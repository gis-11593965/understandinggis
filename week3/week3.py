from math import sqrt
from geopandas import read_file

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

#Testing Distance functio
print(distance(345678,456789,445678,556789))
        
# read in shapefiles, ensure that they all have the same CRS
pop_points = read_file("../../data/gulu/pop_points.shp")
water_points = read_file("../../data/gulu/water_points.shp").to_crs(pop_points.crs)
gulu_district = read_file("../../data/gulu/district.shp").to_crs(pop_points.crs)

print(water_points.estimate_utm_crs(datum_name='Arc 1960'))


