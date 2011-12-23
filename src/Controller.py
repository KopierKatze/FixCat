from CategoryContainer import CategoryContainer
from Clock import Clock
from Cursor import Cursor
from EyeMovement import EyeMovement
from VideoReader import VideoReader, ReaderError
from VideoWriter import VideoWriter

import cv

class Controller(object):
  """this class connects all the in- and output classes together and provides a
  clean interface for the connection to the gui"""
  def __init__(self, gui):
    self.gui = gui
    self.gui.controller = self
    self.video_reader = None
    self.eye_movement = None
    self.clock = None
    self.cursor = None
    self.category_container = None
    self.categorise_frames = False

  def ready(self):
    """you should'nt always make sure this class is ready before using it's functions.
    ready means every data needed is available"""
    return bool(self.video_reader) and \
	   bool(self.eye_movement) and \
	   bool(self.clock) and \
	   bool(self.cursor) and \
	   bool(self.category_container)

  def new_project(self, video_file, eye_movement_file, categorise_frames=False):
    """create a new project.
    you can decide whether you want to categorise frames or fixations by the 'categorise_frames' flag.
    """
    self.cursor = Cursor()
    
    self.categorise_frames = categorise_frames
    self.eye_movement = EyeMovement(eye_movement_file)
    self.video_reader = VideoReader(video_file)

    self.clock = Clock(self.video_reader.duration, self.video_reader.fps)
    self.clock.register(self._tick)
    
    if self.categorise_frames:
      number_of_indexes = self.video_reader.total_frames
    else:
      number_of_indexes = self.eye_movement.countFixations()

    self.category_container = CategoryContainer(int(number_of_indexes))

    self.gui.newVideo(self.video_reader.total_frames)

  def _tick(self, frame):
    """will populate current image to gui.
    have a look at Clock class for more information."""
    self.gui.setImageAndFrame(self.overlayedFrame(frame, True, True, True), frame)

  def overlayedFrame(self, frame, left, right, mean):
    image = self.video_reader.frame(frame)

    left_look = self.eye_movement.leftLookAt(frame)
    right_look = self.eye_movement.rightLookAt(frame)
    mean_look = self.eye_movement.meanLookAt(frame)
    # TODO: this try-except block is really bad taste! only for the show today
    try:
      if left and right_look[0] < image.width and right_look[1] < image.height:
	left_cursor = self.cursor.cursorFor(self.eye_movement.statusLeftEyeAt(frame))
	cv.SetImageROI(image, (int(left_look[0]), int(left_look[1]), left_cursor.width, left_cursor.height))
	cv.Add(image, left_cursor, image)

      if right and left_look[0] < image.width and left_look[1] < image.height:
	right_cursor = self.cursor.cursorFor(self.eye_movement.statusRightEyeAt(frame))
	cv.SetImageROI(image, (int(right_look[0]), int(right_look[1]), right_cursor.width, right_cursor.height))
	cv.Add(image, right_cursor, image)


      if mean and mean_look[0] < image.width and mean_look[1] < image.height:
	mean_cursor = self.cursor.cursorFor(self.eye_movement.meanStatusAt(frame))
	cv.SetImageROI(image, (int(mean_look[0]), int(mean_look[1]), mean_cursor.width, mean_cursor.height))
	cv.Add(image, mean_cursor, image)
    except Exception:
      pass

    return image

  def play(self):
    if not self.clock.running: self.clock.run()

  def pause(self):
    if self.clock.running: self.clock.stop()

  def seek(self, second):
    self.clock.seek(second)

  def categorise(self, shortcut):
    if self.categorise_frames:
      index = self.video_reader.frameNumberOfSecond(self.clock.time)
      self.category_container.categorise(index, shortcut)
    else:
      pass
# -----------  FRAME JUMPING ----
  def nextFrame(self):
    """jump one frame into the future"""
    self.seek(self.clock.frame + 1)

  def prevFrame(self):
    """jump one frame into the past"""
    self.seek(self.clock.frame - 1)

  def jumpToNextUncategorisedFixation(self):
    """no yet"""
    pass

  def getCategoryContainer(self):
    """returns the category_container of this controller."""
    return self.category_container
# --------------- PLAYBACK SPEED -----
  def slowerPlayback(self):
    self.clock.setMultiplicator(self.clock.multiplicator * 0.9)
  def normalPlayback(self):
    self.clock.setMultiplicator(1.0)
  def fasterPlayback(self):
    self.clock.setMultiplicator(self.clock.multiplicator * 1.1)
if __name__ == '__main__':
  from gui.MainFrame import MainFrame
  import wx
  a = wx.App()
  e = MainFrame()
  e.Show()

  from thread import start_new_thread
  start_new_thread(a.MainLoop, ())
  controller = Controller(e)
  #controller.new_project("../example/t2d1gl_ett0.avi", "../example/t2d1gl.asc", True)
  controller.new_project("../example/overlayed_video.avi", "../example/t2d1gl.asc", True)
  
  import yappi
  yappi.start(True)
  #print "ready:", controller.ready()
  ##controller.clock.setMultiplicator(0.5)
  #controller.play()
  #import test
  #test.app = test.wx.App()
  #test.mframe = test.MyFrame()
  #test.mframe.Show()

  #import thread, time
  #thread.start_new_thread(test.app.MainLoop, ())
  #time.sleep(2)
  #controller.pause()
  
  #controller.clock.register(lambda x:e.videopanel.SetImage(controller.overlayedFrameAt(x, False, False, True)))