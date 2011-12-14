import wx
from CategoryFrame import CategoryFrame
from OpenCVImage import OpenCVImage

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="pyPsy",
            size=(900, 600))

        self.InitUI()
        self.Centre()
        self.Show(True)
        self.dirname=""
        self.controller = None

    def InitUI(self):

        # menubar elements
        statusBar = self.CreateStatusBar()

        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "Oeffnen")
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "About", "Ueber pyPsy")
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save', "Speichern")
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit" , "Schliessen")

        codecMenu = wx.Menu()
        setCodec = codecMenu.Append(wx.ID_PREFERENCES, "Codecs", "Codec aendern")

        cursorMenu = wx.Menu()
        menuSetImage = cursorMenu.Append(wx.ID_PREFERENCES, "Cursor", "Cursor aendern")

        categoryMenu = wx.Menu()
        categoryEdit = categoryMenu.Append(wx.ID_PREFERENCES, "Category", "Kategorie editieren")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(codecMenu, "Codecs")
        menuBar.Append(cursorMenu, "Cursor")
        menuBar.Append(categoryMenu, "Category")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuSave)
        self.Bind(wx.EVT_MENU, self.OnEditCategory, categoryEdit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuSetImage)
        self.Bind(wx.EVT_MENU, self.OnAbout, setCodec)

        #sizer boxes for panels
        mainbox = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------------------------------ video ctrl
        self.videopanel = OpenCVImage(self, wx.ID_ANY)
        vbtnpanel = wx.Panel(self, -1)
        self.slider1 = wx.Slider(vbtnpanel, -1, 0, 0, 1000)
        self.Bind(wx.EVT_SCROLL, self.OnSliderScroll, self.slider1)
        pause = wx.Button(vbtnpanel, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        play  = wx.Button(vbtnpanel, -1, "Play")
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play)
        next  = wx.Button(vbtnpanel, -1, "Next F")
        self.Bind(wx.EVT_BUTTON, self.OnNextFrame, next)
        prev  = wx.Button(vbtnpanel, -1, "Prev F")
        self.Bind(wx.EVT_BUTTON, self.OnPrevFrame, prev)
        slower  = wx.Button(vbtnpanel, -1, "90%")
        self.Bind(wx.EVT_BUTTON, self.OnSlower, slower)
        normal  = wx.Button(vbtnpanel, -1, "100%")
        self.Bind(wx.EVT_BUTTON, self.OnNormal, normal)
        faster  = wx.Button(vbtnpanel, -1, "110%")
        self.Bind(wx.EVT_BUTTON, self.OnFaster, faster)


        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(self.slider1, 1)
        hbox2.Add(pause)
        hbox2.Add(play, flag=wx.RIGHT, border=5)
        hbox2.Add(next, flag=wx.LEFT, border=5)
        hbox2.Add(prev)
        hbox2.Add((150, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        hbox2.Add(slower)
        hbox2.Add(normal)
        hbox2.Add(faster)

        vbox.Add(hbox1, 2, wx.EXPAND | wx.BOTTOM, 10)
        vbox.Add(hbox2, 1, wx.EXPAND)
        vbtnpanel.SetSizer(vbox)
        # ------------------------------------------------ new category ctrl  
        self.categorylist = list(["Tisch", "Monitor", "Maus", "Tastatur"])
         
        catbox = wx.BoxSizer(wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.GridSizer(8,2,0,0)
        pnl1 = wx.Panel(self, -1)
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Kategorie')
        self.lc.InsertColumn(1, 'Shortcut')
        self.lc.SetColumnWidth(0, 150)
        self.lc.SetColumnWidth(1, 100)
        vbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        vbox2.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)
        pnl1.SetSizer(vbox3)
        vbox3.Add(wx.Button(pnl1, 12, 'naechste Kategorie'), 0, wx.ALIGN_CENTER| wx.TOP, 15)
        
        #self.Bind (wx.EVT_BUTTON, self.OnAdd, id=12)
        
        catbox.Add(vbox2, 1, wx.EXPAND)
        catbox.Add(vbox1, 1, wx.EXPAND)
        
        # ------------------------------ setting size of main window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        sizer.Add(vbtnpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)

        mainbox.Add(sizer,4, flag=wx.EXPAND)
        mainbox.Add(catbox,2,flag=wx.EXPAND)
        self.SetSizer(mainbox)

    def newVideo(self, duration):
      wx.CallAfter(self.slider1.SetMax, (duration))

    def setImageAndTime(self, image, time):
      wx.CallAfter(self.videopanel.SetImage, (image))
      wx.CallAfter(self.slider1.SetValue, (time))

    def controllerIO(self):
      if self.controller is None: pass
      if not self.controller.ready(): pass
      return True

    # ---------------- PLAYBACK CONTROLL --------------
    
    def OnPlay(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.play()

    def OnPause(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.pause()

    def OnNextFrame(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.nextFrame()

    def OnPrevFrame(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.prevFrame()

    def OnSlower(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.slowerPlayback()

    def OnNormal(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.normalPlayback()

    def OnFaster(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.fasterPlayback()
      
    def OnSliderScroll(self, event):
      """ check whether contoller is ready"""
      if not self.controllerIO(): return event

      self.controller.seek(self.slider1.GetValue())

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

