from Savable import Savable

from threading import Thread
from time import sleep, time
try:
  from cv2 import cv
except ImportError:
  import cv

class VideoReader(Savable):
    """provides a image-by-image access to a video file"""

    def __init__(self, filepath=None, saved_state={}):
        """open the video file at filepath.
        will raise VideoOpenError on failure"""
        self.filepath = saved_state.get('filepath', filepath)

	self.reader = cv.CaptureFromFile(self.filepath)
	# have to check if codec is available!
	test_frame = cv.QueryFrame(self.reader)
	print dir(test_frame)
	if test_frame is None or test_frame.width == 0 or test_frame.height == 0:
	  raise ReaderError('Konnte Video nicht oeffnen. Codec nicht vorhanden oder Video defekt.')
	self.frame_count = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT))
	self.fps = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FPS)
	self.duration = self.frame_count * self.fps
	self.height = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_HEIGHT))
	self.width = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_WIDTH))
    def getState(self):
      return {'filepath':self.filepath}

    def frame(self, frame_number):
        """returns the image that you would see when playing the video at second
        'second'"""
        if frame_number is not None and frame_number >= 0 and frame_number <= self.frame_count:
          cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES, frame_number)
          frame = cv.QueryFrame(self.reader) #IplImage
	  return_frame = cv.CreateImage((self.width, self.height), cv.IPL_DEPTH_8U, 3)
	  cv.Copy(frame, return_frame)
	  return return_frame
        else:
          return ReaderError("second should be between")

    def releaseReader(self):
        """closes VideoReader after use """
        cv.ReleaseCapture(reader)

class ReaderError(Exception):
    pass