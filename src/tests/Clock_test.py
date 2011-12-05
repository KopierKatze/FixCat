from Clock import Clock, ClockError, ClockWorker
import nose

@nose.tools.raises(ClockError)
def end_of_time_test(): #future todo: should use test generator
    i = 5 # if generator is present, maybe end_of_time_test gets parameters
    c = Clock(i)
    c.seek(i+0.1)
    
