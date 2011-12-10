from CategoryContainer import CategoryContainer
from Clock import Clock
from Cursor import Cursor
from EyeMovement import EyeMovement
from VideoReader import VideoReader
from VideoWriter import VideoWriter

import cv

class Controller(object):
  def __init__(self):
    self.video_reader = None
    self.eye_movement = None
    self.clock = None
    self.cursor = None
    self.category_container = None
    self.categorise_frames = False

  def ready(self):
    return bool(self.video_reader) and \
	   bool(self.eye_movement) and \
	   bool(self.clock) and \
	   bool(self.cursor) and \
	   bool(self.category_container)

  def _new_project(self, video_file, eye_movement_file, categorise_frames=False):
    self.cursor = Cursor()
    
    self.categorise_frames = categorise_frames
    self.eye_movement = EyeMovement(eye_movement_file)
    self.video_reader = VideoReader(video_file)

    self.clock = Clock(self.video_reader.duration(), 0.2)
    self.clock.register(self._tick)
    
    if self.categorise_frames:
      number_of_indexes = self.video_reader.fps() * self.video_reader.duration()
    else:
      number_of_indexes = self.eye_movement.countFixations()

    self.category_container = CategoryContainer(int(number_of_indexes))

  def _tick(self, time):
    global test
    
    test.picture = self.overlayedFrameAt(time, False, False, True)

  def overlayedFrameAt(self, second, left, right, mean):
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

if __name__ == '__main__':
  controller = Controller()
  controller._new_project("../example/t2d1gl_ett0.avi", "../example/t2d1gl.asc", True)
  print "ready:", controller.ready()
  controller.clock.setMultiplicator(0.5)
  controller.play()
  import test
  test.app = test.wx.App()
  test.mframe = test.MyFrame()
  test.mframe.Show()

  import thread
  thread.start_new_thread(test.app.MainLoop, ())
  time.sleep(2)
  controller.pause()
  