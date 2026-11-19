
from geopandas import read_file
from sys import exit
from math import sqrt


# SETTINGS
# Set the percentage of nodes that you want to remove
SIMPLIFICATION_PERC = 98


# FUNCTIONS

def distance(x1, y1, x2, y2):
    """
    Use Pythagoras' theorem to calculate the distance
    between two points.
    """

    a = x1 - x2
    b = y1 - y2

    distance_value = sqrt(a**2 + b**2)

    return distance_value


def get_effective_area(a, b, c):
    """
    Calculate the area of a triangle made from points
    a, b and c using Heron's formula.
    """

    # Calculate the length of each side
    side_a = distance(b[0], b[1], c[0], c[1])
    side_b = distance(a[0], a[1], c[0], c[1])
    side_c = distance(a[0], a[1], b[0], b[1])

    # Calculate semi-perimeter of the triangle
    s = (side_a + side_b + side_c) / 2

    # Apply Heron's formula and return
    return sqrt(max(0, s * (s - side_a) * (s - side_b) * (s - side_c)))


def visvalingam_whyatt(node_list, n_nodes):

    # Create an empty list to store effective areas
    areas = []

    # Loop through each node, excluding the end points
    for i in range(1, len(node_list) - 1):

        # Calculate effective area using neighbouring nodes
        area = get_effective_area(
            node_list[i - 1],
            node_list[i],
            node_list[i + 1]
        )

        # Append the node and effective area to the list
        areas.append({"point": node_list[i], "area": area})

    # Add the end points back into the list
    areas.insert(0, {"point": node_list[0], "area": 0})

    areas.insert(
        len(areas),
        {"point": node_list[-1], "area": 0}
    )

    # Check that both lists contain the same number of nodes
    print("Original nodes:", len(node_list))
    print("Nodes stored in areas:", len(areas))

    # The simplification algorithm will be added later


# MAIN CODE

# Open a dataset of all countries in the world
world = read_file("../../data/natural-earth/ne_10m_admin_0_countries.shp")


# Extract the UK, project to British National Grid,
# and extract its geometry
uk = world[world["ADM0_A3"] == "GBR"].to_crs("EPSG:27700").geometry.iloc[0]


# Quit the analysis if the geometry is not a MultiPolygon
if uk.geom_type != "MultiPolygon":
    print("Geometry is not a MultiPolygon, exiting...")
    exit()


# Initialise variables to hold the coordinates and area
# of the largest polygon
biggest_area = 0
coord_list = []


# Loop through each polygon and find the biggest
# (mainland Great Britain)
for poly in uk.geoms:

    # If it is the biggest so far
    if poly.area > biggest_area:

        # Store the new biggest area
        biggest_area = poly.area

        # Store the coordinates of the polygon
        coord_list = list(poly.boundary.coords)


# Calculate how many nodes we need
n_nodes = int(
    len(coord_list) / 100.0 * (100 - SIMPLIFICATION_PERC)
)


# Ensure that there are at least 3 nodes
if n_nodes < 3:
    n_nodes = 3


# Call the Visvalingam-Whyatt function
simplified_nodes = visvalingam_whyatt(coord_list, n_nodes)
