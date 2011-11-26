class VideoWriter(object):
  """creates a new video file where one can add frames to"""
  def __init__(self, file, width, height, fps, codec=None):
    """creates video file with the given properties.
    codec should be one of the codecs yielded by codecs().

    will raise error on file problems or invalid codecs.
    """
    raise NotImplementedError()

  def addFrame(self, new_frame):
    """add the IplImage new_frame to the end of the video file.

    what happens on full disk???"""
    raise NotImplementedError()

  @classmethod
  def codecs(cls):
    """returns a dict that maps codec to human readable codec name"""
    raise NotImplementedError()
