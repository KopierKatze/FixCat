from CategoryContainer import CategoryContainer
from Clock import Clock
from Cursor import Cursor
from EyeMovement import EyeMovement
from VideoReader import VideoReader, ReaderError
from VideoWriter import VideoWriter
from Config import Config

try:
  from cv2 import cv
except ImportError:
  import cv

class Controller(object):
  """this class connects all the in- and output classes together and provides a
  clean interface for the connection to the gui"""
  def __init__(self, video_str, current_frame):
    self.video_reader = None
    self.eye_movement = None
    self.clock = None
    self.cursor = None
    self.category_container = None
    self.categorise_frames = False

    self.show_eyes = [False, False, False] # [left_eye, right_eye, mean_eye]

    self.video_str = video_str
    self.current_frame = current_frame
    """contains the current image of the overlayed video.
    shared memory, so no latent ipc is needed"""

    self.config = Config()

  def leftEyeStatus(self, show):
    self.show_eyes[0] = bool(show)
    # reproduce the current image to show or exclude this eye
    self._tick(self.clock.frame)
  def rightEyeStatus(self, show):
    self.show_eyes[1] = bool(show)
    # reproduce the current image to show or exclude this eye
    self._tick(self.clock.frame)
  def meanEyeStatus(self, show):
    self.show_eyes[2] = bool(show)
    # reproduce the current image to show or exclude this eye
    self._tick(self.clock.frame)
  def getEyeStatus(self):
    return self.show_eyes

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
      objects = {}
      for frame in xrange(int(self.video_reader.frame_count)):
        objects[(frame, frame)] = str(frame)
    else:
      objects = self.eye_movement.fixations(None)

    self.category_container = CategoryContainer(objects)

    self.show_eyes = [False, False, True] # show mean eye

  def _tick(self, frame):
    """will populate current image to gui.
    have a look at Clock class for more information."""
    fr = self.overlayedFrame(frame, self.show_eyes[0], self.show_eyes[1], self.show_eyes[2])
    return_frame = cv.CreateImage((self.video_reader.width, self.video_reader.height), cv.IPL_DEPTH_8U, 3)
    cv.Copy(fr, return_frame)
    cv.CvtColor(return_frame, return_frame, cv.CV_BGR2RGB)
    video_str = return_frame.tostring()
    self.current_frame.value = frame
    self.video_str.value = video_str

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

    cv.ResetImageROI(image)
    return image

  def play(self):
    if not self.clock.running: self.clock.run()

  def pause(self):
    if self.clock.running: self.clock.stop()

  def seek(self, frame):
    self.clock.seek(frame)
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
  
  def nextFixation(self):
    '''jump to next fixation'''
    frame = self.eye_movement.nextFixationFrame(self.clock.frame, None)
    self.seek(frame)

  def prevFixation(self):
    '''jump to prev fixation'''
    frame = self.eye_movement.prevFixationFrame(self.clock.frame, None)
    self.seek(frame)
# --------------- PLAYBACK SPEED -----
  def slowerPlayback(self):
    self.clock.setMultiplicator(self.clock.multiplicator * 0.9)
  def normalPlayback(self):
    self.clock.setMultiplicator(1.0)
  def fasterPlayback(self):
    self.clock.setMultiplicator(self.clock.multiplicator * 1.1)
# --------------- VIDEO INFORMATION -----
  def getVideoStrLength(self):
    return len(self.video_reader.frame(0).tostring())
  def getVideoHeight(self):
    return self.video_reader.height
  def getVideoWidth(self):
    return self.video_reader.width
  def getVideoFrameCount(self):
    return self.video_reader.frame_count

  def getFix(self):
    return self.eye_movement.fixations(None)

if __name__ == '__main__':
  from multiprocessing import Process, Value

  video_str = Value('c' '')

  from gui.MainFrame import MainFrame
  import wx
  a = wx.App()
  e = MainFrame(video_str)
  e.Show()
  gui_process = Process()
  gui_process.run = a.MainLoop
  gui_process.start()


  from thread import start_new_thread
  #start_new_thread(a.MainLoop, ())
  import cProfile
  controller = Controller(video_str)
  #controller.new_project("../example/t2d1gl_ett0.avi", "../example/t2d1gl.asc", True)
  controller.new_project("../example/overlayed_video.avi", "../example/t2d1gl.asc", True)
  #prof = cProfile.Profile()
  #prof.runctx('l()', {}, {'l':a.MainLoop})
  #prof.print_stats('time')
