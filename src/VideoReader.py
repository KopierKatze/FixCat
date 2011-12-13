import cv

class VideoReader(object):
    """provides a image-by-image access to a video file"""
  
    def __init__(self, filepath):
        """open the video file at filepath.
        will raise VideoOpenError on failure"""

        if filepath is not None and filepath is not '':
            self.reader = cv.CaptureFromFile(filepath)
            
            frames = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT)
            cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES, frames-1)
            # have to query frame to settle position
            cv.QueryFrame(self.reader)
            self._duration = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_MSEC)
            print self._duration
        else:
            raise ReaderError('invalid filepath')

    def frameAt(self, second):
        """returns the image that you would see when playing the video at second
        'second'"""
        duration = self.duration()
        if second is not None and second >= 0 and second <= duration: 
            cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_MSEC, second*1000)
            frame = cv.QueryFrame(self.reader) #IplImage 
            return frame
        else:
            return ReaderError("second should be between")


    def duration(self):
        """duration of the video in seconds"""
        return self._duration

        framecount = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT)
        duration = framecount / self.fps()
        return duration

    def fps(self):
	framerate = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FPS)
	return framerate

    def frameNumberOfSecond(self, second):
      duration = self.duration()
      if second is not None and second >= 0 and second <= duration:
	cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_MSEC, second*1000)
	return int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES))
      else:
	return ReaderError("second should be between")

    def beginOfFrame(self, number):
      """returns the second from which on the frame is seen in the video"""
      cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES, number)
      return cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_MSEC)

    def releaseReader(self):
        """closes VideoReader after use """
        cv.ReleaseCapture(reader)

class ReaderError(Exception):
    pass
