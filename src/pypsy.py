from multiprocessing import Process
from multiprocessing.sharedctypes import Array, Value
from multiprocessing.managers import SyncManager

import wx

from Controller import Controller
from gui.MainFrame import MainFrame



video_str = Array('c', 2**20*'_')
video_str_length = Value('i', 0)
frame_size = Array('i', [0,0])

class ControllerManager(SyncManager):
  pass

myController = None
def getController():
  global myController, video_str, video_str_length, frame_size
  if myController is None:
    myController = Controller(video_str, video_str_length, frame_size)
  return myController

ControllerManager.register('getController', getController)

if __name__ == '__main__':
  controllermanager = ControllerManager()
  controllermanager.start()

  controllerproxy = controllermanager.getController()
  #controllerproxy = getController()
  controllerproxy.new_project("../example/overlayed_video.avi", "../example/t2d1gl.asc", True)

  a = wx.App()
  e = MainFrame(video_str, video_str_length, frame_size, controllerproxy)
  e.Show()
  a.MainLoop()
