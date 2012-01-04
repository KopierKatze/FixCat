from multiprocessing import Process
from multiprocessing.sharedctypes import Array, Value
from multiprocessing.managers import SyncManager

import wx

from Controller import Controller
from gui.MainFrame import MainFrame



video_str = Array('c', 2**20*'_')
current_frame = Value('i', 0)

class ControllerManager(SyncManager):
  pass

myController = None
def getController():
  global myController, video_str, current_frame
  if myController is None:
    myController = Controller(video_str, current_frame)
  return myController

ControllerManager.register('getController', getController)

if __name__ == '__main__':
  controllermanager = ControllerManager()
  controllermanager.start()

  controllerproxy = controllermanager.getController()
  #controllerproxy = getController()
  #controllerproxy.new_project("../example/overlayed_video.avi", "../example/t2d1gl.asc", True)

  a = wx.App()
  e = MainFrame(video_str, current_frame, controllerproxy)
  e.Show()
  e.newProject("../example/overlayed_video.avi", "../example/t2d1gl.asc")
  a.MainLoop()
