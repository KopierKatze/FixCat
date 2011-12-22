import threading
from thread import start_new_thread
import time #for sleeping

class Clock(object):
  """a clock!
     ticks in a specific interval. will call functions registered with
     'register()' on every tick. informs those funtions about current time
     in seconds.
     the time passed within one interval can be altered by a multiplicator."""
  def __init__(self, total_frames, fps):
    """creates clock with interval(time in the real world that passes between
    two ticks) and end_of_time(duration of video)"""
    
    self._frame = 0.0 # is not always a round number! do to the multiplicator
    self.running = False # initializing with False, True in run()
    self.registered = []
    self.multiplicator = 1.0
    self.total_frames = total_frames
    self.interval = 1.0/fps

  @property
  def frame(self):
    return int(round(self._frame))

  def register(self, function):
    """register a funtion f to be called one every tick.
    f will get the current clock time as one float argument.
    e.g. f(2.3421)"""
    if(function is None):
        raise ClockError("error during appending function. function may not be null")
    else:
        self.registered.append(function)
 
  def setMultiplicator(self, multi):
    """manipulates how much time of the clock passes within on interval.
       time of clock will be altered within one interval with value of
       interval * multi
    """
    if(multi != 0):
        self.multiplicator = float(multi)
    else:
        raise ClockError("multiplicator may not be 0")

  def run(self): 
    """let the clock tick until end_of_time is reached"""
    if self.running == False:
        self.running = True
        worker = ClockWorker(self)
        worker.start()
    else:
        raise ClockError("clock already running")
        

  def stop(self): 
    """stop the clock at current time"""
    if self.running == True:
        self.running = False
    else:
        raise ClockError("clock already stopped")

  def seek(self, frame):
    """set current time of clock to frame
    if frame > end_of_time a ClockError will be raised"""
    # immer zeit ueber seek aendern
    # registrierte funktionen hier aufrufen (ueber liste iterieren)
    if frame < 0 or frame > self.total_frames:
        self.stop()
        raise ClockError("seek error: frame out of scope")
    self._frame = frame
    for function in self.registered:
	thread = threading.Thread()
	thread.run = lambda: function(self.frame)
	thread.daemon = True
	thread.start()
	#function(self.frame)

class ClockError(Exception):
    pass
  
class ClockWorker(threading.Thread):
    def __init__(self, Clock):
        threading.Thread.__init__(self)
        # set to daemon otherwise we can't stop program if clock is running
        self.daemon = True
        self.c = Clock

    def run(self):
        while self.c.running:
            time.sleep(self.c.interval)
            new_frame = self.c._frame + (1.0 * self.c.multiplicator)
            if round(new_frame) > self.c.total_frames:
	      self.c.seek(self.c.total_frames)
	      self.c.stop()
	    else:
	      self.c.seek(new_frame)
