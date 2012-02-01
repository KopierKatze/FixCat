from CategoryDialog import CategoryDialog
from StringImage import StringImage
from CategoryList import CategoryList
from OpenDialog import OpenDialog

from pypsy.Config import Config

import wx
import threading # used for video export

class MainFrame(wx.Frame):
    def __init__(self, video_str, current_frame, controller):
        wx.Frame.__init__(self, None, title="pyPsy",
            size=(900, 600))

        self.controller = controller

        self.InitUI()
        self.Centre()
        self.Maximize()
        self.Show()

        self.video_str = video_str
        self.current_frame = current_frame

        self.frames_total = 0 # used for video export progress bar

        self.reloadTimer = wx.CallLater(1.0/35.0*1000, self.loadImage)
        self.reloadTimer.Stop()
        self.autoreload = False

        self.playing = False

        self.loopthrough_categorykey = None

        self.config = Config()

        self.save_file = None
        asm = self.config.get('general', 'autosave_minutes')
        if asm is None:
	  self.autosave_timer = wx.CallLater(10, lambda: None)
	  self.autosave_timer.Restart = lambda: None
	else:
	  self.autosave_timer = wx.CallLater(asm*60*1000, self.autosave)
	  # activated on project load
	  self.autosave_timer.Stop()

	self.OnOpen(bootstrap_phase=True)

	self.ActivateMouseAndKeyCatching()

    def autosave(self):
        if self.save_file is None:
	    d = wx.MessageDialog(self, "Hi, ich wuerde jetzt das aktuelle Projekt speichern. Kann das aber nicht tun, weil es noch nicht gepspeichert wurde. Soll es jetzt gepspeichert werden? (Ich werde nicht wieder damit nerven)", style=wx.YES_NO)
	    if d.ShowModal() == wx.ID_YES:
	      self.OnSave()
	    d.Destroy()
	else:
	    self.statusBar.SetFields(['Automatisches Speichern...'])
	    self.controller.save_project(self.save_file)
	    self.autosave_timer.Restart()
	    self.statusBar.SetFields([''])

    def InitMenu(self):
        # menubar elements
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Oeffnen", "Oeffnen")
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "Ueber", "Ueber pyPsy")
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Speichern', "Speichern")
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "Beenden" , "Schliessen")

        categoryMenu = wx.Menu()
        categoryEdit = categoryMenu.Append(wx.ID_ANY, "Kategorien verwalten")

        tempMenu = wx.Menu()
        exportVideo = tempMenu.Append(wx.ID_ANY, "Export", "Video als AVI-Datei exportieren")

        category_export = categoryMenu.Append(wx.ID_ANY, "Kategoriesierungen exportieren", "Kategorisierungen als CSV-Datei exportieren")


        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "Datei")
        menuBar.Append(categoryMenu, "Kategorie")
        menuBar.Append(tempMenu, "Video")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExport, exportVideo)
        self.Bind(wx.EVT_MENU, self.OnCategoryExport, category_export)
        self.Bind(wx.EVT_MENU, self.OnEditCategory, categoryEdit)


    def InitUIControlls(self):
	# fetch bitmaps of bitmapbuttons
	playfile = "pypsy/gui/buttons/play.png"
	pausefile = "pypsy/gui/buttons/pause.png"
	nextfile = "pypsy/gui/buttons/n_frame.png"
	prevfile = "pypsy/gui/buttons/p_frame.png"
	next_uncatfile = "pypsy/gui/buttons/next_uncat.png"
	play_bmp = wx.Image(playfile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	pause_bmp = wx.Image(pausefile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	next_f_bmp = wx.Image(nextfile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	prev_f_bmp = wx.Image(prevfile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	next_uncat_bmp = wx.Image(next_uncatfile, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
	
        self.controllspanel = wx.Panel(self.mainpanel, wx.ID_ANY)
        self.slider = wx.Slider(self.controllspanel, wx.ID_ANY, 0, 0, 1000)
        self.Bind(wx.EVT_SCROLL, self.OnSliderScroll, self.slider)
        pause = wx.BitmapButton(self.controllspanel, -1, pause_bmp)
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        play = wx.BitmapButton(self.controllspanel, -1, play_bmp)
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play)
        next = wx.BitmapButton(self.controllspanel, -1, next_f_bmp)
        self.Bind(wx.EVT_BUTTON, self.OnNextFrame, next)
        prev = wx.BitmapButton(self.controllspanel, -1, prev_f_bmp)
        self.Bind(wx.EVT_BUTTON, self.OnPrevFrame, prev)
        slower  = wx.Button(self.controllspanel, wx.ID_ANY, "90%")
        self.Bind(wx.EVT_BUTTON, self.OnSlower, slower)
        normal  = wx.Button(self.controllspanel, wx.ID_ANY, "100%")
        self.Bind(wx.EVT_BUTTON, self.OnNormal, normal)
        faster  = wx.Button(self.controllspanel, wx.ID_ANY, "110%")
        self.Bind(wx.EVT_BUTTON, self.OnFaster, faster)
        next_uncategorised = wx.BitmapButton(self.controllspanel, -1, next_uncat_bmp)
        self.Bind(wx.EVT_BUTTON, self.OnNextUncategorisedObject, next_uncategorised)

        self.left_eye = wx.CheckBox(self.controllspanel, wx.ID_ANY, "L")
        self.Bind(wx.EVT_CHECKBOX, self.OnLeftEyeCheckbox, self.left_eye)
        self.right_eye = wx.CheckBox(self.controllspanel, wx.ID_ANY, "R")
        self.Bind(wx.EVT_CHECKBOX, self.OnRightEyeCheckbox, self.right_eye)
        self.mean_eye = wx.CheckBox(self.controllspanel, wx.ID_ANY, "M")
        self.Bind(wx.EVT_CHECKBOX, self.OnMeanEyeCheckbox, self.mean_eye)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox1.Add(self.slider, 1)
        hbox2.Add(prev)
        hbox2.Add(play)
        hbox2.Add(pause)
        hbox2.Add(next)
        hbox2.Add(next_uncategorised)
        hbox2.Add(self.left_eye, flag=wx.LEFT, border=15)
        hbox2.Add(self.right_eye)
        hbox2.Add(self.mean_eye)
        hbox2.Add((150, wx.ID_ANY), 1)
        hbox2.Add(slower)
        hbox2.Add(normal)
        hbox2.Add(faster)

        vbox.Add(hbox1, 1, wx.EXPAND)
        vbox.Add(hbox2, 1, wx.EXPAND)
        self.controllspanel.SetSizer(vbox)

    def seek(self, frame):
      self.controller.seek(frame)
      self.loadImage()

    def InitUI(self):
        self.InitMenu()
        self.statusBar = self.CreateStatusBar()

        # correct colors in windows 7
        self.mainpanel = wx.Panel(self, wx.ID_ANY)

        # this sizer will locate the widgets
        contentsizer = wx.BoxSizer(wx.VERTICAL)
        self.mainpanel.SetSizer(contentsizer)

        # upper side: video image and categorylist
        uppersizer = wx.BoxSizer(wx.HORIZONTAL)

        self.videoimage = StringImage(self.mainpanel, wx.ID_ANY)
        self.category_list = CategoryList(self.mainpanel, wx.ID_ANY, self.seek)

        uppersizer.Add(self.videoimage, 1, flag=wx.RIGHT|wx.EXPAND, border=5)
        uppersizer.Add(self.category_list, 0, flag=wx.ALIGN_RIGHT|wx.EXPAND)

        contentsizer.Add(uppersizer, 1, flag=wx.EXPAND)

        # lower side: controlls
        self.InitUIControlls()
        contentsizer.Add(self.controllspanel, 0, flag=wx.EXPAND|wx.TOP|wx.ALIGN_BOTTOM, border=5)
	
    def ActivateMouseAndKeyCatching(self):
        # ------ global mouse and key events ------------
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMousewheel)
        # catching key events is a lot more complicated. they are not propagated to parent classes...
        # so we have to get them from the app itself
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)

    def DeactivateMouseAndKeyCatching(self):
        # ------ global mouse and key events ------------
        self.Bind(wx.EVT_MOUSEWHEEL, None)
        # catching key events is a lot more complicated. they are not propagated to parent classes...
        # so we have to get them from the app itself
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, None)

    def setEyeCheckboxStates(self):
      left, right, mean = self.controller.getEyeStatus()
      self.left_eye.SetValue(left)
      self.right_eye.SetValue(right)
      self.mean_eye.SetValue(mean)

    def loadImage(self):
      image_str = self.video_str.get_obj().raw[:self.video_str_length]
      self.videoimage.SetImage(image_str)
      self.slider.SetValue(self.current_frame.value)
      self.category_list.MarkFrame(self.current_frame.value)

      if self.autoreload:
	self.reloadTimer.Restart()

    def newProject(self, video_filepath, eyemovement_filepath, categorise_frames, categorising_eye_is_left):
      self.controller.new_project(video_filepath, eyemovement_filepath, categorise_frames, categorising_eye_is_left)
      self.save_file = None
      self._loadProjectInfo()

    def loadProject(self, filepath):
      self.controller.load_project(filepath)
      self.save_file = filepath
      self._loadProjectInfo()

    def _loadProjectInfo(self):
      self.video_str_length = self.controller.getVideoStrLength()
      self.videoimage.SetImageSize(self.controller.getVideoWidth(), self.controller.getVideoHeight())
      self.slider.SetMax(self.controller.getVideoFrameCount())
      self.frames_total = self.controller.getVideoFrameCount()
      self.setEyeCheckboxStates()
      self.category_list.SetCategorisationOrder(self.controller.getCategorisationsOrder())
      self.loadCategorisationInToList()
      self.loadImage()

      # start autosave timer
      self.autosave_timer.Restart()

    def loadCategorisationInToList(self):
      self.category_list.FillInCategorisations(self.controller.getCategorisations())

    def getCategories(self):
      return self.controller.getCategories()

    def editCategory(self, old_shortcut, new_shortcut, category_name):
      return self.controller.editCategory(old_shortcut, new_shortcut, category_name)

    def importCategories(self, filepath):
      self.controller.importCategories(filepath)

    def controllerIO(self):
      if self.controller is None: return False
      if not self.controller.ready(): return False
      return True

    # ----- SHORTCUTS ----
    def OnMousewheel(self, event):
      if event.GetWheelRotation() > 0:
	self.OnNextFrame(event)
      else:
	self.OnPrevFrame(event)

    def OnKeyPressed(self, event):
      key_code = event.GetKeyCode()

      if key_code == self.config.get('keyboard_shortcuts', 'prev_frame'):
	self.OnPrevFrame()
      elif key_code == self.config.get('keyboard_shortcuts', 'next_frame'):
	self.OnNextFrame()
      elif key_code == self.config.get('keyboard_shortcuts', 'next_fixation'):
	self.OnNextFixation()
      elif key_code == self.config.get('keyboard_shortcuts', 'prev_fixation'):
	self.OnPrevFixation()
      elif key_code == self.config.get('keyboard_shortcuts', 'faster'):
	self.OnFaster()
      elif key_code == self.config.get('keyboard_shortcuts', 'slower'):
	self.OnSlower()
      elif key_code == self.config.get('keyboard_shortcuts', 'play/pause'):
	if self.playing:
	  self.OnPause()
	else:
	  self.OnPlay()
      else:
	# try to categorise the current frame to the category which may belong tho key_code
	self.categorise(key_code)


    def categorise(self, key_code, overwrite=True):
      if key_code is None: return
      if not overwrite and not self.controller.getCategoryOfFrame(self.current_frame.value) is None: return
      return_info = self.controller.categorise(key_code)
      if return_info:
	index, category = return_info
	self.category_list.Update(index, category)
	# load Image so category_list will jump to categorised frame
	self.category_list.MarkFrame(self.current_frame.value)
	
	self.loopthrough_categorykey = key_code

    # ---------------- PLAYBACK CONTROLL --------------
    def OnPlay(self, event=None):
      self.loopthrough_categorykey = None

      self.playing = True
      self.controller.play()
      self.autoreload = True
      self.loadImage()

    def OnPause(self, event=None):
      self.loopthrough_categorykey = None

      self.playing = False
      self.controller.pause()
      self.autoreload = False
      self.loadImage()

    def OnNextFrame(self, event=None):
      self.controller.nextFrame()
      self.loadImage()
      self.categorise(self.loopthrough_categorykey, False)

    def OnPrevFrame(self, event=None):
      self.controller.prevFrame()
      self.loadImage()
      self.categorise(self.loopthrough_categorykey, False)

    def OnNextFixation(self, event=None):
      self.controller.nextFixation()
      self.loadImage()
      self.categorise(self.loopthrough_categorykey, False)

    def OnPrevFixation(self, event=None):
      self.controller.prevFixation()
      self.loadImage()
      self.categorise(self.loopthrough_categorykey, False)

    def OnSlower(self, event=None):
      self.controller.slowerPlayback()

    def OnNormal(self, event=None):
      self.controller.normalPlayback()

    def OnFaster(self, event=None):
      self.controller.fasterPlayback()

    def OnSliderScroll(self, event):
      self.loopthrough_categorykey = None

      self.seek(self.slider.GetValue())

    def OnNextUncategorisedObject(self,event):
      self.loopthrough_categorykey = None

      self.controller.jumpToNextUncategorisedObject()
      self.loadImage()

    # ---------------- PLAYBACK CONTROLL END ----------
    # ---------------- SHOWING EYE STATUS CONTROLLS ---
    def OnLeftEyeCheckbox(self, event):
      self.controller.leftEyeStatus(event.Checked())
      # load changed image, important if we currently not playing
      self.loadImage()
    def OnRightEyeCheckbox(self, event):
      self.controller.rightEyeStatus(event.Checked())
      # load changed image, important if we currently not playing
      self.loadImage()
    def OnMeanEyeCheckbox(self, event):
      self.controller.meanEyeStatus(event.Checked())
      # load changed image, important if we currently not playing
      self.loadImage()
    # ---------------- SHOWING EYE STATUS END --------

    def OnCategoryExport(self, event):
      file_dialog = wx.FileDialog(self, "CSV Export", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard="CSV Datei (*.csv)|*.csv")
      if file_dialog.ShowModal() == wx.ID_OK:
	path = file_dialog.GetPath()
	if not "." in path:
	  path += ".csv"
        self.controller.exportCategorisations(path)
    #------------------------------------------- menu items     
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "PyPsy ist ein Tool, das bei der Verarbeitung von Eyetracking-Daten hilft.", "Ueber PyPsy", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, e):
        #wx.CallAfter(self.controller.pause ()) doesn't work
        self.Close(True)

    def OnOpen(self, event=None, bootstrap_phase=False):
      open_dialog = OpenDialog(self, bootstrap_phase)
      open_dialog.ShowModal()

    def OnEditCategory(self, e):
        CategoryDialog(self, wx.ID_ANY).ShowModal()

    def OnSave(self, event=None):
      file_dialog = wx.FileDialog(self, "Projekt speichern", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard="PYPS Datei (*.pyps)|*.pyps")
      if file_dialog.ShowModal() == wx.ID_OK:
	path = file_dialog.GetPath()
	if not "." in path:
	  path += ".pyps"
	self.controller.save_project(path)
	self.save_file = path
	self.autosave_timer.Restart()

    def OnExport(self, event):
      file_dialog = wx.FileDialog(self, "Video exportieren", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard="AVI Datei (*.avi)|*.avi")
      if file_dialog.ShowModal() == wx.ID_OK:
	path = file_dialog.GetPath()
	if not "." in path:
	  path += ".avi"

	progress_dialog = wx.ProgressDialog('Video Export', 'Exportiere Video...', parent=self, maximum=self.frames_total,
	  style=wx.PD_APP_MODAL|wx.PD_REMAINING_TIME|wx.PD_ELAPSED_TIME|wx.PD_SMOOTH)
	# show progress by displaying the current frame
	self.autoreload = True
	self.loadImage()
	waiting_thread = threading.Thread()
	waiting_thread.run = lambda: self.controller.exportVideo(path)
	waiting_thread.start()
	while waiting_thread.isAlive():
	  wx.MilliSleep(500)
	  progress_dialog.Update(self.current_frame.value)
	# stop reloading frame
	self.autoreload = False
	progress_dialog.Destroy()


if __name__ == '__main__':
  
    app = wx.App()
    Example(None, title="eyepsy window")
    app.MainLoop()

