#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")
from julespy import *
import numpy
import pylab
import matplotlib
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
    'figure.subplot.wspace' : 0.02,   # the amount of width reserved for blank space between subplots
    'figure.subplot.hspace' : 0.02,   # the amount of height reserved for white space between subplots
    'text.usetex': True ,
    'figure.figsize': fig_size}
    pylab.rcParams.update(params)
    
PreparePlotsParams()
# Start by reading some JULES output file, and processing it

p2=process_jules_output ("../../../OUTPUT/loobos.p1.30m.asc")

# Extract the dates
dates = numpy.array(p2.keys())

# Extract a few variables, such as
# * tstar
# * canopy
# * latentHeat
# * lsRain

tstar = numpy.array( [ p2[i]["tstar"] for i in dates])
canopy = numpy.array( [ p2[i]["canopy"] for i in dates])
latentHeat = numpy.array( [ p2[i]["latentHeat"] for i in dates])
lsRain = numpy.array( [ p2[i]["lsRain"] for i in dates])

# Now, convert dates into pylab numeric epoch

dates = pylab.datestr2num ( dates )

# Sort dates
i = numpy.argsort ( dates )
dates = dates[i]

#Order the other arrays
tstar = tstar[i]
canopy = canopy[i]
latentHeat = latentHeat[i]
lsRain = lsRain[i]

# Give us a figure
fig = pylab.figure()
var_list = [ tstar, canopy, latentHeat, lsRain ]
for (i, variable) in enumerate ( ['tstar', 'canopy', 'latentHeat', 'lsRain']):
    ax = fig.add_subplot(4, 1, i+1)
    ax.plot_date ( dates, var_list[i], '-', label=r'%s'%variable)
    ax.legend (loc="upper left", fancybox=True, shadow=True )
    monthsLoc = matplotlib.dates.MonthLocator()
    ax.xaxis.set_major_locator( monthsLoc )
    monthsFmt = matplotlib.dates.DateFormatter('%b/%y')
    ax.xaxis.set_major_formatter( monthsFmt )
    xtl = ax.get_xticklabels()
    [ label.set_visible(False) for label in xtl ]
    ax.grid (True )
xtl = ax.get_xticklabels()
[ label.set_visible(True) for label in xtl ]
fig.autofmt_xdate(bottom=0.18)
pylab.show()