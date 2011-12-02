import cv

class VideoReader(object):
  """provides a image-by-image access to a video file"""
  
  def __init__(self, filepath):
    """open the video file at filepath.
    will raise VideoOpenError on failure"""
    if filepath is not None:
        self.reader = cv.CaptureFromFile(filepath)
    

  def frameAt(self, second):
    """returns the image that you would see when playing the video at second
    'second'"""
    if second >= 0:
        cv.SetCaptureProperty(reader, cv.CV_CAP_PROP_POS_MSEC, second*1000)
        frame = cv.QueryFrame(reader) #IplImage 
    return frame

  def duration(self):
    """duration of the video in seconds"""
    self.duration = (long(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_POS_MSEC))) / 1000
    return self.duration

  def fps(self):
    self.framerate = int(cv.GetCaptureProperty(reader, cv.CV_CAP_PROP_FPS))
    return selfframerate    
  def releaseReader(self):
    """closes VideoReader after use """
    cv.ReleaseCapture(reader)
