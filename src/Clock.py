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
    self.running = True
    self.registered = []
    self.multiplicator = 1

  def register(self, function):
    """register a funtion f to be called one every tick.
    f will get the current clock time as one float argument.
    e.g. f(2.3421)"""
    try:
        if(function is None):
            raise ClockError("error during appending function")
        else:
            self.registered.append(function)
    except ClockError as e:
        print "Caught: " + e.arg 

  def setMultiplicator(self, multi):
    """manipulates how much time of the clock passes within on interval.
       time of clock will be altered within one interval with value of
       interval * multi
    """
    if(multi != 0):
        self.multiplicator = multi
    return self.multiplicator

  def run(self): 
    """let the clock tick until end_of_time is reached"""    
    # while(!self.stop && <max_duration>)
    # sleep interval
    # clock seek to +interval * multi 
    while self.running and (clock < max_duration):
        time.sleep(self.interval)
        seek((self.interval + self.interval) * self.multiplicator)


  def stop(self): 
    """stop the clock at current time"""
    self.running = False

  def seek(self, second):
    """set current time of clock to second
    if second > end_of_time a ClockError will be raised"""
    # immer zeit ueber seek aendern
    # clock = second
    # registrierte funktionen hier aufrufen (ueber liste iterieren)
    try:
        self.clock = second
        for function in self.registered:
            function(self.clock)     
        raise ClockError("seek error")
    except ClockError as e:
        print "Caught: " + e.arg

class ClockError(Exception):
     def __init__(self, arg):
         self.arg = arg
  
class ClockWorker(threading.Thread, Clock):
    pass
    
    
worker = ClockWorker()
worker.start()
