from Clock import Clock, ClockError
import nose

def end_of_time_test(): #should use test generator
  i = 5
  c = Clock(i)
  c.seek(i-0.1)
  c.seek(i)
  nose.tools.raises(ClockError, c.seek, i+0.000001)

def registered_function_call_test():
  pass
