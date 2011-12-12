import wx
import os
import cv
class Example(wx.Frame): 
    ID_TIMER_PLAY = 5

    def __init__(self, parent, title):    
        super(Example, self).__init__(parent, title=title, 
            size=(900, 600))

        self.InitUI()
        self.Centre()
        #self.Show()     
        self.dirname=""
        

    def InitUI(self):
        self.playing = False
        self.bmp = None
        # menubar elements
        statusBar = self.CreateStatusBar()

        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "open")
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "&About", "Information about")
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit" , "terminate")

        codecMenu = wx.Menu()
        codecMenu.Append(wx.ID_SETUP, "&Codecs", "set codec")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(codecMenu, "C&odecs")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuSave)
        
        #sizer boxes for panels
        mainbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.videopanel = wx.Panel(self, -1)
        #videopanel.SetBackgroundColour(wx.BLACK)
        pnl2 = wx.Panel(self, -1) 
        self.slider1 = wx.Slider(pnl2, -1, 0, 0, 1000)
        pause = wx.Button(pnl2, -1, "Pause")
        play  = wx.Button(pnl2, -1, "Play")
        next  = wx.Button(pnl2, -1, "Next")
        prev  = wx.Button(pnl2, -1, "Prev")
        
        self.Bind(wx.EVT_SLIDER, self.onSlider, self.slider1)
        self.Bind(wx.EVT_BUTTON, self.onPlay, play)
        self.Bind(wx.EVT_TOOL, self.onStop, pause)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(self.slider1, 1)
        hbox2.Add(pause)
        hbox2.Add(play, flag=wx.RIGHT, border=5)
        hbox2.Add(next, flag=wx.LEFT, border=5)
        hbox2.Add(prev)
        hbox2.Add((150, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)

        vbox.Add(hbox1, 2, wx.EXPAND | wx.BOTTOM, 10)
        vbox.Add(hbox2, 1, wx.EXPAND)
        pnl2.SetSizer(vbox)
        
        
        
        categorybox = wx.BoxSizer(wx.VERTICAL)
        
        #table content for category
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Kategorie')
        self.lc.InsertColumn(1, 'Shortcut')
        self.lc.SetColumnWidth(0, 100)
        self.lc.SetColumnWidth(1, 90)
        
        # add table to category box
        categorybox.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)
        
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        sizer.Add(pnl2, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        mainbox.Add(sizer,3, flag=wx.EXPAND)
        mainbox.Add(categorybox,1, flag=wx.EXPAND)      
        self.SetSizer(mainbox)    
        
        self.playTimer = wx.Timer(self, self.ID_TIMER_PLAY)
        self.Bind(wx.EVT_TIMER, self.onNextFrame, self.playTimer)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Show(True)
        
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "<slipsum>", "about eyepy", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnExit(self, e):
        self.Close(True)
        
    def OnOpen(self, e):
        filters = 'AVI files (*.avi)|*.avi|All files (*.*)|*.*'
       
        dlg = wx.FileDialog(None, message = 'Select AVI files....', wildcard=filters, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.capture = cv.CaptureFromFile(filename)
            
            frame = cv.QueryFrame(self.capture)
            totalFrames = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_COUNT)

            self.slider1.SetRange(0, totalFrames)
            self.slider1.SetValue(0)
            self.onSlider(wx.EVT_SLIDER)

            if frame:
                cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
                self.bmp = wx.BitmapFromBuffer(frame.width, frame.height, frame.tostring())
                #self.SetSize((frame.width, frame.height))
                sliderSize = self.slider1.GetSize()
                self.slider1.SetClientSizeWH(frame.width - 100, sliderSize.GetHeight())

    def onSlider(self, evt):
        frameNumber = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_POS_FRAMES)
        if (frameNumber != self.slider1.GetValue()):
            cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_POS_FRAMES, self.slider1.GetValue())
            self.updateVideo()

    def onStop(self, evt):
        self.playTimer.Stop()
        self.playing = False

    def onPlay(self, evt):
        fps = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_FPS)
        if fps!=0:
            self.playTimer.Start(1000/fps)#every X ms
        else:
            print "fallback to 25 fps"
            self.playTimer.Start(1000/25)#assuming 15 fps
        print "playing"
        self.playing = True

    #def onIdle(self, evt):
        #if (self.capture):
            #if (self.ToolBar.GetToolEnabled(self.ID_OPEN) != (not self.playing)):
            #    self.ToolBar.EnableTool(self.ID_OPEN, not self.playing)
            #if (self.slider.Enabled != (not self.playing)):
             #   self.slider.Enabled = not self.playing
            #if (self.ToolBar.GetToolEnabled(self.ID_STOP) != self.playing):
            #    self.ToolBar.EnableTool(self.ID_STOP, self.playing)
            #if (self.ToolBar.GetToolEnabled(self.ID_PLAY) != (not self.playing)):
            #    self.ToolBar.EnableTool(self.ID_PLAY, not self.playing)
        #else:
            #if (not self.ToolBar.GetToolEnabled(self.ID_OPEN)):
            #    self.ToolBar.EnableTool(self.ID_OPEN, True)
            #if (self.slider.Enabled):
            #    self.slider.Enabled = False
            #if (self.ToolBar.GetToolEnabled(self.ID_STOP)):
            #    self.ToolBar.EnableTool(self.ID_STOP, False)
            #if (self.ToolBar.GetToolEnabled(self.ID_PLAY)):
            #    self.ToolBar.EnableTool(self.ID_PLAY, False)

    def onPaint(self, evt):
        if self.bmp:
            wx.BufferedPaintDC(self.videopanel, self.bmp)
        evt.Skip()
        
    def onNextFrame(self, evt):
        frameNumber = cv.GetCaptureProperty(self.capture, cv.CV_CAP_PROP_POS_FRAMES)
        self.slider1.SetValue(frameNumber)
        self.updateVideo()
        evt.Skip()
    
    def updateVideo(self):
        frame = cv.QueryFrame(self.capture)
        if frame:
            cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
            self.bmp.CopyFromBuffer(frame.tostring())
            self.Refresh()
        
if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="amazing window")
    app.MainLoop()

