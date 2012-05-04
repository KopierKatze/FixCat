#!/usr/bin/python
from multiprocessing import Process, freeze_support
from multiprocessing.sharedctypes import Array, Value
from multiprocessing.managers import SyncManager

import wx

from FixCat.Controller import Controller
from FixCat.gui.MainFrame import MainFrame

from FixCat import Config


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
    # activate multiprocessing freeze support (needed to build executables)
    freeze_support()
    # configuration file check
    try:
        # will raise configerror on problems
        Config.Config()
    except Config.ConfigError, e:
        app = wx.PySimpleApp()
        wx.MessageBox('Error while loading config file: %s'% e.message, 'Error')
        app.MainLoop()
        raise SystemExit()

    video_str = Array('c', 2**20*'_')
    current_frame = Value('i', 0)

    controllermanager = ControllerManager()
    controllermanager.start(set_shared_vars, (video_str, current_frame))

    controllerproxy = controllermanager.getController()

    a = wx.PySimpleApp()
    e = MainFrame(video_str, current_frame, controllerproxy)
    e.Show()
    a.MainLoop()
