import cv

class VideoReader(object):
    """provides a image-by-image access to a video file"""
  
    def __init__(self, filepath):
        """open the video file at filepath.
        will raise VideoOpenError on failure"""

        if filepath is not None and filepath is not '':
            self.reader = cv.CaptureFromFile(filepath)
            
            self.total_frames = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT)
            self.fps = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FPS)
            self.duration = self.total_frames * self.fps
        else:
            raise ReaderError('invalid filepath')

    def frame(self, frame_number):
        """returns the image that you would see when playing the video at second
        'second'"""
        if frame_number is not None and frame_number >= 0 and frame_number <= self.total_frames: 
            cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES, frame_number)
            frame = cv.QueryFrame(self.reader) #IplImage
            return_frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 3)
            cv.Copy(frame, return_frame)
            return return_frame
        else:
            return ReaderError("second should be between")

    def releaseReader(self):
        """closes VideoReader after use """
        cv.ReleaseCapture(reader)

class ReaderError(Exception):
    pass
