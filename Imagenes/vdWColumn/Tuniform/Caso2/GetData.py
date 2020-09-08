#### import the simple module from the paraview
from paraview.simple import *

# create a new 'EnSight Reader'
lbmcase = EnSightReader(CaseFileName='lbm.case')

# Go to last time
times = lbmcase.TimestepValues

# Properties modified on lbmcase
lbmcase.PointArrays = ['rho', 'T']

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=lbmcase, Source='High Resolution Line Source')

# Properties modified on plotOverLine1
plotOverLine1.Tolerance = 2.2e-16

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point1 = [1.0, 0.0, 0.0]
plotOverLine1.Source.Point2 = [1.0, 600.0, 0.0]
plotOverLine1.Source.Resolution = 600


# Update pipeline to latest time
plotOverLine1.UpdatePipeline( time = times[-1] )


# save data
SaveData('Caso.csv', proxy=plotOverLine1)
