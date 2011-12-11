import wx

class Example(wx.Frame): 
    def __init__(self, parent, title):    
        super(Example, self).__init__(parent, title=title, 
            size=(900, 600))

        self.InitUI()
        self.Centre()
        self.Show()     
        self.dirname=""
        
    def InitUI(self):
    
        # menubar elements
        self.CreateStatusBar()

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
        
        pnl1 = wx.Panel(self, -1)
        pnl1.SetBackgroundColour(wx.BLACK)
        pnl2 = wx.Panel(self, -1) 
        slider1 = wx.Slider(pnl2, -1, 0, 0, 1000)
        pause = wx.Button(pnl2, -1, "Pause")
        play  = wx.Button(pnl2, -1, "Play")
        next  = wx.Button(pnl2, -1, "Next")
        prev  = wx.Button(pnl2, -1, "Prev")

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(slider1, 1)
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
        self.lc.SetColumnWidth(0, 140)
        self.lc.SetColumnWidth(1, 90)
        
        # add table to category box
        categorybox.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)
        
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pnl1, 1, flag=wx.EXPAND)
        sizer.Add(pnl2, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        mainbox.Add(sizer,3, flag=wx.EXPAND)
        mainbox.Add(categorybox,1, flag=wx.EXPAND)      
        self.SetSizer(mainbox)    
        
        
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "The path of the righteous man is beset on all sides by the iniquities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of darkness, for he is truly his brother's keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who would attempt to poison and destroy My brothers. And you will know My name is the Lord when I lay My vengeance upon thee.", "about this program", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        
    def OnExit(self, e):
        self.Close(True)
        
    def OnOpen(self, e):
        dlg = wx.FileDialog(self, "choose", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filnemane), "r")
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="amazing window")
    app.MainLoop()

