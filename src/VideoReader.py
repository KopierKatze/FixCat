class VideoReader(object):
  """provides a image-by-image access to a video file"""
  def __init__(self, filepath):
    """open the video file at filepath.
    will raise VideoOpenError on failure"""
    raise NotImplementedError()

  def frameAt(self, second):
    """returns the image that you would see when playing the video at second
    'second'"""
    raise NotImplementedError()

  def duration(self):
    """duration of the video in seconds"""
    raise NotImplementedError()

  def fps(self):
    raise NotImplementedError()
