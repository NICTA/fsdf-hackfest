from mpl_toolkits.basemap import Basemap
import headlessmpl
import numpy as np

#output file
filename = "demo_4.png"
width = 1920
height = 1080

#map bounds
long_0 = -107
lat_1 = 50
low_long = -145
high_long = -2.5
low_lat = 1.0
high_lat = 20.0

#setup Lambert Conformal Conic projection
fig = headlessmpl.figure(width, height)
axes = fig.add_subplot(111)
m = Basemap(projection='lcc', llcrnrlon=low_long,
        llcrnrlat=low_lat, urcrnrlon=high_long, urcrnrlat=high_lat,
        lat_1=lat_1, lon_0=long_0,
        resolution = 'h', area_thresh =1000, ax=axes)

#add a nice background
m.bluemarble()
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)

#make some random data
lons, lats = np.mgrid[-180.:180.:100*1j,
        -90:90:100*1j]
wave = np.sin(2.*(lats*np.random.random(lats.shape))/180.0)**8*np.cos(4.*lons/180.0)
mean = np.cos(2.*lats/180.0)*((np.sin(2.*lons/180.0))**2 + 2.)
# # compute native map projection coordinates of lat/lon grid.
x, y = m(lons, lats)
# contour data over the map.
cs = m.contour(x,y,wave+mean,15,linewidths=1.5)

#write the output file
headlessmpl.figure_to_file(fig, filename)
