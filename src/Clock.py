import threading
import time #for sleeping

class Clock(object):
  """a clock!
     ticks in a specific interval. will call functions registered with
     'register()' on every tick. informs those funtions about current time
     in seconds.
     the time passed within one interval can be altered by a multiplicator."""
  def __init__(self, maximal_duration, interval = 1.0/30):
    """creates clock with interval(time in the real world that passes between
    two ticks) and end_of_time(duration of video)"""
    
    self.clock = 0.0
    self.running = False # initializing with False, True in run()
    self.registered = []
    self.multiplicator = 1
    self.maximal_duration = maximal_duration
    self.interval = interval

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
        self.multiplicator = multi
        return self.multiplicator
    else:
        raise ClockError("multiplicator may not be 0")
        return 1

  def run(self): 
    """let the clock tick until end_of_time is reached"""    
    # while(!self.stop && <max_duration>)
    # sleep interval
    # clock seek to +interval * multi 
    if self.running == False:
        self.running = True
    else:
        raise ClockError("clock already running")
        
    while self.running and self.clock <= self.maximal_duration - self.interval:
        time.sleep(self.interval)
        self.seek((self.clock + self.interval) * self.multiplicator)
    if self.clock > self.maximal_duration:
        raise ClockError("running for too long")

  def stop(self): 
    """stop the clock at current time"""
    if self.running == True:
        self.running = False
    else:
        raise ClockError("clock already stopped")

  def seek(self, second):
    """set current time of clock to second
    if second > end_of_time a ClockError will be raised"""
    # immer zeit ueber seek aendern
    # clock = second
    # registrierte funktionen hier aufrufen (ueber liste iterieren)
    if second < 0 or second > self.maximal_duration:
        self.stop()
        raise ClockError("seek error")
    self.clock = second
    for function in self.registered:
        function(self.clock)     

class ClockError(Exception):
     def __init__(self, arg):
         self.arg = arg
  
class ClockWorker(threading.Thread, Clock):
    pass
    
    
worker = ClockWorker()
worker.start()
