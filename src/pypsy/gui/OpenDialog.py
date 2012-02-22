import wx
import  wx.lib.intctrl
from pypsy.VideoReader import ReaderError
from pypsy.EyeMovement import EyeMovementError

class OpenDialog(wx.Dialog):
    def __init__(self, parent, bootstrap_phase=False):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Load existing project or start a new one", size=(430,310))

        self.bootstrap_phase = bootstrap_phase

        self.parent = parent

        self.new_save = 'NEW'
        self.video_filepath = None
        self.eyedata_filepath = None
        self.left_eye_categorisation = True # None -> mean eye, True -> left eye, False -> right eye
        self.frame_categorisation = True # False -> fixation categorisation

        self.saved_filepath = None

        self.InitUI()

        self.Center()

    def InitUI(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.new_radio = wx.RadioButton(self, wx.ID_ANY, "Start a new project")
        sizer.Add(self.new_radio, 0)
        new_project_video_box = wx.BoxSizer(wx.HORIZONTAL)
        self.video_text = wx.StaticText(self, wx.ID_ANY, "Choose video file...")
        new_project_video_box.Add(self.video_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
        self.video_button = wx.Button(self, wx.ID_ANY, "Open")
        new_project_video_box.Add(self.video_button, 0, wx.ALIGN_RIGHT)
        sizer.Add(new_project_video_box, 0, wx.EXPAND)

        new_project_eyedate_box = wx.BoxSizer(wx.HORIZONTAL)
        self.eyedata_text = wx.StaticText(self, wx.ID_ANY, "Choose EDF...")
        new_project_eyedate_box.Add(self.eyedata_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
        self.eyedata_button = wx.Button(self, wx.ID_ANY, "Open")
        new_project_eyedate_box.Add(self.eyedata_button, 0)
        sizer.Add(new_project_eyedate_box, 0, wx.EXPAND)

        self.eye_rb = wx.RadioBox(self, wx.ID_ANY, "Data of eye you want to categorise", choices=['left', 'right', 'mean'])
        sizer.Add(self.eye_rb, 0, wx.LEFT, 25)

        self.frames_rb = wx.RadioBox(self, wx.ID_ANY, "Categorise frames or fixations", choices=['frame', 'fixations'])
        sizer.Add(self.frames_rb, 0, wx.LEFT, 25)

        trialid_box = wx.BoxSizer(wx.HORIZONTAL)
        self.trialid_text = wx.StaticText(self, wx.ID_ANY, "Select trial id...")
        trialid_box.Add(self.trialid_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
        self.trialid_target = wx.lib.intctrl.IntCtrl(self, limited=True)
        self.trialid_target.SetValue(1)
        self.trialid_target.SetMin(1)
        trialid_box.Add(self.trialid_target, 0)
        sizer.Add(trialid_box, 0, wx.EXPAND)

        self.saved_radio = wx.RadioButton(self, wx.ID_ANY, "Load an existing project")
        sizer.Add(self.saved_radio, 0)
        saved_project_box = wx.BoxSizer(wx.HORIZONTAL)
        self.saved_text = wx.StaticText(self, wx.ID_ANY, "Choose existing project...")
        saved_project_box.Add(self.saved_text, 1, wx.ALIGN_CENTER|wx.LEFT, 25)
        self.saved_button = wx.Button(self, wx.ID_ANY, "Open")
        saved_project_box.Add(self.saved_button, 0)
        sizer.Add(saved_project_box, 0, wx.EXPAND)

        line = wx.StaticLine(self, wx.ID_ANY, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.TOP|wx.BOTTOM, 10)

        btnsizer = wx.StdDialogButtonSizer()
        load_btn = wx.Button(self, wx.ID_OK)
        btnsizer.AddButton(load_btn)
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(cancel_btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER)

        self.SetSizer(sizer)

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
        self.trialid_target.Enable(True)
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
        self.trialid_target.Enable(False)
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
        q = self._open_file('Choose video file...', 'AVI file (*.avi)|*.avi')
        if not q is None:
            self.video_text.SetLabel(q)
            self.video_filepath = q

    def OnSelectEyedata(self, event):
        q = self._open_file('Choose edf...', 'ASC file (*.asc)|*.asc')
        if not q is None:
            self.eyedata_text.SetLabel(q)
            self.eyedata_filepath = q

    def OnSelectSaved(self, event):
        q = self._open_file('Choose existing project', 'PYPS file (*.pyps)|*.pyps|PYPS-AUTOSAVES (*.pyps_autosave)|*.pyps_autosave')
        if not q is None:
            self.saved_text.SetLabel(q)
            self.saved_filepath = q

    def OnLoad(self, event=None, overwrite_video_filepath=None):
        try:
            if self.new_save == 'NEW':
                self.parent.newProject(self.video_filepath, self.eyedata_filepath, self.trialid_target.GetValue(), self.frame_categorisation, self.left_eye_categorisation)
                if not self.parent.newProjectPlausible():
                    dlg = wx.MessageDialog(self, 'Are you sure you have selected the right video and eyemovement file/trial? The video has %s frames but the eyemovement trial has information for %s frames. Do you want to continue?' % (self.parent.frames_total, self.parent.getMaxFramesOfEyeMovement()), 'Plausibility check', wx.YES_NO | wx.ICON_INFORMATION)
                    if not dlg.ShowModal() == wx.ID_YES:
                        return
            else:
                self.parent.loadProject(self.saved_filepath, overwrite_video_filepath)
        except ReaderError as e:
            error_dlg = wx.MessageDialog(self, 'Error while loading video file: %s' % e, 'Error', wx.OK | wx.ICON_ERROR)
            error_dlg.ShowModal()
            if self.new_save == 'SAVE':
                video_filepath = self._open_file('Choose video file...', 'AVI file (*.avi)|*.avi')
                if not video_filepath is None:
                    self.OnLoad(overwrite_video_filepath=video_filepath)
        except EyeMovementError as e:
            error_dlg = wx.MessageDialog(self, 'Error while loading eyemovement data: %s' % e, 'Error', wx.OK | wx.ICON_ERROR)
            error_dlg.ShowModal()
        else:
            self.Destroy()

    def OnCancel(self, event):
        if self.bootstrap_phase:
            raise SystemExit()
        self.Destroy()
