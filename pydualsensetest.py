from pydualsense import pydualsense, TriggerModes

ds = pydualsense() # open controller
ds.init() # initialize controller
ds.light.setColorI(255,0,0) # set touchpad color to red
ds.triggerL.setMode(TriggerModes.Rigid)
ds.triggerL.setForce(1, 255)
ds.close() # closing the controller