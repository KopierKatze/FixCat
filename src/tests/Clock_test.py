from Clock import Clock, ClockError, ClockWorker
from nose.tools import assert_raises
from time import sleep

def end_of_time_test(): 
    c = Clock(4)
    assert_raises(ClockError, c.seek ,4+0.1)

def set_multiplicator_test():
    c = Clock(10,  0.0001)
    # multiplicator of 0 would make the clock useless
    assert_raises(ClockError, c.setMultiplicator, 0)
    # test whether multiplicator works... no that deterministic test, no better idea
    c.setMultiplicator(10000000)
    c.run()
    sleep(0.2)
    # should not be running anymore...
    # 10000000 * 0.2 is obviously greater than 10
    # (multiplicator * time_passed > maximal duration of clock)
    assert c.running == False
    assert c.time == 10
    
def double_stop_test():
    c = Clock(2)
    c.run()
    c.stop()
    assert_raises(ClockError, c.stop)
    
def running_test():
    c = Clock(2)
    c.run()
    assert_raises(ClockError, c.run)

