class Clock(object):
  """a clock!
     ticks in a specific interval. will call functions registered with
     'register()' on every tick. informs those funtions about current time
     in seconds.
     the time passed within one interval can be altered by a multiplicator."""
  def __init__(self, interval = 1.0/30):
    """creates clock with interval(time in the real world that passes between
    two ticks) and end_of_time(duration of video)"""
    raise NotImplementedError()

  def register(self, function):
    """register a funtion f to be called one every tick.
    f will get the current clock time as one float argument.
    e.g. f(2.3421)"""
    raise NotImplementedError()

  def setMultiplicator(self, multi):
    """manipulates how much time of the clock passes within on interval.
       time of clock will be altered within one interval with value of
       interval * multi
    """
    raise NotImplementedError()

  def run(self):
    """let the clock tick until end_of_time is reaced"""
    raise NotImplementedError()

  def stop(self):
    """stop the clock at current time"""
    raise NotImplementedError()

  def seek(self, second):
    """set current time of clock to second
    if second > end_of_time a ClockError will be raised"""
    raise NotImplementedError()

class ClockError(Exception):
  pass