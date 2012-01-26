import wx
from EditCategoryDialog import EditCategoryDialog
    
class CategoryDialog(wx.Dialog):
    def __init__(self, parent, id, controller, title='Kategorie Uebersicht'):
        infotext = "In diesem Fenster koennen die Kategorien editiert werden. \nKategorie in der Tabelle aswaehlen und auf Editieren klicken. \nIn dem neuen Dialog koennen dann die Parameter der Kategorie \n- Buchstabe und Name - geaendert werden.\n Mit Hilfe des Buchstabes wird Tastenkombination fuer die Kategorie festgelegt."
        wx.Dialog.__init__(self, parent, id, title, size=(600,600))
        self.Center()
        # get dict from controler
        categories = parent.controller.getCategories()
        self.category = None
        self.shortcut = None  
        self.parent = parent
        mainbox  = wx.BoxSizer(wx.VERTICAL)
        tablebox = wx.BoxSizer(wx.HORIZONTAL)
        textbox = wx.BoxSizer(wx.VERTICAL)
        
        textpnl = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
        
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Kategorie')
        self.lc.InsertColumn(1, 'Shortcut')
        self.lc.SetColumnWidth(0, 100)
        self.lc.SetColumnWidth(1, 80)
        # ---------------------------------- fill category table
        num_items = self.lc.GetItemCount()
        for shortcut, category in categories.iteritems(): #.iteritems():
            num_items = self.lc.GetItemCount()
            self.category = category
            print self.category
            self.shortcut = str(shortcut)
            print self.shortcut
            self.lc.InsertStringItem(num_items, self.category)
            self.lc.SetStringItem(num_items, 1, self.shortcut)
        # -----------------------------------	
        
        tablebox.Add(self.lc, 4, wx.EXPAND)
        tablebox.Add(wx.Button(self, 1, 'Bearbeiten'), 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER)
        self.Bind (wx.EVT_BUTTON, self.OnEdit, id=1)
        
        info = wx.StaticText(textpnl, -1, infotext,(50,10), style=wx.ALIGN_CENTER)
        textbox.Add(textpnl, 3, wx.EXPAND | wx.ALL)
        textbox.Add(wx.Button(self, 2, 'Schliessen'), 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER)
        #self.Bind (wx.EVT_BUTTON, self.OnClose, id=2)
        self.Bind (wx.EVT_BUTTON, self.OnClose, id=2)
        
        mainbox.Add(tablebox, 3, flag=wx.EXPAND)
        mainbox.Add(textbox, 1, flag=wx.EXPAND)
        self.SetSizer(mainbox)
        
    def OnClose(self, event):
       self.Close()
       
    def OnEdit(self, event):
      index = self.lc.GetFocusedItem()
      cat = self.lc.GetItem(index, 0).GetText()
      short = self.lc.GetItem(index, 1).GetText()
      print cat
      edit_dlg = EditCategoryDialog(self, cat, short)
      edit_dlg.ShowModal()
	
    #def OnCloseWindow(self, event):
         #self.Destroy()

if __name__ == "__main__":       
    class MyApp(wx.App):
        def OnInit(self):
           frame = CategoryFrame(None, -1, 'Kategorie Uebersicht')
           frame.Show(True)
           frame.Centre()
           return True
       
    app = MyApp(0)
    app.MainLoop()
