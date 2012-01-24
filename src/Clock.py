from Savable import Savable

import threading
from thread import start_new_thread
from time import time, sleep

class Clock(Savable):
  """a clock!
     ticks in a specific interval. will call functions registered with
     'register()' on every tick. informs those funtions about current time
     in seconds.
     the time passed within one interval can be altered by a multiplicator."""
  def __init__(self, total_frames=None, fps=None, saved_state={}):
    """creates clock with interval(time in the real world that passes between
    two ticks) and end_of_time(duration of video)"""
    assert not(total_frames is None and fps is None and saved_state == {})

    self._frame = saved_state.get('_frame', 0.0) # is not always a round number! do to the multiplicator
    self.running = False # initializing with False, True in run()
    self.registered = []
    self.multiplicator = saved_state.get('multiplocator', 1.0)
    self.total_frames = saved_state.get('total_frames', total_frames)
    try:
      self.interval = 1.0/saved_state.get('fps', fps)
    except ZeroDivisionError:
      self.interval = 1.0/30.0

  def getState(self):
    return {'_frame':self._frame, 'total_frames':self.total_frames, 'fps':1.0/self.interval, 'multiplicator': self.multiplicator}

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

    if self.frame == frame:
      # nothing to change so save cpu time
      return

    if frame < 0 or frame > self.total_frames:
      self.stop()
      raise ClockError("seek error: frame out of scope")

    self._frame = frame
    for function in self.registered:
	#thread = threading.Thread()
	#thread.run = lambda: function(self.frame)
	#thread.daemon = True
	#thread.start()
	function(self.frame)

class ClockError(Exception):
    pass

import cProfile
    
class ClockWorker(threading.Thread):
    def __init__(self, Clock):
        threading.Thread.__init__(self)
        # set to daemon otherwise we can't stop program if clock is running
        self.daemon = True
        self.c = Clock

    def run(self):
      prof = cProfile.Profile()
      prof.runctx('l()', {}, {'l':self.run1})
      prof.print_stats('time')

    def run1(self):
        target = self.c.interval
        actual = self.c.interval
        sleeptime = self.c.interval
        while self.c.running:
	    temptime = time()
	    sleeptime = 0.8 * sleeptime + 0.2 * (target - actual)
	    if sleeptime > 0.00001: sleep(sleeptime)
	    else: sleep(0.00001)
            new_frame = self.c._frame + (1.0 * self.c.multiplicator)
            if round(new_frame) > self.c.total_frames:
	      self.c.seek(self.c.total_frames)
	      self.c.stop()
	    else:
	      self.c.seek(new_frame)
	    actual = time() - temptime
	    #print int(actual/target*100), sleeptime
