#import basemap and the mpl file writer
from mpl_toolkits.basemap import Basemap
import headlessmpl

filename = "demo_1.png"
#image resolution
width = 1920
height = 1080

#bounds of the map
low_long = -180
high_long = 180
low_lat = -90
high_lat = 90

#create a new headless figure
fig = headlessmpl.figure(width, height)
axes = fig.add_subplot(111)

#create a basemap object with a cylindrical projection
m = Basemap(projection='cyl', llcrnrlon=low_long,
        llcrnrlat=low_lat, urcrnrlon=high_long, urcrnrlat=high_lat,
        resolution = 'h', area_thresh =1000, ax=axes)

#draw some boundaries etc
m.drawcoastlines()
m.fillcontinents()
m.drawcountries(linewidth=0.5)
m.drawmapboundary(fill_color='#1C4E63')
m.fillcontinents(color='#63561B',lake_color='#1C4E63')

#write the resultant map to a file
headlessmpl.figure_to_file(fig, filename)
