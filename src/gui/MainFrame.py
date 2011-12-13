import wx

from OpenCVImage import OpenCVImage

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="pyPsy",
            size=(900, 600))

        self.InitUI()
        self.Centre()
        self.Show(True)
        self.dirname=""

    def InitUI(self):

        # menubar elements
        statusBar = self.CreateStatusBar()

        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "open")
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "&About", "Information About")
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit" , "Terminate")

        codecMenu = wx.Menu()
        codecMenu.Append(wx.ID_PREFERENCES, "&Codecs", "Set codec")

        cursorMenu = wx.Menu()
        menuSetImage = cursorMenu.Append(wx.ID_PREFERENCES, "&Cursor", "Change Cursor Image")

        categoryMenu = wx.Menu()
        categoryAdd = categoryMenu.Append(wx.ID_PREFERENCES, "&Category", "Add A Category")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(codecMenu, "C&odecs")
        menuBar.Append(cursorMenu, "&Cursor")
        menuBar.Append(categoryMenu, "&Category")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuSave)
        #self.Bind(wx.EVT_MENU, self.OnAddCategory, categoryAdd)
        #self.Bind(wx.EVT_MENU, self., )

        #sizer boxes for panels
        mainbox = wx.BoxSizer(wx.HORIZONTAL)

        # ------------------------------------------ video ctrl
        self.videopanel = OpenCVImage(self, wx.ID_ANY)
        vbtnpanel = wx.Panel(self, -1)
        self.slider1 = wx.Slider(vbtnpanel, -1, 0, 0, 1000)
        pause = wx.Button(vbtnpanel, -1, "Pause")
        play  = wx.Button(vbtnpanel, -1, "Play")
        next  = wx.Button(vbtnpanel, -1, "Next F")
        prev  = wx.Button(vbtnpanel, -1, "Prev F")

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
        vbtnpanel.SetSizer(vbox)
        # ------------------------------------------------ new category ctrl  
        self.categorylist = list(["Tisch", "Monitor", "Maus", "Tastatur"])
         
        catbox = wx.BoxSizer(wx.VERTICAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.GridSizer(8,2,0,0)
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Index')
        self.lc.InsertColumn(1, 'Kategorie')
        self.lc.InsertColumn(1, 'Shortcut')
        self.lc.SetColumnWidth(0, 40)
        self.lc.SetColumnWidth(1, 150)
        self.lc.SetColumnWidth(1, 100)
        vbox1.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        vbox2.Add(self.lc, 1, wx.EXPAND | wx.ALL, 3)
        self.tcindex = wx.TextCtrl(pnl1, -1)
        self.tccat = wx.TextCtrl(pnl1, -1)
        self.tcshort = wx.TextCtrl(pnl1, -1)
        vbox3.AddMany([ (wx.StaticText(pnl1, -1, 'Index'),0, wx.ALIGN_CENTER),
                       (self.tcindex, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                       (wx.StaticText(pnl1, -1, 'Kategorie'),0, wx.ALIGN_CENTER_HORIZONTAL),
                       (self.tccat,0),
                       (wx.StaticText(pnl1, -1, 'Shortcut'),0, wx.ALIGN_CENTER_HORIZONTAL),
                       (self.tcshort,0)])
        pnl1.SetSizer(vbox3)
        vbox3.Add(wx.Button(pnl1, 10, 'Hinzufuegen'),   0, wx.ALIGN_CENTER| wx.TOP, 45)
        vbox3.Add(wx.Button(pnl1, 11, 'Entfernen'), 0, wx.ALIGN_CENTER|wx.TOP, 15)
        vbox3.Add(wx.Button(pnl1, 12, 'Liste leeren'), 0, wx.ALIGN_CENTER| wx.TOP, 15)
        
        self.Bind (wx.EVT_BUTTON, self.OnAdd, id=10)
        self.Bind (wx.EVT_BUTTON, self.OnRemove, id=11)
        self.Bind (wx.EVT_BUTTON, self.OnClear, id=12)
        catbox.Add(vbox2, 1, wx.EXPAND)
        catbox.Add(vbox1, 1, wx.EXPAND)
        #self.SetSizer(catbox)
        
        # ------------------------------ setting size of main window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        sizer.Add(vbtnpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)

        mainbox.Add(sizer,4, flag=wx.EXPAND)
        mainbox.Add(catbox,2,flag=wx.EXPAND)
        #mainbox.Add(pnl1, flag=wx.EXPAND) 
        self.SetSizer(mainbox)    
        
    #------------------------------------------- menu items     
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

    def OnAddCategory(self, e):
        CategoryEditor().Show()

    def setImageAndTime(self, image, time):
      wx.CallAfter(self.videopanel.SetImage, (image))

    # -------------------- category editor buttons
    def load_buttonClick(self, event):
        """load the name list into the bistbox"""
        self.elistbox.SetStrings(self.categorylist)

    def clear_buttonClick(self, event):
        """clear all items from the elistbox"""
        self.elistbox.SetStrings([])
        self.label.SetLabel("")

    def sort_buttonClick(self, event):
        """sort the items in the elistbox"""
        # GetStrings() puts the elistbox items into a list
        categorylist = self.elistbox.GetStrings()
        categorylist.sort()
        # SetStrings() clears and reloads the elistbox
        self.elistbox.SetStrings(categorylist)

    def listctrlClick(self, event):
        """display the selected listctrl item of the elistbox"""
        for n in range(self.actual_listctrl.GetItemCount()):
            state = wx.LIST_STATE_SELECTED
            if self.actual_listctrl.GetItemState(n, state):
                selected_item = self.actual_listctrl.GetItemText(n)
        s = "You selected " + selected_item
        self.label.SetLabel(s)
 
        pass
    # -------------------- category editor buttons 
    def OnAdd(self, event):
       if not self.tcindex.GetValue() or not self.tccat.GetValue() or not self.tcshort.GetValue():
           return
       num_items = self.lc.GetItemCount()
       self.lc.InsertStringItem(num_items, self.tcindex.GetValue())
       self.lc.SetStringItem(num_items, 1, self.tccat.GetValue())
       self.tcindex.Clear()
       self.tccat.Clear()
       self.tcshort.Clear()

    def OnRemove(self, event):
       index = self.lc.GetFocusedItem()
       self.lc.DeleteItem(index)

    def OnClear(self, event):
       self.lc.DeleteAllItems()
        
if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="eyepsy window")
    app.MainLoop()

