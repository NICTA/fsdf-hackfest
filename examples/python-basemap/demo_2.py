#imports
from mpl_toolkits.basemap import Basemap
import headlessmpl
import numpy as np

#output image name and resolution
filename = "demo_2.png"
width = 1920
height = 1080

#map bounds
low_long = -180
high_long = 180
low_lat = -90
high_lat = 90

#setup map
fig = headlessmpl.figure(width, height)
axes = fig.add_subplot(111)
m = Basemap(projection='cyl', llcrnrlon=low_long,
        llcrnrlat=low_lat, urcrnrlon=high_long, urcrnrlat=high_lat,
        resolution = 'h', area_thresh =1000, ax=axes)
m.drawcoastlines(linewidth=0.5)
m.fillcontinents()
m.drawcountries(linewidth=0.5)
m.drawmapboundary(fill_color='#1C4E63')
m.fillcontinents(color='#63561B',lake_color='#1C4E63')

#generate some random data on a lat-long grid
lons, lats = np.mgrid[-180.:180.:100*1j,
                      -90:90:100*1j]
#pay no attention to the trig here, just for show
wave = np.sin(2.*(lats*np.random.random(lats.shape))/180.0)**8*np.cos(4.*lons/180.0)
mean = np.cos(2.*lats/180.0)*((np.sin(2.*lons/180.0))**2 + 2.)

#plot the data as a contour plot
m.contour(lons,lats,wave+mean,15,linewidths=1.5)

#write the map to a file
headlessmpl.figure_to_file(fig, filename)
