from Clock import Clock, ClockError, ClockWorker
from nose.tools import assert_raises
from time import sleep, time

def seek_test():
    c = Clock(4)
    assert_raises(ClockError, c.seek ,4+0.1)
    c.seek(3.987)
    assert c.time == 3.987

def recall_test():
  global hey
  c = Clock(2)
  c.register(hey1)
  hey = 23
  c.seek(1)
  sleep(0.01)
  assert hey == 24
  
  c = Clock(2)
  c.register(hey2)
  hey = 23
  t1 = time()
  c.seek(2)
  assert time() - t1 < 1
  assert hey == 23

def hey1(time):
  global hey
  hey += 1

def hey2(time):
  """i'm fucking evil!!!!"""
  global hey
  sleep(40)
  hey += 2

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
    
def double_run_test():
    c = Clock(2)
    c.run()
    assert_raises(ClockError, c.run)

