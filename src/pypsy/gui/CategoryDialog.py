import wx
from EditCategoryDialog import EditCategoryDialog
from pypsy.Helper import KeyCodeToHumanReadable

class CategoryDialog(wx.Dialog):
    def __init__(self, parent, id, title='Kategorie Uebersicht'):
        self.infotext = "In diesem Fenster koennen die Kategorien editiert werden. \nKategorie in der Tabelle aswaehlen und auf Editieren klicken. \nIn dem neuen Dialog koennen dann die Parameter der Kategorie \n- Buchstabe und Name - geaendert werden.\n Mit Hilfe des Buchstabes wird Tastenkombination fuer die Kategorie festgelegt."
        wx.Dialog.__init__(self, parent, id, title, size=(600,600))
        self.Center()
        # get dict from controller
        self.MainFrame = parent

        self.InitUI()

        self.MainFrame.DeactivateMouseAndKeyCatching()

    def Destroy(self):
        self.MainFrame.ActivateMouseAndKeyCatching()
        wx.Dialog.Destroy(self)

    def InitUI(self):
      mainbox  = wx.BoxSizer(wx.VERTICAL)
      tablebox = wx.BoxSizer(wx.HORIZONTAL)
      btnbox = wx.BoxSizer(wx.VERTICAL)
      textbox = wx.BoxSizer(wx.VERTICAL)

      textpnl = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)

      self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
      self.lc.InsertColumn(0, 'Kategorie')
      self.lc.InsertColumn(1, 'Shortcut')
      self.lc.SetColumnWidth(0, 100)
      self.lc.SetColumnWidth(1, 80)

      self.FillCategoryTable()

      tablebox.Add(self.lc, 4, wx.EXPAND)

      btnbox.Add(wx.Button(self, 1, 'Bearbeiten'), 0, wx.ALIGN_CENTER)
      self.Bind (wx.EVT_BUTTON, self.OnEdit, id=1)

      btnbox.Add(wx.Button(self, 3, 'Neu'), 0, wx.ALIGN_CENTER)
      self.Bind (wx.EVT_BUTTON, self.OnAdd, id=3)

      btnbox.Add(wx.Button(self, 4, 'Loeschen'), 0, wx.ALIGN_CENTER)
      self.Bind (wx.EVT_BUTTON, self.OnDelete, id=4)

      btnbox.Add(wx.Button(self, 5, 'Import'), 0, wx.ALIGN_CENTER)
      self.Bind (wx.EVT_BUTTON, self.OnImport, id=5)

      tablebox.Add(btnbox, 1, flag=wx.EXPAND)

      info = wx.StaticText(textpnl, -1, self.infotext,(50,10), style=wx.ALIGN_CENTER)
      textbox.Add(textpnl, 3, wx.EXPAND | wx.ALL)
      textbox.Add(wx.Button(self, 2, 'Schliessen'), 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER)
      self.Bind (wx.EVT_BUTTON, self.OnClose, id=2)

      mainbox.Add(tablebox, 3, flag=wx.EXPAND)
      mainbox.Add(textbox, 1, flag=wx.EXPAND)
      self.SetSizer(mainbox)

      self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnImport(self, event):
      confirm_dialog = wx.MessageDialog(self, 
	'Dieser Vorgang ueberschreibt alle bisher eingegebenen Kategorien und Kategoriesierungen! Wirklich fortfahren?',
	'Kategorien importieren', wx.OK | wx.CANCEL)
      
      if confirm_dialog.ShowModal() == wx.ID_OK:
	file_dialog = wx.FileDialog(self, 'Gespeichertes Projekt waehlen', style=wx.FD_OPEN, wildcard='PYPS-Datei (*.pyps)|*.pyps')
	if file_dialog.ShowModal() == wx.ID_OK:
	  self.MainFrame.importCategories(file_dialog.GetPath())
      confirm_dialog.Destroy()
      
    def OnClose(self, event):
      self.MainFrame.loadCategorisationInToList()
      self.Destroy()

    def OnEdit(self, event):
      index = self.lc.GetFocusedItem()
      cat = self.lc.GetItem(index, 0).GetText()
      short = self.lc.GetItemData(index)

      edit_dlg = EditCategoryDialog(self, self.MainFrame.editCategory, cat, short)
      edit_dlg.ShowModal()
      # refreshing list 
      self.lc.DeleteAllItems()
      self.FillCategoryTable()

    def OnAdd(self, event):
      edit_dlg = EditCategoryDialog(self, self.MainFrame.editCategory)
      edit_dlg.ShowModal()
      # refreshing list
      self.lc.DeleteAllItems()
      self.FillCategoryTable()

    def OnDelete(self, event):
      index = self.lc.GetFocusedItem()
      short = self.lc.GetItemData(index)

      self.MainFrame.editCategory(short, None, None)
      # refreshing list
      self.lc.DeleteAllItems()
      self.FillCategoryTable()

    def FillCategoryTable(self):
      for shortcut, category in self.MainFrame.getCategories().iteritems():
	  num_items = self.lc.GetItemCount()
	  self.lc.InsertStringItem(num_items, category)
	  self.lc.SetStringItem(num_items, 1, KeyCodeToHumanReadable(shortcut))
	  self.lc.SetItemData(num_items, shortcut)

if __name__ == "__main__":
    class MyApp(wx.App):
        def OnInit(self):
           frame = CategoryFrame(None, -1, 'Kategorie Uebersicht')
           frame.Show(True)
           frame.Centre()
           return True

    app = MyApp(0)
    app.MainLoop()
