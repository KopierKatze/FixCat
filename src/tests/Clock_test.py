from Clock import Clock, ClockError, ClockWorker
import nose

@nose.tools.raises(ClockError)
def end_of_time_test(): #future todo: should use test generator
    i = 5
    c = Clock(i)
    #i = -5
    c.seek(i+0.1)
    #c.seek(i)
    
