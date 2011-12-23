from threading import Thread
from time import sleep, time
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
            self.cache = dict() # maps frame number to frame ressource
            self._last_frame = 0
            self.prefetcher = VideoPrefetcher(self)
            self.prefetcher.daemon = True
            self.prefetcher.start()
        else:
            raise ReaderError('invalid filepath')

    def frame(self, frame_number):
        """returns the image that you would see when playing the video at second
        'second'"""
        if frame_number is not None and frame_number >= 0 and frame_number <= self.total_frames:
	  self._last_frame = frame_number
	  if self.cache.has_key(frame_number):
	    print "cache hit!"
	    frame = self.cache.get(frame_number)
	  else:
	    print "cache miss"
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

class VideoPrefetcher(Thread):
  def __init__(self, video_reader, prefetch_deep=120):
    Thread.__init__(self)
    self.video_reader = video_reader
    self.prefetch_deep = prefetch_deep

  def run(self):
    cv_reader = self.video_reader.reader

    last_prefetched_frame = 0

    while True:
      sleep(0.3)
      if self.video_reader._last_frame <= last_prefetched_frame - 40: continue
      print "preloading...."
      tstart = time()
      for i in xrange(self.prefetch_deep):
	sleep(1.0/60.0)
	frame_number = int(cv.GetCaptureProperty(cv_reader, cv.CV_CAP_PROP_POS_FRAMES))
	frame = cv.QueryFrame(cv_reader)
	return_frame = cv.CreateImage((frame.width, frame.height), cv.IPL_DEPTH_8U, 3)
	cv.Copy(frame, return_frame)
	# now add to cache
	self.video_reader.cache.update([(frame_number, return_frame)])
	# increase prefetch counter
	last_prefetched_frame = frame_number
      print "loading finished in %f seconds, now purging old frames" % (time() - tstart)
      tstart = time()
      for i in self.video_reader.cache.keys():
	if i < self.video_reader._last_frame:
	  del self.video_reader.cache[i]
      print "purging finished in %f seconds, now sleeping until needed again" %(time() - tstart)