from EyeMovement import EyeMovement, EyeMovementError
from nose.tools import assert_raises

def single_status_test():
  em = EyeMovement('tests/data/eye_movement_test.asc')

  assert em.statusLeftEyeAt(0.001) == 'saccade', "%s" % em.statusLeftEyeAt(0.001)
  assert em.statusLeftEyeAt(0.05) == 'fixated'
  assert em.statusRightEyeAt(0.1) == 'blink'

  with assert_raises(EyeMovementError):
    em.statusLeftEyeAt(0.101)
    em.statusRightEyeAt(0.101)

def mean_status_test():
  em = EyeMovement('tests/data/eye_movement_test.asc')
  
  assert em.meanStatusAt(0.001) == 'saccade'
  assert em.meanStatusAt(0.05) == 'fixated'
  assert em.meanStatusAt(0.1) == 'fixated'

def single_looking_coordinates_test():
  em = EyeMovement('tests/data/eye_movement_test.asc')

  assert em.rightLookAt(0.001) == (3.0, 4.0)
  assert em.leftLookAt(0.100) == (151.0, 152.0)
  
  with assert_raises(EyeMovementError):
    em.leftLookAt(0.101)
    em.rightLookAt(0.101)

def mean_looking_coordinates_test():
  em = EyeMovement('tests/data/eye_movement_test.asc')
  
  assert em.meanLookAt(0.04) == (2.0, 3.0)
  assert em.meanLookAt(0.091) == (152.0, 153.0)

  with assert_raises(EyeMovementError):
    em.meanLookAt(1.0)
    
def duration_test():
  em = EyeMovement('tests/data/eye_movement_test.asc')

  assert em.duration() == 0.1, "Testfile contains 100msecs, not %f." % em.duration()

