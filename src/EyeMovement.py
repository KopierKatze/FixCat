from Savable import Savable

import re

class EyeMovement(Savable):
  number = r'([ 0-9]{5}.[0-9])'
  eye_look = r'(([0-9]+)\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t.)'
  saccade = r'(SSACC (L|R)  ([0-9]+))'
  fixation = r'(SFIX (L|R)   ([0-9]+))'
  blink = r'(SBLINK (L|R) ([0-9]+))'
  start = r'(START\t([0-9]+) \tLEFT\tRIGHT\tSAMPLES\tEVENTS)'
  end = r'(END\t([0-9]+) \tSAMPLES\tEVENTS\tRES\t([ 0-9]{4}.[0-9]{2})\t([ 0-9]{4}.[0-9]{2}))'
  frame = r'(MSG\t([0-9]+) VFRAME ([0-9]+) ([a-zA-Z0-9]+.avi))'
  
  def __init__(self, filename=None, saved_state={}):
    assert filename or saved_state, "No data for EyeMovement provided!"
    assert filename and not saved_state or saved_state and not filename, "filename and saved_state provided! Don't know which to take."

    self._status_left = saved_state.get('left', []) # 'fixated', 'saccade', 'blink' or None; indexed by frame
    self._status_right = saved_state.get('right', []) #  -- " --
    self._status_mean = saved_state.get('mean', []) #  -- " --

    self._looks = saved_state.get('looks', []) # (left, right); indexed by frame

    if filename:
      #checks
      self._parseFile(filename)

  def getState(self):
    return {'left':self._status_left, 'right':self._status_right, 'mean':self._status_mean, 'looks':self._looks}

  def _parseFile(self, filename):
    """
    SAMPLES EVENTS keyword
    timestamps are milliseconds
    """

    # regular expressions
    eye_look_re = re.compile(self.eye_look)
    saccade_re = re.compile(self.saccade)
    fixation_re = re.compile(self.fixation)
    blink_re = re.compile(self.blink)
    start_re = re.compile(self.start)
    end_re = re.compile(self.end)
    frame_re = re.compile(self.frame)

    # create containers
    looks = {}
    status_left = {}
    status_rigth = {}

    # set start time to None, before anything can be added we have to know the starttime!
    starttime = None
    
    # open file
    fd = open(filename)

    current_frame = None

    #checks are ordered in likelieness of statements
    for line in fd:
      frame = frame_re.match(line)
      if frame:
	current_frame = int(frame.groups()[2])
	current_frame -= 1 # cvs frames start at 0 eyelinks frames at 1
	
      # we index by frames... so everything bevor a frame indication is thrown away!
      if current_frame == None:
	continue
	  
      eye_look = eye_look_re.match(line)
      if eye_look:
	looks[current_frame] = (
	    (float(eye_look.groups()[2]), float(eye_look.groups()[3])),
	    (float(eye_look.groups()[5]), float(eye_look.groups()[6])),
	  )
	continue

      saccade = saccade_re.match(line)
      if saccade:
	if saccade.groups()[1] == 'L':
	  status_left[current_frame] = (saccade.groups()[2], 'saccade')
	else:
	  status_rigth[current_frame] = (saccade.groups()[2], 'saccade')

      fixation = fixation_re.match(line)
      if fixation:
	if fixation.groups()[1] == 'L':
	  status_left[current_frame] = (fixation.groups()[2], 'fixated')
	else:
	  status_rigth[current_frame] = (fixation.groups()[2], 'fixated')

      blink = blink_re.match(line)
      if blink:
	if blink.groups()[1] == 'L':
	  status_left[current_frame] = (blink.groups()[2], 'blink')
	else:
	  status_rigth[current_frame] = (blink.groups()[2], 'blink')

      if (end_re.match(line)):
	break # we reached end of file

    # parsing is over!
    # now complete our containers for faster access of data
    self._looks = self._completeContainer(looks)
    self._status_left = self._completeContainer(status_left)
    self._status_right = self._completeContainer(status_rigth)
    self._calculateMeanStatusList()

  def _completeContainer(self, container):
    complete = []
    current_value = None
    for i in xrange(max(container.keys())):
      if container.has_key(i):
	current_value = container[i]
      complete.append(current_value)
    return complete

  def _calculateMeanStatus(self, left, right):
    if left is None and right is None:
      return None
    elif left is None:
      return right
    elif right is None:
      return left
    
    if left[1] == 'fixated' or right[1] == 'fixated':
      return (max(int(left[0]), int(right[0])), 'fixated')

    elif left[1] == 'saccade' or right[1] == 'saccade':
      return (max(int(left[0]), int(right[0])), 'saccade')

    else:
      return (max(int(left[0]), int(right[0])), 'blink')

  def _calculateMeanStatusList(self):
    self._status_mean = []
    previous_state = None
    previous_index = None
    
    for frame in xrange(max(len(self._status_left), len(self._status_right))):
      # shouldn't be needed as we complete them until the last frame
      # but safety first
      if frame > len(self._status_left):
	left = (0,None)
      else:
	left = self._status_left[frame]
      if frame > len(self._status_right):
	right = (0,None)
      else:
	right = self._status_right[frame]

      inference = self._calculateMeanStatus(left, right)
      # if this is the first entry simply take the inference
      if previous_index is None or previous_state is None:
	self._status_mean.append(inference)
	continue

      # if the state didn't change retain the current index
      if previous_state == inference[1]:
	self._status_mean.append((previous_index, previous_state))
      else:
	# otherwise take new state and maximum index (see _calculateMeanStatus)
	self._status_mean.append(inference)

  def statusLeftEyeAt(self, frame):
    return self._status_left[frame][1]

  def statusRightEyeAt(self, frame):
    return self._status_right[frame][1]

  def meanStatusAt(self, frame):
    return self._status_mean[frame][1]

  def rightLookAt(self, frame):
    try:
      return self._looks[frame][1]
    except TypeError:
      return None

  def leftLookAt(self, frame):
    try:
      return self._looks[frame][0]
    except TypeError:
      return None

  def meanLookAt(self, frame):
    l = self.leftLookAt(frame)
    r = self.rightLookAt(frame)

    if l is None or r is None:
      return None

    return ((l[0] + r[0])/2.0, (l[1] + r[1])/2.0)

  def nextFixationFrame(self, frame, left):
    if left is True:
      return self._prev_nextFixationFrame(frame, 1, self.statusLeftEyeAt)
    elif left is False:
      return self._prev_nextFixationFrame(frame, 1, self.statusRightEyeAt)
    elif left is None:
      return self._prev_nextFixationFrame(frame, 1, self.meanStatusAt)
    else:
      raise Exception("left has to be True, False or None!")

  def prevFixationFrame(self, frame, left):
    if left is True:
      return self._prev_nextFixationFrame(frame, -1, self.statusLeftEyeAt)
    elif left is False:
      return self._prev_nextFixationFrame(frame, -1, self.statusRightEyeAt)
    elif left is None:
      return self._prev_nextFixationFrame(frame, -1, self.meanStatusAt)
    else:
      raise Exception("left has to be True, False or None!")

  def _prev_nextFixationFrame(self, frame, direction, func):
    saw_other_state = False
    current_frame = frame

    while not saw_other_state or not func(current_frame) == 'fixated':
      current_frame = current_frame + direction
      if func(current_frame) != 'fixated':
	saw_other_state = True
    return current_frame

  def fixations(self, left):
    """returns a list of fixation indexes (times of their occurence in edf file)
    indexed by (start of fixation video frame, end of fixation video frame)"""
    if left is True:
      status = self._status_left
    elif left is False:
      status = self._status_right
    elif left is None:
      status = self._status_mean
    else:
      raise Exception("left has to be True or False or None!")

    result = {}
    last_index = None
    current_start_frame = None
    current_index = None
    for frame in xrange(len(status)):
      stat = status[frame]
      if stat is None:
	continue
      if stat[1] == 'fixated' and current_start_frame is None:
	last_index = stat[0]
	current_start_frame = frame
	current_index = stat[0]
      elif not current_index is None and not current_start_frame is None and stat[1] != 'fixated':
	result[(current_start_frame, frame-1)] = current_index
	current_start_frame = None
	current_index = None

    if not current_index is None and not current_start_frame is None:
      result[(current_start_frame, len(status)-1)] = current_index
    return result


class EyeMovementError(Exception):
  pass

if __name__ == '__main__':
  e = EyeMovement('../example/t2d1gl.asc')