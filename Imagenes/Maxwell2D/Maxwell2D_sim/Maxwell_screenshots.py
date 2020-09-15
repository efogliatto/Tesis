# trace generated using paraview version 5.8.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'EnSight Reader'
lbmcase = EnSightReader(CaseFileName='/home/fogliate/Documents/Tesis/Imagenes/Maxwell2D/lbm.case')
lbmcase.PointArrays = ['rho', 'T', 'f0', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'U']

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# Properties modified on lbmcase
lbmcase.PointArrays = ['rho']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [829, 546]

# get layout
layout1 = GetLayout()

# show data in view
lbmcaseDisplay = Show(lbmcase, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'rho'
rhoLUT = GetColorTransferFunction('rho')

# get opacity transfer function/opacity map for 'rho'
rhoPWF = GetOpacityTransferFunction('rho')

# trace defaults for the display properties.
lbmcaseDisplay.Representation = 'Surface'
lbmcaseDisplay.ColorArrayName = ['POINTS', 'rho']
lbmcaseDisplay.LookupTable = rhoLUT
lbmcaseDisplay.OSPRayScaleArray = 'rho'
lbmcaseDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
lbmcaseDisplay.SelectOrientationVectors = 'None'
lbmcaseDisplay.ScaleFactor = 20.0
lbmcaseDisplay.SelectScaleArray = 'rho'
lbmcaseDisplay.GlyphType = 'Arrow'
lbmcaseDisplay.GlyphTableIndexArray = 'rho'
lbmcaseDisplay.GaussianRadius = 1.0
lbmcaseDisplay.SetScaleArray = ['POINTS', 'rho']
lbmcaseDisplay.ScaleTransferFunction = 'PiecewiseFunction'
lbmcaseDisplay.OpacityArray = ['POINTS', 'rho']
lbmcaseDisplay.OpacityTransferFunction = 'PiecewiseFunction'
lbmcaseDisplay.DataAxesGrid = 'GridAxesRepresentation'
lbmcaseDisplay.PolarAxes = 'PolarAxesRepresentation'
lbmcaseDisplay.ScalarOpacityFunction = rhoPWF
lbmcaseDisplay.ScalarOpacityUnitDistance = 8.256564438936037
lbmcaseDisplay.ExtractedBlockIndex = 1

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
lbmcaseDisplay.ScaleTransferFunction.Points = [0.08249971270561218, 0.0, 0.5, 0.0, 0.08416624367237091, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
lbmcaseDisplay.OpacityTransferFunction.Points = [0.08249971270561218, 0.0, 0.5, 0.0, 0.08416624367237091, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera()

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [100.0, 100.0, 10000.0]
renderView1.CameraFocalPoint = [100.0, 100.0, 0.0]

# show color bar/color legend
lbmcaseDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# hide color bar/color legend
lbmcaseDisplay.SetScalarBarVisibility(renderView1, False)

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [100.0, 100.0, 10000.0]
renderView1.CameraFocalPoint = [100.0, 100.0, 0.0]
renderView1.CameraParallelScale = 141.4213562373095

# save screenshot
SaveScreenshot('/home/fogliate/Documents/Tesis/Imagenes/Maxwell2D/prueba.jpeg', renderView1, ImageResolution=[1658, 1092],
    TransparentBackground=1, 
    # JPEG options
    Quality=100)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [100.0, 100.0, 10000.0]
renderView1.CameraFocalPoint = [100.0, 100.0, 0.0]
renderView1.CameraParallelScale = 141.4213562373095

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).