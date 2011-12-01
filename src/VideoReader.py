import cv

class VideoReader(object):
  """provides a image-by-image access to a video file"""
  
  def __init__(self, filepath):
    """open the video file at filepath.
    will raise VideoOpenError on failure"""
    reader = cv.CaptureFromFile(filepath)
    

  def frameAt(self, second):
    """returns the image that you would see when playing the video at second
    'second'"""
    
    cv.SetCaptureProperty(reader, cv.CV_CAP_PROP_POS_MSEC, second*1000)
    frame = cv.QueryFrame(reader) #IplImage 
    return frame

  def duration(self):
    """duration of the video in seconds"""
    duration = (long(cv.GetCaptureProperty(video, cv.CV_CAP_PROP_POS_MSEC))) / 1000
    return duration

  def fps(self):
    framerate = int(cv.GetCaptureProperty(reader, cv.CV_CAP_PROP_FPS))
    return framerate    
  def releaseReader(self):
    """closes VideoReader after use """
    cv.ReleaseCapture(reader)
