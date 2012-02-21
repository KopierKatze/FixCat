from Saveable import Saveable

import threading
from thread import start_new_thread
from time import time, sleep

class Clock(Saveable):
    """This class provides the methods for the Clock that runs in the background 
    of the tool. It plays a central role by defining the speed of playback and 
    keeping track of methods to be executed at each tick. 
    Methods can be registered via the `register()` method. This will cause the 
    registered methods to be performed at each tick. Registered methods can be
    informed about the current time in frame numbers.
    Playback speed - i.e. the time of passed within one interval - 
    can be manipulated with the `setMultiplicator()` method. 
    After the Clock is set to `run()`, it can `seek()` to different positions 
    within the video file by specifying the frame number you want it to be placed.
    If the Cloc has reached the end of the video, the `stop()` method will be 
    called. 
    
    As specified in the `run()` method, the Clock itself does not actually run 
    itself, but it creates a worker thread that will do the work instead. See 
    ClockWorker for more details."""
    
    def __init__(self, total_frames=None, fps=None, saved_state={}):
        """Creates a clock with a total amount of frames of the video, framerate 
        of the videoand, if existing, a saved state. The `saved_state` contains
        data about the frame that was displayed the last time you opened the project,
        the multiplicator that was set, the `fps` and total_frames."""
        assert not(total_frames is None and fps is None and saved_state == {})

        self._frame = saved_state.get('_frame', 0.0) # is not always a round number! do to the multiplicator
        self.running = False # initializing with False, True in run()
        self.registered = []
        self.multiplicator = saved_state.get('multiplicator', 1.0)
        self.total_frames = saved_state.get('total_frames', total_frames)
        try:
            self.interval = 1.0/saved_state.get('fps', fps)
        except ZeroDivisionError:
            self.interval = 1.0/30.0

    def getState(self):
        return {'_frame':self._frame, 'total_frames':self.total_frames, 'fps':1.0/self.interval, 'multiplicator': self.multiplicator}

    @property
    def frame(self):
        """Returns the frame number the Clock is currently at."""
        return int(round(self._frame))

    def register(self, function):
        """Registers a new funtion f to be called in every interval.
        f will get the current clock time as a float argument, e.g. f(2.3421)"""
        if(function is None):
            raise ClockError("Error during appending function. Function to be appended may not be null")
        else:
            self.registered.append(function)
 
    def setMultiplicator(self, multiplicator):
        """Manipulates how much time passes within one interval or tick.
        The length of an interval will be altered the following way:
        length of interval * `multiplicator` """
        if(multiplicator != 0.0):
            self.multiplicator = float(multiplicator)
        else:
            raise ClockError("Multiplicator may not be 0")

    def run(self): 
        """Runs the Clock by running the ClockWorker thread. The worker should only 
        be started, if the Clock itself is already running."""
        if self.running == False:
            self.running = True
            worker = ClockWorker(self)
            worker.start()
        else:
            raise ClockError("Clock already running")
        

    def stop(self): 
        """Stop the Clock at the current time. """
        if self.running == True:
            self.running = False
        else:
            raise ClockError("Clock already stopped")

    def seek(self, frame):
        """Set the Clock to `frame`, eg. for seeking in the player and for normal
        playback. See `run()` in ClockWorker. 
        If `frame` is higher than the total amount of frames, a ClockError will 
        be raised"""
        if self.frame == frame:
            # nothing to change so save cpu time
            return

        if frame < 0 or frame > self.total_frames:
            if self.running: self.stop()
            raise ClockError("Seek error: frame out of scope")

        self._frame = frame
        for function in self.registered:
            function(self.frame)

class ClockError(Exception):
    """This Error is thrown if
        - The function you tried to append in `Clock.register()` is None
        - The new multiplicator in `Clock.setMultiplicator()` is 0. 
        This value is intended to be greater than 0. 
        - The Clock is already running and `Clock.run()` is called again. This is not 
        allowed, since only one Clock and its ClockWorker are supposed to be 
        running at once.
        - The number of the frame passed to `Clock.seek()` is either 
        smaller than 0 or greater than the total number of frames of the video."""
    pass
    
class ClockWorker(threading.Thread):
    """This worker class is need for the actual work our Clock does. 
    It instantiates a Clock of the class above and then uses its methods in the
    `Clock.run()` method. The ClockWorker runs in its own thread, so it has to inherit
    from the threading module. 
    The running instance of a ClockWorker sleeps for a certain interval(depending
    on the multiplicator) and then increments the framecount.
    If the count of total_frames is smaller than the
    amount of frames in the video, the ClockWorker seeks to the 
    new frame, if total_frames is bigger, 
    the clock will seek to the highest frame number possible and then stop. 
    """
    def __init__(self, Clock):
        threading.Thread.__init__(self)
        # set to daemon otherwise we can't stop program if clock is running
        self.daemon = True
        self.c = Clock

    def run(self):
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
