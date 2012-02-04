from Savable import Savable

from threading import Thread
from time import sleep, time
import os.path
try:
  from cv2 import cv
except ImportError:
  import cv

class VideoReader(Savable):
    """provides a image-by-image access to a video file"""

    def __init__(self, filepath=None, saved_state={}):
        """open the video file at filepath.
        will raise VideoOpenError on failure"""

        if saved_state=={} and (filepath is None or filepath == ''): raise ReaderError('Es wurde keine Videodatei ausgewaehlt.')
        if saved_state and not filepath is None: raise ReaderError('Es ist bereits ein Dateiname fuer die Videodatei ausgewaehlt.')
        self.filepath = saved_state.get('filepath', filepath)

	if not os.path.isfile(self.filepath): raise ReaderError('Die angegebene Videodatei existiert nicht.')
	if not os.access(self.filepath, os.R_OK): raise ReaderError('Auf die Videodatei kann nicht zugegriffen werden (keine Leseberechtigung).')
	self.reader = cv.CaptureFromFile(self.filepath)
	# have to check if codec is available!
	test_frame = cv.QueryFrame(self.reader)
	if test_frame is None or test_frame.width == 0 or test_frame.height == 0:
	  raise ReaderError('Konnte Video nicht oeffnen. Codec nicht vorhanden oder Video defekt.')
	self.height = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_HEIGHT))
	self.width = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_WIDTH))
	self.frame_count = self._determine_frame_count()
	self.fps = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FPS)
	self.duration = self.frame_count * self.fps
	
    def getState(self):
      return {'filepath':self.filepath}

    def _determine_frame_count(self):
      current_frame = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT))
      captured_frame = False
      while not captured_frame:
        try:
          self.frame(current_frame)
        except ReaderError:
          current_frame -= 1
        else:
          captured_frame = True
      exception_raised = False
      while not exception_raised:
        try:
          self.frame(current_frame+1)
        except ReaderError:
          exception_raised = True
        else:
          current_frame += 1
      return current_frame
      
    def frame(self, frame_number):
        """returns the image that you would see when playing the video at second
        'second'"""
        if frame_number is not None and frame_number >= 0 and (not hasattr(self, "frame_count") or frame_number <= self.frame_count):
          cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES, frame_number)
          frame = cv.QueryFrame(self.reader) #IplImage
	  return_frame = cv.CreateImage((self.width, self.height), cv.IPL_DEPTH_8U, 3)
          try:
            cv.Copy(frame, return_frame)
          except (TypeError, cv.error):
            """copy will fail if no video frame was delivered by queryframe"""
            raise ReaderError("Es ist ein Problem beim lesen eines Videoframes aufgetreten!")
	  return return_frame
        else:
          return ReaderError("Die Nummer des Frames muss zwischen 0 und der Gesamtzahl von Frames liegen.")

    def releaseReader(self):
        """closes VideoReader after use """
        cv.ReleaseCapture(reader)

class ReaderError(Exception):
    pass
