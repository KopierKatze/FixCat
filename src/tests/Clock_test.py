from Clock import Clock, ClockError, ClockWorker
import nose

@nose.tools.raises(ClockError)
def end_of_time_test(): #future todo: should use test generator
    i = 5 # if generator is present, maybe end_of_time_test gets parameters
    c = Clock(i)
    c.seek(i+0.1)
    
@nose.tools.raises(ClockError)
def set_multiplicator_test():
    c = Clock(3)
    c.setMultiplicator(0)
    
@nose.tools.raises(ClockError)
def stop_test():
    c = Clock(2)
    c.stop()
    
@nose.tools.raises(ClockError)
def running_test():
    c = Clock(2)
    c.run()
    c.run()

