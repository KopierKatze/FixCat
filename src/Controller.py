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

    self.clock = Clock(self.video_reader.duration(), 0.1)
    self.clock.register(self._tick)
    
    if self.categorise_frames:
      number_of_indexes = self.video_reader.fps() * self.video_reader.duration()
    else:
      number_of_indexes = self.eye_movement.countFixations()

    self.category_container = CategoryContainer(int(number_of_indexes))

    self.gui.newVideo(self.video_reader.duration())

  def _tick(self, time):
    """will populate current image to gui.
    have a look at Clock class for more information."""
    self.gui.setImageAndTime(self.overlayedFrameAt(False, False, True), time)

  def overlayedFrameAt(self, left, right, mean):
    second = self.clock.time
    
    image = self.video_reader.frameAt(second)
    left_look = self.eye_movement.leftLookAt(second)
    right_look = self.eye_movement.rightLookAt(second)
    mean_look = self.eye_movement.meanLookAt(second)
    left_cursor = self.cursor.cursorFor(self.eye_movement.statusLeftEyeAt(second))
    right_cursor = self.cursor.cursorFor(self.eye_movement.statusRightEyeAt(second))
    mean_cursor = self.cursor.cursorFor(self.eye_movement.meanStatusAt(second))
    
    if left and left_cursor:
      cv.SetImageROI(image, (int(left_look[0]), int(left_look[1]), left_cursor.width, left_cursor.height))
      cv.Add(image, left_cursor, image)
      
    if right and right_cursor:
      cv.SetImageROI(image, (int(right_look[0]), int(right_look[1]), right_cursor.width, right_cursor.height))
      cv.Add(image, right_cursor, image)

      
    if mean and mean_cursor:
      cv.SetImageROI(image, (int(mean_look[0]), int(mean_look[1]), mean_cursor.width, mean_cursor.height))
      cv.Add(image, mean_cursor, image)
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
    cur_frame = self.video_reader.frameNumberOfSecond(self.clock.time)
    print "current frame is:", cur_frame, "at:", self.clock.time
    try:
      nextFrameTime = self.video_reader.beginOfFrame(cur_frame + 1)
      print "jumped to:", nextFrameTime
    except ReaderError:
      """we are already at the end of the video"""
      pass
    else:
      self.seek(nextFrameTime)

  def prevFrame(self):
    """jump one frame into the past"""
    cur_frame = self.video_reader.frameNumberOfSecond(self.clock.time)
    try:
      prevFrameTime = self.video_reader.beginOfFrame(cur_frame - 1)
    except ReaderError:
      """we are already at the beginning of the video"""
      pass
    else:
      self.seek(prevFrameTime)

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
  controller.new_project("../example/t2d1gl_ett0.avi", "../example/t2d1gl.asc", True)
  
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