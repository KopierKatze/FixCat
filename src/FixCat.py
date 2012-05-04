#!/usr/bin/python
"""
Copyright 2012 Alexandra Weiss, Franz Gregor

This file is part of FixCat.

FixCat is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FixCat is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FixCat.  If not, see <http://www.gnu.org/licenses/>.
"""
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
