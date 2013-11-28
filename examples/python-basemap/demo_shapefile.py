import collections
import csv
import shapefile
import numpy as np
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap
import headlessmpl

#Output file
filename = "geolpldd.shp"
width = 1920
height = 1080

#NSW Boundaries
low_long = 135
high_long = 155
low_lat = -39
high_lat = -27


def load_colors():
    """load a dictionary of colours from the CSV file from the 
    Geology1M dataset from Geoscience Australia"""
    csv_list = []
    with open('colour_guide.txt', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        csv_list = [row for row in reader]
    keys = [k[0] for k in csv_list]
    csv_list = csv_list[1:]
    #scale colours between 0 and 1
    values = [(float(k[1])/255.0, float(k[2])/255.0, float(k[3])/255.0)
              for k in csv_list]
    #Give a sensible default of a bluish, water-ish colour
    colour_dict = collections.defaultdict(lambda:(0.11,0.306,0.388),zip(keys, values))
    return colour_dict

def setup_axes():
    """setup a headless basemap figure with a geostationary projection"""
    fig = headlessmpl.figure(width, height)
    axes = fig.add_subplot(111)
    globe = Basemap(projection='geos', llcrnrlon=low_long,
            llcrnrlat=low_lat, urcrnrlon=high_long, urcrnrlat=high_lat,
            lon_0=150,resolution = 'h', area_thresh = 1000, ax=axes)
    globe.bluemarble()
    globe.drawcoastlines()
    globe.drawcountries()
    globe.drawstates()
    return globe, axes, fig

def add_data(globe, axes, color_dict):
    """Add shapefile polygons to the matplotlib axes"""
    file_object = shapefile.Reader(filename)
    shapes = file_object.shapes()
    records = file_object.records()
    #iterate over all but the first 20 polygons (they're junk)
    for record, shape in zip(records[20:],shapes[20:]):
        #this entry is the colour code
        description = record[6]
        lons,lats = zip(*shape.points)
        #transform the lat/long coords to the right projection
        data = np.array(globe(lons, lats)).T
        #shapefile shapes can have disconnected parts, we have
        #to check
        if len(shape.parts) == 1:
            segs = [data,]
        else:
            segs = []
            for i in range(1,len(shape.parts)):
                #add all the parts
                index = shape.parts[i-1]
                index2 = shape.parts[i]
                segs.append(data[index:index2])
            segs.append(data[index2:])
        #Add all the parts we've found as a set of lines
        lines = LineCollection(segs,antialiaseds=(1,))
        lines.set_facecolors(color_dict[description])
        lines.set_edgecolors('k')
        lines.set_linewidth(0.1)
        #add the collection to the active axes
        axes.add_collection(lines)

def main():
    color_dict = load_colors()
    globe, axes, fig = setup_axes()
    add_data(globe, axes, color_dict)
    globe.drawmapboundary(fill_color='#1C4E63')
    globe.fillcontinents(color='#63561B',lake_color='#1C4E63')
    #write the result out to a file
    headlessmpl.figure_to_file(fig, "shapefile.png")


if __name__ == "__main__":
    main()
