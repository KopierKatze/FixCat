import wx

class EditCategoryDialog(wx.Dialog):
  def __init__(self, parent, category_name=None, category_shortcut=None):
    wx.Dialog.__init__(self, parent, wx.ID_ANY)
    
    self.category_name = category_name
    self.category_shortcut = category_shortcut
    self.parent = parent
    self.controller = parent.controller
    sizer = wx.BoxSizer(wx.VERTICAL)

    label = wx.StaticText(self, -1, "Kategorie editieren")   
    sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    box = wx.BoxSizer(wx.HORIZONTAL)
    
    label = wx.StaticText(self, -1, "Kategorie:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    self.new_category = wx.TextCtrl(self, -1, self.category_name, size=(80,-1))   
    box.Add(self.new_category, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self, -1, "Shortcut:")
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    
    self.shortcut = wx.Button(self, -1, "Eingabe", size=(80,-1))
    box.Add(self.shortcut, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    
   
    
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
    
    self.Bind(wx.EVT_BUTTON, self.OnSave, save_btn)
    self.Bind(wx.EVT_BUTTON, self.OnClose, cancel_btn)
    
  def OnSave(self, event):
    self.new_shortcut = 69
    self.category_shortcut = 68
    self.new_category = "neu"
    self.controller.editCategory(self.category_shortcut, self.new_shortcut, self.new_category)  #new_category.GetText()
    self.Destroy()
      
  def OnClose(self, event):
      self.Close()