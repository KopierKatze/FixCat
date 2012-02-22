import wx
from EditCategoryDialog import EditCategoryDialog
from pypsy.Helper import KeyCodeToHumanReadable

class CategoryDialog(wx.Dialog):
    def __init__(self, parent, id, title='Category overview'):
        wx.Dialog.__init__(self, parent, id, title, size=(400,300))
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

        textpnl = wx.Panel(self, -1)

        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lc.InsertColumn(0, 'Kategorie')
        self.lc.InsertColumn(1, 'Shortcut')
        self.lc.SetColumnWidth(0, 140)
        self.lc.SetColumnWidth(1, 100)

        self.FillCategoryTable()

        tablebox.Add(self.lc, 4, wx.EXPAND)

        btnbox.Add(wx.Button(self, 3, 'New'), 0, wx.ALIGN_CENTER)
        self.Bind (wx.EVT_BUTTON, self.OnAdd, id=3)

        btnbox.Add(wx.Button(self, 1, 'Edit'), 0, wx.ALIGN_CENTER)
        self.Bind (wx.EVT_BUTTON, self.OnEdit, id=1)

        btnbox.Add(wx.Button(self, 4, 'Delete'), 0, wx.ALIGN_CENTER)
        self.Bind (wx.EVT_BUTTON, self.OnDelete, id=4)

        btnbox.Add(wx.Button(self, 5, 'Import'), 0, wx.ALIGN_CENTER)
        self.Bind (wx.EVT_BUTTON, self.OnImport, id=5)

        tablebox.Add(btnbox, 1, flag=wx.EXPAND)

        textbox.Add(wx.Button(self, 2, 'Close'), 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER)
        self.Bind (wx.EVT_BUTTON, self.OnClose, id=2)

        mainbox.Add(tablebox, 3, flag=wx.EXPAND)
        mainbox.Add(textbox, 0, flag=wx.EXPAND)
        self.SetSizer(mainbox)

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnImport(self, event):
        confirm_dialog = wx.MessageDialog(self,
          'This procedure overrides all existing categories and categorisations! This cannot be reverted. Do you want to continue?',
          'Import categories', wx.YES_NO)

        if confirm_dialog.ShowModal() == wx.ID_YES:
            file_dialog = wx.FileDialog(self, 'Open existing project', style=wx.FD_OPEN, wildcard='PYPS file (*.pyps)|*.pyps')
            if file_dialog.ShowModal() == wx.ID_OK:
                self.MainFrame.importCategories(file_dialog.GetPath())
                self.FillCategoryTable()

    def OnClose(self, event):
        self.MainFrame.loadCategorisationInToList()
        self.Destroy()

    def OnEdit(self, event):
        index = self.lc.GetFocusedItem()
        cat = self.lc.GetItem(index, 0).GetText()
        short = self.lc.GetItemData(index)

        # in case there are no categories
        if cat == '' or index is None: return

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
        # in case there are no categories
        index = self.lc.GetFocusedItem()
        if self.lc.GetItem(index, 0).GetText() == '' or self.lc.GetItem(index, 0) is None: return
        confirm_dialog = wx.MessageDialog(self,
          'This category and all of its categorisations will be deleted! This cannot be reverted. Do you want to continue?',
          'Delete category', wx.YES_NO)

        if confirm_dialog.ShowModal() != wx.ID_YES:
            return

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
            frame = CategoryFrame(None, -1, 'Category overview')
            frame.Show(True)
            frame.Centre()
            return True

    app = MyApp(0)
    app.MainLoop()
