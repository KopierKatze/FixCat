import wx

class OpenDialog(wx.Dialog):
  def __init__(self, parent):
    wx.Dialog.__init__(self, parent, wx.ID_ANY, "Projekt laden oder neu beginnen")

    self.parent = parent

    self.new_save = 'NEW'
    self.video_filepath = None
    self.eyedata_filepath = None
    self.saved_filepath = None

    self.InitUI()

  def InitUI(self):
    mainpanel = wx.Panel(self, wx.ID_ANY)

    mainpanel_sizer = wx.BoxSizer(wx.VERTICAL)
    mainpanel.SetSizer(mainpanel_sizer)

    self.new_radio = wx.RadioButton(mainpanel, wx.ID_ANY, "Neues Projekt beginnen")
    mainpanel_sizer.Add(self.new_radio)
    new_project_video_box = wx.BoxSizer(wx.HORIZONTAL)
    self.video_text = wx.StaticText(mainpanel, wx.ID_ANY, "Video waehlen...")
    new_project_video_box.Add(self.video_text)
    self.video_button = wx.Button(mainpanel, wx.ID_ANY, "Durchsuchen")
    new_project_video_box.Add(self.video_button)
    mainpanel_sizer.Add(new_project_video_box)

    new_project_eyedate_box = wx.BoxSizer(wx.HORIZONTAL)
    self.eyedata_text = wx.StaticText(mainpanel, wx.ID_ANY, "EDF-Datei waehlen...")
    new_project_eyedate_box.Add(self.eyedata_text)
    self.eyedata_button = wx.Button(mainpanel, wx.ID_ANY, "Durchsuchen")
    new_project_eyedate_box.Add(self.eyedata_button)
    mainpanel_sizer.Add(new_project_eyedate_box)


    self.saved_radio = wx.RadioButton(mainpanel, wx.ID_ANY, "Gespeichertes Projekt laden")
    mainpanel_sizer.Add(self.saved_radio)
    saved_project_box = wx.BoxSizer(wx.HORIZONTAL)
    self.saved_text = wx.StaticText(mainpanel, wx.ID_ANY, "Gespeichertes Projekt waehlen...")
    saved_project_box.Add(self.saved_text)
    self.saved_button = wx.Button(mainpanel, wx.ID_ANY, "Durchsuchen")
    saved_project_box.Add(self.saved_button)
    mainpanel_sizer.Add(saved_project_box)

    ok = wx.Button(mainpanel, wx.ID_ANY, "Okay")
    mainpanel_sizer.Add(ok)

    self.Bind(wx.EVT_RADIOBUTTON, self.OnNewSelection, self.new_radio)
    self.Bind(wx.EVT_RADIOBUTTON, self.OnSavedSelection, self.saved_radio)
    self.Bind(wx.EVT_BUTTON, self.OnSelectVideo, self.video_button)
    self.Bind(wx.EVT_BUTTON, self.OnSelectEyedata, self.eyedata_button)
    self.Bind(wx.EVT_BUTTON, self.OnSelectSaved, self.saved_button)

    self.Bind(wx.EVT_BUTTON, self.OnOK, ok)

    self.OnNewSelection()

  def OnNewSelection(self, event=None):
    self.saved_button.Enable(False)
    self.video_button.Enable(True)
    self.eyedata_button.Enable(True)
    self.saved_text.SetForegroundColour((125,125,125))
    self.video_text.SetForegroundColour((0,0,0))
    self.eyedata_text.SetForegroundColour((0,0,0))

    self.new_save = 'NEW'

  def OnSavedSelection(self, event=None):
    self.saved_button.Enable(True)
    self.video_button.Enable(False)
    self.eyedata_button.Enable(False)
    self.saved_text.SetForegroundColour((0,0,0))
    self.video_text.SetForegroundColour((125,125,125))
    self.eyedata_text.SetForegroundColour((125,125,125))

    self.new_save = 'SAVE'

  def _open_file(self, title, wildcard):
    file_dialog = wx.FileDialog(self, title, style=wx.FD_OPEN, wildcard=wildcard)
    if file_dialog.ShowModal() == wx.ID_OK:
      return file_dialog.GetPath()
    else:
      return None

  def OnSelectVideo(self, event):
    q = self._open_file('Video waehlen', 'AVI-Datei (*.avi)|*.avi')
    if not q is None:
      self.video_text.SetLabel(q)
      self.video_filepath = q

  def OnSelectEyedata(self, event):
    q = self._open_file('Augenbewegungsdaten waehlen', 'ASC-Datei (*.asc)|*.asc')
    if not q is None:
      self.eyedata_text.SetLabel(q)
      self.eyedata_filepath = q

  def OnSelectSaved(self, event):
    q = self._open_file('Gespeichertes Projekt waehlen', 'PYPS-Datei (*.pyps)|*.pyps')
    if not q is None:
      self.saved_text.SetLabel(q)
      self.saved_filepath = q

  def OnOK(self, event):
    if self.new_save == 'NEW':
      try:
	self.parent.newProject(self.video_filepath, self.eyedata_filepath, False)
      except:
	pass
        # error show
      else:
	self.Destroy()
