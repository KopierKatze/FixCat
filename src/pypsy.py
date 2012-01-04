from multiprocessing import Process
from multiprocessing.sharedctypes import Array, Value
from multiprocessing.managers import SyncManager

import wx

from Controller import Controller
from gui.MainFrame import MainFrame


myController = None
def getController():
  global myController, video_str, current_frame
  if myController is None:
    myController = Controller(video_str, current_frame)
  return myController

def set_shared_vars(v, f):
  global video_str, current_frame, myController

  myController = None

  video_str = v
  current_frame = f

class ControllerManager(SyncManager):
  pass

ControllerManager.register('getController', getController)
if __name__ == '__main__':
  video_str = Array('c', 2**20*'_')
  current_frame = Value('i', 0)

  controllermanager = ControllerManager()
  controllermanager.start(set_shared_vars, (video_str, current_frame))

  controllerproxy = controllermanager.getController()

  a = wx.App()
  e = MainFrame(video_str, current_frame, controllerproxy)
  e.Show()
  e.newProject("../example/overlayed_video.avi", "../example/t2d1gl.asc")
  a.MainLoop()
