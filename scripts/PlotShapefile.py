#from scipy import *
from numpy import *
import osgeo.ogr as ogr
import pylab
import matplotlib.patches
from mpl_toolkits.basemap import Basemap
from matplotlib.colorbar import ColorbarBase, make_axes
"""
Un programa que ejemplifica la conexion OGR con la base de datos espacial PostGIS, usando Python
y matplotlib para hacer un mapa.

(c) J L Gomez Dans, 2007
"""

def PreparePlotsParams ():
        import pylab
        import numpy
        fig_width_pt = 615.0  # Get this from LaTeX using \showthe\columnwidth
        inches_per_pt = 1.0/72.27               # Convert pt to inches
        golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
        fig_width = fig_width_pt*inches_per_pt  # width in inches
        fig_height =fig_width*golden_mean       # height in inches
        fig_size = [fig_width,fig_height]
        params = {'backend': 'ps',
          'ps.papersize': 'a4',
          'axes.formatter.limits' : [-3, 3], #No large numbers with loads of 0s
          'axes.labelsize': 10,
          'text.fontsize': 8,
          'legend.fontsize': 8,
          'xtick.labelsize': 8,
          'ytick.labelsize': 8,
          'figure.subplot.left'  : 0.1,  # the left side of the subplots of the figure
          'figure.subplot.right' : 0.95,    # the right side of the subplots of the figure
          'figure.subplot.bottom' : 0.1,   # the bottom of the subplots of the figure
          'figure.subplot.top' : 0.8,      # the top of the subplots of the figure
          'figure.subplot.wspace' : 0.1,   # the amount of width reserved for blank space between subplots
          'figure.subplot.hspace' : 0.2,   # the amount of height reserved for white space between subplots
          'text.usetex': True ,
          'figure.figsize': fig_size}
        pylab.rcParams.update(params)

PreparePlotsParams()
pft_name = ["TrBE","TrBR","TeNE","TeBE","TeBS","BoNE","BoNS","BoBS","TeH","TrH"]
pft = 0
C=pylab.cm.jet(arange(0,256,1))
fig = pylab.figure (figsize=(8,9))

for pft in arange(1,10):
	ax=fig.add_subplot(3,3,pft)
	## SAfrica
	mapa = Basemap(projection='merc', lat_ts=0.,\
			llcrnrlat=-20,urcrnrlat=-10,\
			llcrnrlon=11,urcrnrlon=31,\
			rsphere=6371200.,resolution='h',area_thresh=10000)
	## Borneo
	#mapa = Basemap(projection='merc', lat_ts=0.,\
			#llcrnrlat=-5,urcrnrlat=8,\
			#llcrnrlon=108,urcrnrlon=120,\
			#rsphere=6371200.,resolution='h',area_thresh=10000)
	##NOz
	#mapa = Basemap(projection='merc', lat_ts=0.,\
			#llcrnrlat=-20,urcrnrlat=-10,\
			#llcrnrlon=120,urcrnrlon=150,\
			#rsphere=6371200.,resolution='h',area_thresh=10000)
			
			
	try:
		g = ogr.Open ("/home/ucfajlg/spitfire/data/spinup_%d.shp"%pft)
		print g.name
		L = g.GetLayer(0)
		N = 0
		feat = L.GetNextFeature()
	#	mapa = Basemap(llcrnrlon=5,llcrnrlat=-21,urcrnrlon=32,urcrnrlat=-8,
	#            projection='mill') 
	#		ax = pylab.gca()		
		while feat is not None:
			field_count = L.GetLayerDefn().GetFieldCount()
			cover=int(feat.GetFieldAsDouble('FPC_GRID') *256)
			if cover>255:
				cover=255
			geo = feat.GetGeometryRef()
			g1 = geo.GetGeometryRef( 0 )
			x =[g1.GetX(i) for i in range(g1.GetPointCount()) ]
			y =[g1.GetY(i) for i in range(g1.GetPointCount()) ]
			x = array( x, 'f')
			y = array (y, 'f')
			(X,Y) = mapa.projtran(x,y)
			ax.fill(X,Y,'k',linewidth=0,facecolor=C[cover])
			feat = L.GetNextFeature()
		g.Destroy()
	except:
		pass
		#coast=mapa.drawcoastlines(linewidth=1.5,facecolor="gray")

	mapa.drawlsmask( (220,220,220,255), rgba_ocean = (0,0,255,0))
	coast=mapa.drawcoastlines(linewidth=1.5)
	mapa.drawcountries(linewidth=1.0, color='w')
	rivers=mapa.drawrivers()
	mapa.drawparallels(arange(-90,91,2),labels=[1,0,0,0])
	mapa.drawmeridians(arange(-180,181,10),labels=[0,0,0,1]) 
	#pylab.xlabel("Easting [m]")
	#pylab.ylabel("Northing [m]")
	#pylab.grid(True)
	pylab.title("%s"%pft_name[pft])
#	pylab.colorbar()
#	pylab.axis([5.0, 32, -21,-11])
#(12.000000, -22.500000) - (150.000000, 6.500000)
#fig.subplots_adjust(top=0.85)
#ax = fig.add_axes([0.12, 0.9, 0.8, 0.05])
#Mapeo = matplotlib.cm.ScalarMappable ( norm=matplotlib.colors.NoNorm(vmin=0, vmax=1),\
#		cmap=matplotlib.cm.jet)
#pylab.colorbar(cax=ax, orientation='horizontal')
fig.subplots_adjust(top=0.85,wspace=0.25)
cax = fig.add_axes([0.12, 0.9, 0.8, 0.05])
cbase = matplotlib.colorbar.ColorbarBase( cax, cmap=pylab.cm.jet, orientation='horizontal' )

pylab.show()
pylab.savefig ("/tmp/SAfrica_PFTs_AfterSpinup.eps")
pylab.savefig ("/tmp/SAfrica_PFTs_AfterSpinup.pdf")
