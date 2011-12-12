import wx
import os
import cv
class Example(wx.Frame): 
    def __init__(self, parent, title):    
        super(Example, self).__init__(parent, title=title, 
            size=(800, 600))

        self.InitUI()
        self.Centre()
        self.Show(True)     
        self.dirname=""
        
    def InitUI(self):
        
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
        self.videopanel.SetBackgroundColour(wx.BLACK)
        pnl2 = wx.Panel(self, -1) 
        self.slider1 = wx.Slider(pnl2, -1, 0, 0, 1000)
        pause = wx.Button(pnl2, -1, "Pause")
        play  = wx.Button(pnl2, -1, "Play")
        next  = wx.Button(pnl2, -1, "Next")
        prev  = wx.Button(pnl2, -1, "Prev")
        
        #self.Bind(wx.EVT_BUTTON, self.onPlay, play)
        
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
        self.lc.InsertLine()
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
            
        
if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="eyepsy window")
    app.MainLoop()

