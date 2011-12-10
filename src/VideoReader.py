import cv

class VideoReader(object):
    """provides a image-by-image access to a video file"""
  
    def __init__(self, filepath):
        """open the video file at filepath.
        will raise VideoOpenError on failure"""

        if filepath is not None and filepath is not '':
            self.reader = cv.CaptureFromFile(filepath)
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
            #second = 1 <-- for fault tolerance?!
            #cv.SetCaptureProperty(reader, cv.CV_CAP_PROP_POS_MSEC, second*1000)
            #frame = cv.QueryFrame(reader)
            return ReaderError("second should be between")


    def duration(self):
        """duration of the video in seconds"""
        if self.reader is not None: # should be reader ok??
            framecount = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT)
            duration = framecount / self.fps()
            return duration
        else: 
            return ReaderError("invalid video reader")

    def fps(self):
        if self.reader is not None: # should be reader ok??
            framerate = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FPS)
            return framerate
        else:
            return ReaderError("invalid video reader")
        
    def releaseReader(self):
        """closes VideoReader after use """
        cv.ReleaseCapture(reader)
    
class ReaderError(Exception):
    pass
