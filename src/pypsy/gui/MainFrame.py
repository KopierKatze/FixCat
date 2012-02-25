from CategoryDialog import CategoryDialog
from StringImage import StringImage
from CategoryList import CategoryList
from OpenDialog import OpenDialog
import button_images

from pypsy.Config import Config
from pypsy.CategoryContainer import CategoryContainerError

import wx
import threading # used for video export

class MainFrame(wx.Frame):
    """This class handles the main window of pyPsy."""
    def __init__(self, video_str, current_frame, controller):
        """In order to manage everythin in the main window, the MainFrame needs
        to know the `controller` that handles everything, as well as the number
        `current_frame` and a string representation of the video image in
        `video_str`. For more information about `video_str`, please see
        L{StringImage}."""
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
        self.fps = 30 # used for time indicator in statusbar

        self.reloadTimer = wx.CallLater(1.0/35.0*1000, self.loadImage)
        self.reloadTimer.Stop()

        self.playing = False

        self.loopthrough_categorykey = None

        self.needs_save = False

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
        """Handles the behaviour of autosave, as well as the dialog that pops up."""
        if self.save_file is None:
            d = wx.MessageDialog(self, "This is the auto save dialog. You have not yet saved your modified project. Do you want to save the modifications? This dialog will only show up once.", style=wx.YES_NO)
            if d.ShowModal() == wx.ID_YES:
                self.OnSave()
            d.Destroy()
        else:
            self.statusBar.SetFields(['auto save...'])
            self.controller.save_project(self.save_file+"_autosave")
            self.autosave_timer.Restart()
            self.statusBar.SetFields([''])

    def InitMenu(self):
        """Draws the menu at the top of the window."""
        # menubar elements
        fileMenu = wx.Menu()
        menuOpen = fileMenu.Append(wx.ID_OPEN, "&Open", "Open")
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "About", "About PyPsy")
        menuSave = fileMenu.Append(wx.ID_SAVE, '&Save', "Save")
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "Quit" , "Quit")

        categoryMenu = wx.Menu()
        categoryEdit = categoryMenu.Append(wx.ID_ANY, "Manage categories")

        videoMenu = wx.Menu()
        exportVideo = videoMenu.Append(wx.ID_ANY, "Export", "Export video data to avi file")

        category_export = categoryMenu.Append(wx.ID_ANY, "Export categorisations", "Export categorisations to CSV file")


        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "File")
        menuBar.Append(categoryMenu, "Category")
        menuBar.Append(videoMenu, "Video")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        self.Bind(wx.EVT_MENU, self.OnExport, exportVideo)
        self.Bind(wx.EVT_MENU, self.OnCategoryExport, category_export)
        self.Bind(wx.EVT_MENU, self.OnEditCategory, categoryEdit)


    def InitUIControlls(self):
        """Initializes and draws the buttons and UI elements used for playback
        control or boxes defining which eyemovement data is used in the overlayed
        video."""
        play_bmp = button_images.getplayBitmap()
        pause_bmp = button_images.getpauseBitmap()
        next_f_bmp = button_images.getn_frameBitmap()
        prev_f_bmp = button_images.getp_frameBitmap()
        next_uncat_bmp = button_images.getnext_uncatBitmap()

        self.controllspanel = wx.Panel(self.mainpanel, wx.ID_ANY)
        self.slider = wx.Slider(self.controllspanel, wx.ID_ANY, 1, 0, 1000)
        self.Bind(wx.EVT_SCROLL, self.OnSliderScroll, self.slider)
        pause = wx.BitmapButton(self.controllspanel, -1, pause_bmp)
        pause.SetToolTip(wx.ToolTip('Pause playback'))
        self.Bind(wx.EVT_BUTTON, self.OnPause, pause)
        play = wx.BitmapButton(self.controllspanel, -1, play_bmp)
        play.SetToolTip(wx.ToolTip('Start/resume playback'))
        self.Bind(wx.EVT_BUTTON, self.OnPlay, play)
        next = wx.BitmapButton(self.controllspanel, -1, next_f_bmp)
        next.SetToolTip(wx.ToolTip('Jump to next frame'))
        self.Bind(wx.EVT_BUTTON, self.OnNextFrame, next)
        prev = wx.BitmapButton(self.controllspanel, -1, prev_f_bmp)
        prev.SetToolTip(wx.ToolTip('Jump to previous frame'))
        self.Bind(wx.EVT_BUTTON, self.OnPrevFrame, prev)
        self.speedslider = wx.Slider(self.controllspanel, wx.ID_ANY, 100, 10, 1000)
        self.speedslider.SetToolTip(wx.ToolTip('Change playback speed'))
        self.Bind(wx.EVT_SCROLL, self.OnSpeedSliderScroll, self.speedslider)

        self.speed_text = wx.StaticText(self.controllspanel, wx.ID_ANY, "Playback speed")
        #slower  = wx.Button(self.controllspanel, wx.ID_ANY, "90%")
        #self.Bind(wx.EVT_BUTTON, self.OnSlower, slower)
        #normal  = wx.Button(self.controllspanel, wx.ID_ANY, "100%")
        #self.Bind(wx.EVT_BUTTON, self.OnNormal, normal)
        #faster  = wx.Button(self.controllspanel, wx.ID_ANY, "110%")
        #self.Bind(wx.EVT_BUTTON, self.OnFaster, faster)
        next_uncategorised = wx.BitmapButton(self.controllspanel, -1, next_uncat_bmp)
        next_uncategorised.SetToolTip(wx.ToolTip('Jump to next uncategorised frame'))
        self.Bind(wx.EVT_BUTTON, self.OnNextUncategorisedObject, next_uncategorised)

        self.left_eye = wx.CheckBox(self.controllspanel, wx.ID_ANY, "L")
        self.left_eye.SetToolTip(wx.ToolTip('Display position of the left eye'))
        self.Bind(wx.EVT_CHECKBOX, self.OnLeftEyeCheckbox, self.left_eye)
        self.right_eye = wx.CheckBox(self.controllspanel, wx.ID_ANY, "R")
        self.right_eye.SetToolTip(wx.ToolTip('Display position of the right eye'))
        self.Bind(wx.EVT_CHECKBOX, self.OnRightEyeCheckbox, self.right_eye)
        self.mean_eye = wx.CheckBox(self.controllspanel, wx.ID_ANY, "M")
        self.mean_eye.SetToolTip(wx.ToolTip('Display mean position of both eyes'))
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
        hbox2.Add(self.speed_text)
        hbox2.Add((5, wx.ID_ANY))
        hbox2.Add(self.speedslider, 1)
        #hbox2.Add(slower)
        #hbox2.Add(normal)
        #hbox2.Add(faster)

        vbox.Add(hbox1, 1, wx.EXPAND)
        vbox.Add(hbox2, 1, wx.EXPAND)
        self.controllspanel.SetSizer(vbox)

    def seek(self, frame):
        """Helper function for handling the `slider` events."""
        self.controller.seek(frame)
        self.loadImage()

    def InitUI(self):
        """Initializes the different parts of the UI and adds the widget that
        displays the video."""
        self.InitMenu()
        self.statusBar = self.CreateStatusBar(3)
        self.statusBar.SetStatusWidths([-4,-1,150])

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

        self.Bind(wx.EVT_CLOSE, self.OnExit)

    def ActivateMouseAndKeyCatching(self):
        """Check for mouse or keyboard input of the user."""
        # ------ global mouse and key events ------------
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMousewheel)
        # catching key events is a lot more complicated. they are not propagated to parent classes...
        # so we have to get them from the app itself
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        # to also get arrow key and so on windows:
        wx.GetApp().Bind(wx.EVT_CHAR_HOOK, self.OnKeyPressed)

    def DeactivateMouseAndKeyCatching(self):
        """Stop checking for mouse or keyboard input of the user."""
        # ------ global mouse and key events ------------
        self.Bind(wx.EVT_MOUSEWHEEL, None)
        # catching key events is a lot more complicated. they are not propagated to parent classes...
        # so we have to get them from the app itself
        wx.GetApp().Bind(wx.EVT_KEY_DOWN, None)
        wx.GetApp().Bind(wx.EVT_CHAR_HOOK, None)

    def setEyeCheckboxStates(self):
        """Sets the checkboxes for which eyemovement data is currently displayed
        to what the user chose or to what is stored in the saved state."""
        left, right, mean = self.controller.getEyeStatus()
        self.left_eye.SetValue(left)
        self.right_eye.SetValue(right)
        self.mean_eye.SetValue(mean)

    def loadImage(self):
        """Updates the image of the video widget and displays the first
        frame of the video if a new project is started. This method also handles
        the status of the video, eg. `current time`, beeing displayed in the
        lower right corner of the MainFrame."""
        image_str = self.video_str.get_obj().raw[:self.video_str_length]
        self.videoimage.SetImage(image_str)

        self.slider.SetValue(self.current_frame.value)

        self.category_list.MarkFrame(self.current_frame.value)

        current_time = round(self.current_frame.value/self.fps)
        total_time = round(self.frames_total/self.fps)
        speed = self.speedslider.GetValue() * 0.01
        self.statusBar.SetStatusText('%.1fx %i:%02i/%i:%02i (%i/%i)'%(speed, current_time/60, current_time%60, total_time/60, total_time%60, self.current_frame.value,self.frames_total), 2)

        if self.controller.isClockRunning():
            self.reloadTimer.Restart()

    def newProject(self, video_filepath, eyemovement_filepath, trialid_target, categorise_frames, categorising_eye_is_left):
        """Initializes a new project with the input the user set in the OpenDialog."""
        self.controller.new_project(video_filepath, eyemovement_filepath, trialid_target, categorise_frames, categorising_eye_is_left)
        self.save_file = None
        self.needs_save = False
        self._loadProjectInfo()

    def newProjectPlausible(self):
        """This method runs the `Controller.plausibleCheck()` of the `controller`
        in order to check if the video and the eyemovement data match to a certain
        degree or not. If this is not the case, the user will see a dialog window
        asking, if he wants to continue."""
        return self.controller.plausibleCheck()

    def getMaxFramesOfEyeMovement(self):
        """Returns the overall number of frames contained in the trial of the
        eyemovement file by using `Controller.getMaxFramesOfEyeMovement()`."""
        return self.controller.getMaxFramesOfEyeMovement()

    def loadProject(self, filepath, overwrite_video_filepath=None):
        """Loads an existing project and its data."""
        self.controller.load_project(filepath, overwrite_video_filepath)
        self.save_file = filepath
        self.needs_save = False
        self._loadProjectInfo()

    def _loadProjectInfo(self):
        """Helper function for `loadProject()` that takes care of resetting the
        necessary parts of the UI for the project."""
        self.video_str_length = self.controller.getVideoStrLength()
        self.frames_total = self.controller.getVideoFrameCount()
        self.fps = self.controller.getVideoFrameRate()

        self.videoimage.SetImageSize(self.controller.getVideoWidth(), self.controller.getVideoHeight())

        self.slider.SetMax(self.controller.getVideoFrameCount())

        self.setEyeCheckboxStates()

        self.category_list.SetCategorisationOrder(self.controller.getCategorisationsOrder())
        self.loadCategorisationInToList()

        self.loadImage()

        if self.controller.categorisationEye() == 'left':
            status_text = "Left eye|"
        elif self.controller.categorisationEye() == 'right':
            status_text = "Right eye|"
        else:
            status_text = "Mean|"
        if self.controller.categorisationObjects() == 'frames':
            status_text += "Frames"
        else:
            status_text += "Fixations"
        self.statusBar.SetStatusText(status_text, 1)

        # start autosave timer
        self.autosave_timer.Restart()

    def loadCategorisationInToList(self):
        """Loads the list of categorisations from the controller into the widget
        on the right of the MainFrame, which displays the categorisations made
        so far."""
        self.category_list.FillInCategorisations(self.controller.getCategorisations())

    def getCategories(self):
        """Gets the categories from the `controller`."""
        return self.controller.getCategories()

    def editCategory(self, old_shortcut, new_shortcut, category_name):
        """Called if the user edited a category. Either its `category_name` is
        changed or the `old_shortcut` is changed to a `new_shortcut`."""
        self.needs_save = True
        return self.controller.editCategory(old_shortcut, new_shortcut, category_name)

    def importCategories(self, filepath):
        """Imports categories from an existing project into the one currently
        opened, by calling `Controller.importCategories()` in the `controller`."""
        self.needs_save = True
        self.controller.importCategories(filepath)

    def controllerIO(self):
        """This method checks if the `controller` is ready for use. Returns
        False if it is not."""
        if self.controller is None: return False
        if not self.controller.ready(): return False
        return True

        # ----- SHORTCUTS ----
    def OnMousewheel(self, event):
        """Handles user input from the mouse."""
        if event.GetWheelRotation() > 0:
            self.OnNextFrame(event)
        else:
            self.OnPrevFrame(event)

    def OnKeyPressed(self, event):
        """Handles user input from the keyboard."""
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
        elif key_code == self.config.get('keyboard_shortcuts', 'delete'):
            for to_delete in self.category_list.GetSelected():
                self.controller.deleteCategorisation(to_delete[0])
                self.category_list.Update(to_delete, "-")
                self.needs_save = True
        else:
            # try to categorise the current frame to the category which may belong tho key_code
            if self.categorise(key_code) and event.GetEventType() == wx.EVT_KEY_DOWN:
                if self.controller.categorisationObjects() == 'frames':
                    self.OnNextFrame()
                else:
                    self.OnNextFixation()

    def categorise(self, key_code, overwrite=True):
        """Categorises the current frame with the category that belongs to `key_code`.
        This method also takes care of the loopthrough of a category from one
        fixation/frame to the next."""
        if key_code is None: return
        if not overwrite and not self.controller.getCategoryOfFrame(self.current_frame.value) is None: return
        try:
            return_info = self.controller.categorise(key_code)
        except CategoryContainerError:
            # the category container will raise an error when the keycode is not assigned
            # and as we forward nearly all pressed keys this would be quite annoying
            return_info = False
            return False
        if return_info:
            self.needs_save = True
            index, category = return_info
            self.category_list.Update(index, category)
            # load Image so category_list will jump to categorised frame
            self.category_list.MarkFrame(self.current_frame.value)

            self.loopthrough_categorykey = key_code
            return True


    # ---------------- PLAYBACK CONTROLL --------------
    def OnPlay(self, event=None):
        """Playback of the video, either if the button in the UI was used, or if
        the user used the keybaord shortcut."""
        self.loopthrough_categorykey = None

        self.playing = True
        self.controller.play()
        self.loadImage()

    def OnPause(self, event=None):
        """Stops playback, either if the button in the UI was used, or if
        the user used the keybaord shortcut."""
        self.loopthrough_categorykey = None

        self.playing = False
        self.controller.pause()
        self.loadImage()

    def OnNextFrame(self, event=None):
        """Loads and displays the next frame, either if the button in the UI was
        used or if the user used the keyboard shortcut. The user can also jump to
        the next frame by using the mousewheel."""
        self.controller.nextFrame()
        self.loadImage()
        self.categorise(self.loopthrough_categorykey, False)

    def OnPrevFrame(self, event=None):
        """Loads and displays the previous frame, either if the button in the UI was
        used or if the user used the keyboard shortcut. The user can also jump to
        the previous frame by using the mousewheel."""
        self.controller.prevFrame()
        self.loadImage()
        self.categorise(self.loopthrough_categorykey, False)

    def OnNextFixation(self, event=None):
        """Jumps to the next fixation, either if the user used the UI button or 
        the keyboard shortcut."""
        self.controller.nextFixation()
        self.loadImage()
        self.categorise(self.loopthrough_categorykey, False)

    def OnPrevFixation(self, event=None):
        """Jumps to the previous fixation, either if the user used the UI button or 
        the keyboard shortcut."""
        self.controller.prevFixation()
        self.loadImage()
        self.categorise(self.loopthrough_categorykey, False)

    def OnSlower(self, event=None):
        """Reduces playback speed to 90% if the user clicked on the `slower` button."""
        self.controller.slowerPlayback()

    def OnNormal(self, event=None):
        """Resets playback speed to normal."""
        self.controller.normalPlayback()

    def OnFaster(self, event=None):
        """Increases playback speed to 1100% if the user clicked on the `faster` button."""
        self.controller.fasterPlayback()

    def OnSliderScroll(self, event):
        """Sets the slider to the new value produced by moving the `slider`."""
        self.loopthrough_categorykey = None

        self.seek(self.slider.GetValue())

    def OnSpeedSliderScroll(self, event=None):
        """Sets the slider for playback speed control to the new value produced
        by moving the `speedslider`. This method also handles the update of the status
        information of the video displayed in the lower right corner."""
        current_time = round(self.current_frame.value/self.fps)
        total_time = round(self.frames_total/self.fps)
        speed = self.speedslider.GetValue() * 0.01
        self.statusBar.SetStatusText('%.1fx %i:%02i/%i:%02i (%i/%i)'%(speed, current_time/60, current_time%60, total_time/60, total_time%60, self.current_frame.value,self.frames_total), 2)
        self.controller.setPlaybackSpeed(speed)

    def OnNextUncategorisedObject(self,event):
        """Called if the user clicked on the UI button for the `next_uncategorised`
        frame or fixation."""
        self.loopthrough_categorykey = None

        self.controller.jumpToNextUncategorisedObject()
        self.loadImage()
    # ---------------- PLAYBACK CONTROLL END ----------

    # ---------------- SHOWING EYE STATUS CONTROLLS ---
    def OnLeftEyeCheckbox(self, event):
        """Called, if the checkbox for the left eye in the UI controls panel is
        checked."""
        self.controller.leftEyeStatus(event.Checked())
        # load changed image, important if we currently not playing
        self.loadImage()
    def OnRightEyeCheckbox(self, event):
        """Called, if the checkbox for the right eye in the UI controls panel is
        checked."""
        self.controller.rightEyeStatus(event.Checked())
        # load changed image, important if we currently not playing
        self.loadImage()
    def OnMeanEyeCheckbox(self, event):
        """Called, if the checkbox for the mean eye status in the UI controls panel 
        is checked."""
        self.controller.meanEyeStatus(event.Checked())
        # load changed image, important if we currently not playing
        self.loadImage()
    # ---------------- SHOWING EYE STATUS END --------

    #----------------- MENU ITEMS --------------------
    def OnCategoryExport(self, event):
        """Guides the user through the process of exporting categories. After 
        the user selected the output file in the dialog, 
        `Controller.exportCategorisations()` is called and handles the export."""
        file_dialog = wx.FileDialog(self, "Export CSV", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard="CSV file (*.csv)|*.csv")
        if file_dialog.ShowModal() == wx.ID_OK:
            path = file_dialog.GetPath()
            if not "." in path:
                path += ".csv"
            self.controller.exportCategorisations(path)

    def OnAbout(self, e):
        """Shows the about text of pyPsy."""
        dlg = wx.MessageDialog(self, "PyPsy is a tool for processing eyetracking Data.", "About PyPsy", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def SaveAsk(self):
        """Called, if the user has made changes to the project and if `OnExit()`
        is called. This method takes care of showing a dialog if the user wants
        to continue or save the changes. If yes was selected, `OnSave()` is called."""
        if self.needs_save:
            dlg = wx.MessageDialog(self, "The project has been modified. Do you want to save your changes?", "Save changes?", wx.YES_NO|wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self.OnSave()

    def OnExit(self, e):
        """Closes pyPsy and shows a dialog if the user wants to save the changes
        made if necessary."""
        self.SaveAsk()
        self.Destroy()

    def OnOpen(self, event=None, bootstrap_phase=False):
        """Opens the OpenDialog that guides the user through the process of either
        loading an existing project or creating a new one."""
        self.SaveAsk()
        open_dialog = OpenDialog(self, bootstrap_phase)
        open_dialog.ShowModal()

    def OnEditCategory(self, e):
        """Opens the CategoryDialog that displays all categories and their
        shortcuts. In this dialog, the user can add, delete, edit and import
        categories."""
        CategoryDialog(self, wx.ID_ANY).ShowModal()

    def OnSave(self, event=None):
        """Opens a dialog for saving the project to a file."""
        file_dialog = wx.FileDialog(self, "Save project", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard="PYPS Datei (*.pyps)|*.pyps")
        if file_dialog.ShowModal() == wx.ID_OK:
            path = file_dialog.GetPath()
            if not "." in path:
                path += ".pyps"
            self.controller.save_project(path)
            self.save_file = path
            self.needs_save = False
            self.autosave_timer.Restart()

    def OnExport(self, event):
        """This method takes care of the export of a video. For better performance,
        this is handled in a new thread `waiting_thread`. While this thread works,
        a progress dialog will show up. """
        file_dialog = wx.FileDialog(self, "Export video", style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard="AVI file (*.avi)|*.avi")
        if file_dialog.ShowModal() == wx.ID_OK:
            path = file_dialog.GetPath()
            if not "." in path:
                path += ".avi"

            progress_dialog = wx.ProgressDialog('Video Export', 'Exporting video...', parent=self, maximum=self.frames_total,
              style=wx.PD_APP_MODAL|wx.PD_REMAINING_TIME|wx.PD_ELAPSED_TIME|wx.PD_SMOOTH)

            # show progress by displaying the current frame
            waiting_thread = threading.Thread()
            waiting_thread.run = lambda: self.controller.exportVideo(path)
            waiting_thread.start()
            while waiting_thread.isAlive():
                wx.MilliSleep(900)
                progress_dialog.Update(self.current_frame.value)
            progress_dialog.Destroy()
            self.loadImage()


if __name__ == '__main__':

    app = wx.App()
    Example(None, title="eyepsy window")
    app.MainLoop()
