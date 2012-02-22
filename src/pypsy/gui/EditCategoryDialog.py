import wx

from pypsy.Helper import KeyCodeToHumanReadable
from pypsy.CategoryContainer import CategoryContainerError

class EditCategoryDialog(wx.Dialog):
    def __init__(self, parent, editCategoryFunction, category_name='', category_shortcut=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY)

        self.category_name = category_name
        self.old_shortcut = category_shortcut
        self.editCategoryFunction = editCategoryFunction
        self.new_shortcut = category_shortcut

        self.InitUI()

    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Edit categories")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Category:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.category_name_text = wx.TextCtrl(self, -1, self.category_name, size=(80,-1))
        box.Add(self.category_name_text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Shortcut:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.shortcut_button = wx.Button(self, -1, KeyCodeToHumanReadable(self.old_shortcut), size=(80,-1))
        self.shortcut_button.SetToolTip(wx.ToolTip('Click this button to enter a new shortcut for this category'))
        box.Add(self.shortcut_button, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        save_btn = wx.Button(self, wx.ID_OK)
        save_btn.SetDefault()
        btnsizer.AddButton(save_btn)
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(cancel_btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

        self.Bind(wx.EVT_BUTTON, self.OnNewShortcutSelectionFirstPhase, self.shortcut_button)

        self.Bind(wx.EVT_BUTTON, self.OnSave, save_btn)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel_btn)

    def OnNewShortcutSelectionFirstPhase(self, event):
        self.new_shortcut = None
        self.shortcut_button.SetLabel('...')
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, self.OnNewShortcutSelectionSecondPhase)

    def OnNewShortcutSelectionSecondPhase(self, event):
        KeyCode = event.GetKeyCode()
        self.new_shortcut = KeyCode
        self.shortcut_button.SetLabel(KeyCodeToHumanReadable(KeyCode))
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, None)

    def OnSave(self, event):
        self.category_name = self.category_name_text.GetValue()
        try:
            self.editCategoryFunction(self.old_shortcut, self.new_shortcut, self.category_name)
        except CategoryContainerError, e:
            error_dlg = wx.MessageDialog(self, 'Error while saving the category: %s' % e, 'Error', wx.OK | wx.ICON_ERROR)
            error_dlg.ShowModal()
        else:
            self.Destroy()

    def OnCancel(self, event):
        self.Destroy()

