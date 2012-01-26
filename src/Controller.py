from CategoryContainer import CategoryContainer, CategoryContainerError
from Clock import Clock
from EyeMovement import EyeMovement
from VideoReader import VideoReader, ReaderError
from VideoWriter import VideoWriter
from Config import Config
from Savable import Savable, SaveController, SaveControllerError

try:
  from cv2 import cv
except ImportError:
  import cv

class Controller(Savable):
  """this class connects all the in- and output classes together and provides a
  clean interface for the connection to the gui"""
  def __init__(self, video_str, current_frame):
    self.video_reader = None
    self.eye_movement = None
    self.clock = None
    self.cursors = []
    self.category_container = None
    self.categorise_frames = False
    self.video_image = None
    self.show_eyes = [False, False, False] # [left_eye, right_eye, mean_eye]
    self.categorising_eye_is_left = None # True -> left, False -> right, None -> mean

    self.video_str = video_str
    self.current_frame = current_frame
    """contains the current image of the overlayed video.
    shared memory, so no latent ipc is needed"""

    self.config = Config()

  def leftEyeStatus(self, show):
    self.show_eyes[0] = bool(show)
    # reproduce the current image to show or exclude this eye
    self.produceCurrentImage()
  def rightEyeStatus(self, show):
    self.show_eyes[1] = bool(show)
    # reproduce the current image to show or exclude this eye
    self.produceCurrentImage()
  def meanEyeStatus(self, show):
    self.show_eyes[2] = bool(show)
    # reproduce the current image to show or exclude this eye
    self.produceCurrentImage()
  def getEyeStatus(self):
    return self.show_eyes

  def ready(self):
    """you should'nt always make sure this class is ready before using it's functions.
    ready means every data needed is available"""
    return bool(self.video_reader) and \
	   bool(self.eye_movement) and \
	   bool(self.clock) and \
	   bool(self.cursors) and \
	   bool(self.category_container)

  def createCursorDict(self):
    self.cursors = {None:None,
		    'fixated':self.config.get('cursors','fixated'),
		    'saccade':self.config.get('cursors','saccade'),
		    'blink':self.config.get('cursors','blink')}

  def new_project(self, video_file, eye_movement_file, categorise_frames=False):
    """create a new project.
    you can decide whether you want to categorise frames or fixations by the 'categorise_frames' flag.
    """
    self.createCursorDict()

    self.categorise_frames = categorise_frames
    self.eye_movement = EyeMovement(eye_movement_file)
    self.video_reader = VideoReader(video_file)

    self.clock = Clock(self.video_reader.duration, self.video_reader.fps)
    self.clock.register(self._clock_tick)

    if self.categorise_frames:
      objects = {}
      for frame in xrange(int(self.video_reader.frame_count)):
        objects[(frame, frame)] = str(frame)
    else:
      objects = self.eye_movement.fixations(self.categorising_eye_is_left)

    self.category_container = CategoryContainer(objects)

    self.show_eyes = [False, False, True] # show mean eye

    # seek to zero so we'll have a picture
    self.produceCurrentImage()

  def save_project(self, saved_filepath):
    sc = SaveController()

    sc.addSavable('eye_movement', self.eye_movement)
    sc.addSavable('category_container', self.category_container)
    sc.addSavable('video_reader', self.video_reader)
    sc.addSavable('clock', self.clock)
    sc.addSavable('controller', self)

    sc.saveToFile(saved_filepath)

  def load_project(self, saved_filepath):
    sc = SaveController()

    sc.loadFromFile(saved_filepath)

    self.createCursorDict()
    controller_state = sc.getSavedState('controller')
    self.show_eyes = controller_state['show_eyes']
    self.categorise_frames = controller_state['categorise_frames']

    self.eye_movement = EyeMovement(saved_state=sc.getSavedState('eye_movement'))
    self.video_reader = VideoReader(saved_state=sc.getSavedState('video_reader'))
    self.clock = Clock(saved_state=sc.getSavedState('clock'))
    self.clock.register(self._clock_tick)
    self.category_container = CategoryContainer(saved_state=sc.getSavedState('category_container'))
    
    self.produceCurrentImage()

  def getState(self):
    return {'show_eyes':self.show_eyes, 'categorise_frames':self.categorise_frames}

  def _clock_tick(self, frame):
    self.produceCurrentImage()

  def produceCurrentImage(self):
    """will populate current image to gui.
    have a look at Clock class for more information."""
    frame = self.clock.frame
    fr = self.overlayedFrame(frame, self.show_eyes[0], self.show_eyes[1], self.show_eyes[2])
    return_frame = cv.CreateImage((self.video_reader.width, self.video_reader.height), cv.IPL_DEPTH_8U, 3)
    cv.Copy(fr, return_frame)
    cv.CvtColor(return_frame, return_frame, cv.CV_BGR2RGB)
    self.video_image = return_frame
    self.current_frame.value = frame
    video_str = return_frame.tostring()
    self.video_str.value = video_str

  def categorise(self, shortcut):
    try:
      return self.category_container.categorise(self.clock.frame, shortcut)
    except CategoryContainerError:
      raise
      return False

  def getCategorisations(self):
    return self.category_container.dictOfCategorisations()

  def getCategorisationsOrder(self):
    return self.category_container.start_end_frames

  def exportCategorisations(self, filepath):
    self.category_container.export(filepath)

  def getCategories(self):
    return self.category_container.categories

  def overlayedFrame(self, frame, left, right, mean):
    # retrieve original image from video file
    image = self.video_reader.frame(frame)
    # add cursors as neede
    if left:
      self._addCursorToImage(image, self.cursors[self.eye_movement.statusLeftEyeAt(frame)], self.eye_movement.leftLookAt(frame))
    if right:
      self._addCursorToImage(image, self.cursors[self.eye_movement.statusRightEyeAt(frame)], self.eye_movement.rightLookAt(frame))
    if mean:
      self._addCursorToImage(image, self.cursors[self.eye_movement.meanStatusAt(frame)], self.eye_movement.meanLookAt(frame))

    return image

  def _addCursorToImage(self, image, cursor, position):
    # in case that we don't have information about the position or cursor end now
    if position is None or cursor is None: return

    cursor_left_upper_corner = (int(position[0]-cursor.width/2), int(position[1]-cursor.height/2))
    cursor_right_lower_corner = (cursor_left_upper_corner[0]+cursor.width, cursor_left_upper_corner[1]+cursor.height)
    cursorROI = [0, 0, cursor.width, cursor.height]
    imageROI = [cursor_left_upper_corner[0], cursor_left_upper_corner[1], cursor.width, cursor.height]
    if cursor_right_lower_corner[0] <= 0 or cursor_right_lower_corner[1] < 0 or \
     cursor_left_upper_corner[0] > image.width or cursor_left_upper_corner[1] > image.height:
      # cursor out of image
      return
    if cursor_left_upper_corner[0] < 0:
      cursorROI[0] = - cursor_left_upper_corner[0]
      imageROI[0] = 0
    if cursor_left_upper_corner[1] < 0:
      cursorROI[1] = - cursor_left_upper_corner[1]
      imageROI[1] = 0
    if cursor_right_lower_corner[0] > image.width:
      cursorROI[2] = cursor.width - (cursor_right_lower_corner[0] - image.width)
      if cursorROI[2] == 0: return # width of cursor would be zero
      imageROI[2] = image.width
    if cursor_right_lower_corner[1] > image.height:
      cursorROI[3] = cursor.height - (cursor_right_lower_corner[1] - image.height)
      if cursorROI[3] == 0: return # height of cursor would be zero
      imageROI[3] = image.height

    cv.SetImageROI(cursor, tuple(cursorROI))
    cv.SetImageROI(image, tuple(imageROI))
    cv.Add(image, cursor, image)
    cv.ResetImageROI(image)

  def exportVideo(self, output_file):
    """ export the overlayed video to a new video file with the VideoWriter"""
    # TODO: add codec support for this 
    self.seek(0)
    frame_size = (self.getVideoWidth(), self.getVideoHeight())
    vidfps = self.video_reader.fps
    codec = cv.CV_FOURCC('D','I','V','X')
    self.video_writer = VideoWriter(output_file, frame_size, vidfps, codec)

    for frame in xrange(self.video_reader.frame_count):
      self.seek(frame)
      self.video_writer.addFrame(self.video_image)
    self.video_writer.releaseWriter()

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
    frame = self.eye_movement.nextNotCategorisedIndex(self.clock.frame)
    self.seek(frame)
  
  def nextFixation(self):
    '''jump to next fixation'''
    frame = self.eye_movement.nextFixationFrame(self.clock.frame, self.categorising_eye_is_left)
    self.seek(frame)

  def prevFixation(self):
    '''jump to prev fixation'''
    frame = self.eye_movement.prevFixationFrame(self.clock.frame, self.categorising_eye_is_left)
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
  def getVideoFrameRate(self):
    return self.video_reader.fps
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
