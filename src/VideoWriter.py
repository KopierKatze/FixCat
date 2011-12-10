import cv

class VideoWriter(object):
  """creates a new video file where one can add frames to"""
  def __init__(self, file, width, height, fps, codec=None):
    """creates video file with the given properties.
    codec should be one of the codecs yielded by codecs().

    will raise error on file problems or invalid codecs.
    """
    if not file:
        raise WriterError("please select a valid file")
    if not codec:
        codec = CV_FOURCC('X', 'V', 'I', 'D')
    if not fps or fps < 1:
        raise WriterError("please set fps >= 1")
    if not widht or not height or widht < 1 or height <1:
        raise WriterError("please specify a valid height/width of your video")
      
    # windows_feature: codec aus dialog waehlen bei codec = -1 ???
    self.writer = cv.CreateVideoWriter(file, codec, fps, cv.Size(width, height), 1)

  def addFrame(self, new_frame):
    """add the IplImage new_frame to the end of the video file.

    what happens on full disk???"""
    if new_frame is None:
        raise WriterError("new frame may not be none")
    else:
        cv.WriteFrame(self.writer, new_frame)

  @classmethod
  def codecs(cls):
    """returns a dict that maps codec to human readable codec name"""
    # wie viele?? s. fourcc.org
    codec = dict([(('D', 'I', 'B') , 'uncompressed RGB'), 
        (('F', 'F', 'D', 'S') , 'ffdshow'), 
        (('X', 'V', 'I', 'D') , 'XVID Mpeg4'), 
        (('D', 'I', 'V', 'X') , 'DivX')])
    
  def releaseWriter(self):
    """closes VideoWriter after use """
    cv.ReleaseVideoWriter(writer)
    
class WriterError(Exception):
     def __init__(self, arg):
         self.arg = arg
