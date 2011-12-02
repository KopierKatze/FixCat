from Clock import Clock, ClockError, ClockWorker
import nose

def test_generator():
    
    for i in range(0, 5):
        yield end_of_time_test, i

def end_of_time_test(i): #should use test generator
    c = Clock(i)
    c.seek(i-0.1)
    c.seek(i)
    #nose.tools.raises(ClockError, c.seek, i+0.000001)


