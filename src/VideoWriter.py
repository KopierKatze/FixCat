import cv

class VideoWriter(object):
  """creates a new video file where one can add frames to"""
  def __init__(self, file, width, height, fps, codec=None):
    """creates video file with the given properties.
    codec should be one of the codecs yielded by codecs().

    will raise error on file problems or invalid codecs.
    """
    # windows_feature: codec aus dialog waehlen bei codec = -1. wie verfahren???
    writer = cv.CreateVideoWriter(file, 0, fps, cv.Size(width, height), 1) # uncompressed avi

  def addFrame(self, new_frame):
    """add the IplImage new_frame to the end of the video file.

    what happens on full disk???"""
    cr.WriteFrame(writer, new_frame)

  @classmethod
  def codecs(cls):
    """returns a dict that maps codec to human readable codec name"""
    # wie viele?? s. fourcc.org
    codec = dict([('DIB' , 'uncompressed RGB'), ('FFDS' , 'ffdshow'), ('XVID' , 'XVID Mpeg4'), ('DIVX' , 'DivX')])
    
  def releaseWriter(self):
  """closes VideoWriter after use """
    cv.ReleaseVideoWriter(writer)
