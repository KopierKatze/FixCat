import wx
from pypsy.VideoReader import ReaderError
from pypsy.EyeMovement import EyeMovementError

class OpenDialog(wx.Dialog):
  def __init__(self, parent):
    wx.Dialog.__init__(self, parent, wx.ID_ANY, "Projekt laden oder neu beginnen")

    self.parent = parent

    self.new_save = 'NEW'
    self.video_filepath = None
    self.eyedata_filepath = None
    self.left_eye_categorisation = True # None -> mean eye, True -> left eye, False -> right eye
    self.frame_categorisation = True # False -> fixation categorisation

    self.saved_filepath = None

    self.InitUI()

  def InitUI(self):
    mainpanel = wx.Panel(self, wx.ID_ANY)

    mainpanel_sizer = wx.BoxSizer(wx.VERTICAL)
    mainpanel.SetSizer(mainpanel_sizer)

    self.new_radio = wx.RadioButton(mainpanel, wx.ID_ANY, "Neues Projekt beginnen")
    mainpanel_sizer.Add(self.new_radio, 0)
    new_project_video_box = wx.BoxSizer(wx.HORIZONTAL)
    self.video_text = wx.StaticText(mainpanel, wx.ID_ANY, "Video waehlen...")
    new_project_video_box.Add(self.video_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
    self.video_button = wx.Button(mainpanel, wx.ID_ANY, "Durchsuchen")
    new_project_video_box.Add(self.video_button, 0, wx.ALIGN_RIGHT)
    mainpanel_sizer.Add(new_project_video_box, 0, wx.EXPAND)

    new_project_eyedate_box = wx.BoxSizer(wx.HORIZONTAL)
    self.eyedata_text = wx.StaticText(mainpanel, wx.ID_ANY, "EDF-Datei waehlen...")
    new_project_eyedate_box.Add(self.eyedata_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
    self.eyedata_button = wx.Button(mainpanel, wx.ID_ANY, "Durchsuchen")
    new_project_eyedate_box.Add(self.eyedata_button, 0)
    mainpanel_sizer.Add(new_project_eyedate_box, 0, wx.EXPAND)

    self.eye_rb = wx.RadioBox(mainpanel, wx.ID_ANY, "Zu kategorisierendes Auge", choices=['Links', 'Rechts', 'Gemitteltes'])
    mainpanel_sizer.Add(self.eye_rb, 0, wx.LEFT, 25)

    self.frames_rb = wx.RadioBox(mainpanel, wx.ID_ANY, "Frames oder Fixationen kategorisieren", choices=['Frame', 'Fixationen'])
    mainpanel_sizer.Add(self.frames_rb, 0, wx.LEFT, 25)

    self.saved_radio = wx.RadioButton(mainpanel, wx.ID_ANY, "Gespeichertes Projekt laden")
    mainpanel_sizer.Add(self.saved_radio, 0)
    saved_project_box = wx.BoxSizer(wx.HORIZONTAL)
    self.saved_text = wx.StaticText(mainpanel, wx.ID_ANY, "Gespeichertes Projekt waehlen...")
    saved_project_box.Add(self.saved_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
    self.saved_button = wx.Button(mainpanel, wx.ID_ANY, "Durchsuchen")
    saved_project_box.Add(self.saved_button, 0)
    mainpanel_sizer.Add(saved_project_box, 0, wx.EXPAND)

    btnsizer = wx.StdDialogButtonSizer()
    load_btn = wx.Button(mainpanel, wx.ID_OK)
    btnsizer.AddButton(load_btn)
    cancel_btn = wx.Button(mainpanel, wx.ID_CANCEL)
    btnsizer.AddButton(cancel_btn)
    btnsizer.Realize()

    mainpanel_sizer.Add(btnsizer, 0, wx.ALIGN_CENTER)

    self.Bind(wx.EVT_RADIOBUTTON, self.OnNewSelection, self.new_radio)
    self.Bind(wx.EVT_RADIOBUTTON, self.OnSavedSelection, self.saved_radio)
    self.Bind(wx.EVT_BUTTON, self.OnSelectVideo, self.video_button)
    self.Bind(wx.EVT_BUTTON, self.OnSelectEyedata, self.eyedata_button)
    self.Bind(wx.EVT_RADIOBOX, self.OnEyeSelection, self.eye_rb)
    self.Bind(wx.EVT_RADIOBOX, self.OnCategorisationObjectSelection, self.frames_rb)

    self.Bind(wx.EVT_BUTTON, self.OnSelectSaved, self.saved_button)

    self.Bind(wx.EVT_BUTTON, self.OnLoad, load_btn)
    self.Bind(wx.EVT_BUTTON, self.OnCancel, cancel_btn)

    self.OnNewSelection()

  def OnEyeSelection(self, event):
    selection = self.eye_rb.GetSelection()
    if selection == 0:
      self.left_eye_categorisation = True
    elif selection == 1:
      self.left_eye_categorisation = False
    else:
      self.left_eye_categorisation = None

  def OnCategorisationObjectSelection(self, event):
    selection = self.frames_rb.GetSelection()
    if selection == 0:
      self.frame_categorisation = True
    else:
      self.frame_categorisation = False

  def OnNewSelection(self, event=None):
    self.saved_button.Enable(False)
    self.video_button.Enable(True)
    self.eyedata_button.Enable(True)
    self.saved_text.SetForegroundColour((125,125,125))
    self.video_text.SetForegroundColour((0,0,0))
    self.eyedata_text.SetForegroundColour((0,0,0))
    self.eye_rb.Enable(True)
    self.frames_rb.Enable(True)

    self.new_save = 'NEW'

  def OnSavedSelection(self, event=None):
    self.saved_button.Enable(True)
    self.video_button.Enable(False)
    self.eyedata_button.Enable(False)
    self.saved_text.SetForegroundColour((0,0,0))
    self.video_text.SetForegroundColour((125,125,125))
    self.eyedata_text.SetForegroundColour((125,125,125))
    self.eye_rb.Enable(False)
    self.frames_rb.Enable(False)

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

  def OnLoad(self, event):
    if self.new_save == 'NEW':
      try:
	self.parent.newProject(self.video_filepath, self.eyedata_filepath, self.frame_categorisation, self.left_eye_categorisation)
      except ReaderError as e: 
	error_dlg = wx.MessageDialog(self, 'Fehler beim Laden der Videodatei: %s' % e, 'Fehler', wx.OK | wx.ICON_ERROR)
	error_dlg.ShowModal()
      except EyeMovementError as e:
	error_dlg = wx.MessageDialog(self, 'Fehler beim Laden der Augendaten: %s' % e, 'Fehler', wx.OK | wx.ICON_ERROR)
	error_dlg.ShowModal()
      else:
	self.Destroy()
    else:
      try:
	self.parent.loadProject(self.saved_filepath)
      except:
	raise
      else:
	self.Destroy()

  def OnCancel(self, event):
    self.Destroy()
