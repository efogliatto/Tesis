#### import the simple module from the paraview
from paraview.simple import *

# create a new 'EnSight Reader'
lbmcase = EnSightReader(CaseFileName='lbm.case')

# Go to last time
times = lbmcase.TimestepValues

# Properties modified on lbmcase
lbmcase.PointArrays = ['rho', 'T', 'U']

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=lbmcase, Source='High Resolution Line Source')

# Properties modified on plotOverLine1
plotOverLine1.Tolerance = 2.0e-16

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point1 = [1.0, 0.0, 0.0]
plotOverLine1.Source.Point2 = [1.0, 600.0, 0.0]
plotOverLine1.Source.Resolution = 600


# Update pipeline to latest time

for t in times:

    plotOverLine1.UpdatePipeline( time = t )

    # save data
    
    SaveData('Caso_{}.csv'.format(int(t)), proxy=plotOverLine1)
