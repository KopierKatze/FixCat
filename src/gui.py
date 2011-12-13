import wx
import os
import cv
import wx.gizmos

class Example(wx.Frame): 
    def __init__(self, parent, title):   
        super(Example, self).__init__(parent, title=title, 
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
        self.videopanel = wx.Panel(self, -1)
        self.videopanel.SetBackgroundColour(wx.BLACK)
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
        self.catpanel = wx.Panel(self, wx.ID_ANY)
        self.categorylist = list(["Tisch", "Monitor", "Maus", "Tastatur"])
         
        self.elistbox = wx.gizmos.EditableListBox(self.catpanel, wx.ID_ANY,
        label="Category Editor")
        # get the actual control portion of the EditableListBox
        self.actual_listctrl = self.elistbox.GetListCtrl()
        # binds to any newly focused/selected item
        self.actual_listctrl.Bind(wx.EVT_LIST_ITEM_FOCUSED,
        self.listctrlClick)
         
        # create action widgets
        load_button = wx.Button(self.catpanel, wx.ID_ANY, "Load Example")
        clear_button = wx.Button(self.catpanel, wx.ID_ANY, "Clear Categories")
        sort_button = wx.Button(self.catpanel, wx.ID_ANY, "Sort Categories")
        # bind mouse click event to an action
        load_button.Bind(wx.EVT_BUTTON, self.load_buttonClick)
        clear_button.Bind(wx.EVT_BUTTON, self.clear_buttonClick)
        sort_button.Bind(wx.EVT_BUTTON, self.sort_buttonClick)
        # create an output widget
        self.label = wx.StaticText(self.catpanel, wx.ID_ANY, "")
         
        catsizer = wx.GridBagSizer(vgap=5, hgap=5)
        # pos=(row, column) span=(rowspan, columnspan)
        # wx.ALL puts the specified border on all sides
        # listbox spans 6 rows and 2 columns
        catsizer.Add(self.elistbox, pos=(1, 0), span=(6, 2),
        flag=wx.ALL|wx.EXPAND, border=5)
        catsizer.Add(clear_button, pos=(7, 1), flag=wx.ALL, border=5)
        catsizer.Add(sort_button, pos=(7, 0), flag=wx.ALL, border=5)
        catsizer.Add(self.label, pos=(8, 0), flag=wx.ALL, border=5)
        catsizer.Add(load_button, pos=(9, 0), flag=wx.ALL, border=5)
        # set the sizer and fit all its widgets
        self.catpanel.SetSizerAndFit(catsizer)
         
        # size the frame so all its widgets fit inside
        #self.Fit()
        
        
        
        
        # ------------------------------ setting size of main window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.videopanel, 1, flag=wx.EXPAND)
        sizer.Add(vbtnpanel, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, border=10)
        
        mainbox.Add(sizer,4, flag=wx.EXPAND)
        mainbox.Add(self.catpanel,flag=wx.EXPAND)     
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
            
    def OnAddCategory(self, e):
        CategoryEditor().Show()

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
        
if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="eyepsy window")
    app.MainLoop()

