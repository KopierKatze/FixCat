try:
  from cv2 import cv
except ImportError:
  import cv

class VideoWriter(object):
  """creates a new video file where one can add frames to"""
  def __init__(self, filepath, size, fps, codec=None):
    """creates video file with the given properties.
    codec should be one of the codecs yielded by codecs().

    will raise error on file problems or invalid codecs.
    """
    self.size = size
    self.width = size[0]
    self.height = size[1]
    if filepath is None:
        raise WriterError("please select a valid file")
    if codec is None:
        codec = cv.CV_FOURCC('X', 'V', 'I', 'D')
    if fps is None or fps < 1:
        raise WriterError("please set fps >= 1")
    if self.width is None or self.height is None or self.width < 1 or self.height <1:
        raise WriterError("please specify a valid height/width of your video")
      
    # windows_feature: codec aus dialog waehlen bei codec = -1 ???
    self.writer = cv.CreateVideoWriter(filepath, codec, fps, (size), 1)
    #self.current_frame = 0;
    
  def addFrame(self, new_frame):
    """add the IplImage new_frame to the end of the video file.

    what happens on full disk???"""
    if new_frame is None:
        raise WriterError("new frame may not be none")
    else:
	cv.CvtColor(new_frame, new_frame, cv.CV_BGR2RGB)
        cv.WriteFrame(self.writer, new_frame)

  @classmethod
  def codecs(cls):
    """returns a dict that maps codec to human readable codec name"""
    # wie viele?? s. fourcc.org
    codec = dict([(CV_FOURCC('D', 'I', 'B') , 'uncompressed RGB'), 
        (CV_FOURCC('F', 'F', 'D', 'S') , 'ffdshow'), 
        (CV_FOURCC('X', 'V', 'I', 'D') , 'XVID Mpeg4'), 
        (CV_FOURCC('D', 'I', 'V', 'X') , 'DivX')])
    
  def releaseWriter(self):
    """closes VideoWriter after use """ 
    del self.writer
    
class WriterError(Exception):
    pass
