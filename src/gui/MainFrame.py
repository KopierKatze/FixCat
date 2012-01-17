from CategoryFrame import CategoryFrame
from StringImage import StringImage
from Config import Config

import wx

class MainFrame(wx.Frame):
    def __init__(self, video_str, current_frame, controller):
        wx.Frame.__init__(self, None, title="pyPsy",
            size=(900, 600))

        self.InitUI()
        self.Centre()
        self.Show(True)
        self.dirname=""
        self.controller = controller

        self.video_str = video_str
        self.current_frame = current_frame

        self.reloadTimer = wx.CallLater(1.0/35.0*1000, self.loadImage)
        self.autoreload = False

        self.playing = False

        self.config = Config()

    def InitMenu(self):
        # menubar elements
        statusBar = self.CreateStatusBar()

        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "Oeffnen")
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "About", "Ueber pyPsy")
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save', "Speichern")
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit" , "Schliessen")

        categoryMenu = wx.Menu()
        categoryEdit = categoryMenu.Append(wx.ID_ANY, "Category", "Kategorie editieren")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(categoryMenu, "Category")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuSave)

    def InitUIVideoControlls(self):
        self.videocontrollspanel = wx.Panel(self.mainpanel, wx.ID_ANY)
        self.slider1 = wx.Slider(self.videocontrollspanel, wx.ID_ANY, 0, 0, 1000)
        self.Bind(wx.EVT_SCROLL, self.OnSliderScroll, self.slider1)
        pause = wx.Button(self.videocontrollspanel, wx.ID_ANY, "Pause")
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        play  = wx.Button(self.videocontrollspanel, wx.ID_ANY, "Play")
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play)
        next  = wx.Button(self.videocontrollspanel, wx.ID_ANY, "Next F")
        self.Bind(wx.EVT_BUTTON, self.OnNextFrame, next)
        prev  = wx.Button(self.videocontrollspanel, wx.ID_ANY, "Prev F")
        self.Bind(wx.EVT_BUTTON, self.OnPrevFrame, prev)
        slower  = wx.Button(self.videocontrollspanel, wx.ID_ANY, "90%")
        self.Bind(wx.EVT_BUTTON, self.OnSlower, slower)
        normal  = wx.Button(self.videocontrollspanel, wx.ID_ANY, "100%")
        self.Bind(wx.EVT_BUTTON, self.OnNormal, normal)
        faster  = wx.Button(self.videocontrollspanel, wx.ID_ANY, "110%")
        self.Bind(wx.EVT_BUTTON, self.OnFaster, faster)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(self.slider1, 1)
        hbox2.Add(pause)
        hbox2.Add(play, flag=wx.RIGHT, border=5)
        hbox2.Add(next, flag=wx.LEFT, border=5)
        hbox2.Add(prev)
        hbox2.Add((150, wx.ID_ANY), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        hbox2.Add(slower)
        hbox2.Add(normal)
        hbox2.Add(faster)

        vbox.Add(hbox1, 2, wx.EXPAND | wx.BOTTOM, 10)
        vbox.Add(hbox2, 1, wx.EXPAND)
        self.videocontrollspanel.SetSizer(vbox)
        
    def InitUI(self):
        self.InitMenu()

        # why do we need this? - correct colors in windows 7
        self.mainpanel = wx.Panel(self, wx.ID_ANY)

        # this sizer will locate the widgets
        contentsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainpanel.SetSizer(contentsizer)

        # left side: videoimage and video controlls
        leftsidesizer = wx.BoxSizer(wx.VERTICAL)
        self.videoimage = StringImage(self.mainpanel, wx.ID_ANY)
        leftsidesizer.Add(self.videoimage, 1, flag=wx.EXPAND)
        self.InitUIVideoControlls()
        leftsidesizer.Add(self.videocontrollspanel, flag=wx.EXPAND | wx.TOP, border=5)

        # add left side to main (horizontal) sizer
        contentsizer.Add(leftsidesizer, 1, flag=wx.EXPAND)

        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMousewheel)
        # catching key events is a lot more complicated. they are not propagated to parent classes...
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)

        ##sizer boxes for panels
        #mainbox = wx.BoxSizer(wx.HORIZONTAL)
        
        ## ------------------------------ setting size of main window
        
        #mainbox.Add(sizer,4, flag=wx.EXPAND)
        #mainbox.Add(catbox,2,flag=wx.EXPAND)


        
        ## ------------------------------------------------ new category ctrl  
        #self.categorylist = list(["Tisch", "Monitor", "Maus", "Tastatur"])
         
        #catbox = wx.BoxSizer(wx.VERTICAL)
        #vbox1 = wx.BoxSizer(wx.VERTICAL)
        #vbox2 = wx.BoxSizer(wx.VERTICAL)
        #vbox3 = wx.GridSizer(8,2,0,0)
        #pnl1 = wx.Panel(self.mainpanel, -1)
        #self.lc = wx.ListCtrl(self.mainpanel, -1, style=wx.LC_REPORT)
        #self.lc.InsertColumn(0, 'Kategorie')
        #self.lc.InsertColumn(1, 'Shortcut')
        #self.lc.SetColumnWidth(0, 150)
        #self.lc.SetColumnWidth(1, 100)
        #vbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        #vbox2.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)
        #pnl1.SetSizer(vbox3)
        #vbox3.Add(wx.Button(pnl1, 12, 'naechste Kategorie'), 0, wx.ALIGN_CENTER| wx.TOP, 15)
        
        #catbox.Add(vbox2, 1, wx.EXPAND)
        #catbox.Add(vbox1, 1, wx.EXPAND)

    def loadImage(self):
      image_str = self.video_str.get_obj().raw[:self.video_str_length]
      self.videoimage.SetImage(image_str)
      self.slider1.SetValue(self.current_frame.value)

      if self.autoreload:
	self.reloadTimer.Restart()

    def newProject(self, video_filepath, eyemovement_filepath):
      self.controller.new_project(video_filepath, eyemovement_filepath, True)
      self.video_str_length = self.controller.getVideoStrLength()
      self.videoimage.SetImageSize(self.controller.getVideoWidth(), self.controller.getVideoHeight())
      self.slider1.SetMax(self.controller.getVideoFrameCount())

    def controllerIO(self):
      if self.controller is None: return False
      if not self.controller.ready(): return False
      return True

    # ----- SHORTCUTS ----
    def OnMousewheel(self, event):
      if event.GetWheelRotation() > 0:
	self.OnNextFrame(event)
      else:
	self.OnPrevFrame(event)

    def OnKeyPressed(self, event):
      keyCode = event.GetKeyCode()

      # left arrow key
      if keyCode == self.config.get('keyboard_shortcuts', 'prev_frame'):
	self.OnPrevFrame()
      # right arrow key
      elif keyCode == self.config.get('keyboard_shortcuts', 'next_frame'):
	self.OnNextFrame()
      # up arrow key
      elif keyCode == self.config.get('keyboard_shortcuts', 'faster'):
	self.OnFaster()
      # down arrow key
      elif keyCode == self.config.get('keyboard_shortcuts', 'slower'):
	self.OnSlower()
      elif keyCode == self.config.get('keyboard_shortcuts', 'play/pause'):
	if self.playing:
	  self.OnPause()
	else:
	  self.OnPlay()

    # ---------------- PLAYBACK CONTROLL --------------
    
    def OnPlay(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.playing = True
      self.controller.play()
      self.autoreload = True
      self.loadImage()

    def OnPause(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.playing = False
      self.controller.pause()
      self.autoreload = False
      self.loadImage()

    def OnNextFrame(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.nextFrame()
      self.loadImage()

    def OnPrevFrame(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.prevFrame()
      self.loadImage()

    def OnSlower(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.slowerPlayback()

    def OnNormal(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.normalPlayback()

    def OnFaster(self, event=None):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.fasterPlayback()
      
    def OnSliderScroll(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.seek(self.slider1.GetValue())
      self.loadImage()

      # ---------------- PLAYBACK CONTROLL END ----------
        
    #------------------------------------------- menu items     
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "<slipsum>", "about eyepy", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        #wx.CallAfter(self.controller.pause ()) doesn't work
        self.Close(True)

    def OnOpen(self, e):
        filters = 'AVI files (*.avi)|*.avi|All files (*.*)|*.*'
        dlg = wx.FileDialog(None, message = 'Select AVI files....', wildcard=filters, style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()

    def OnEditCategory(self, e):
        CategoryFrame(self, wx.ID_ANY, self.controller).Show()

        
if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="eyepsy window")
    app.MainLoop()

