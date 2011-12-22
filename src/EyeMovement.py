import re

class EyeMovement(object):
  number = r'([ 0-9]{5}.[0-9])'
  eye_look = r'(([0-9]+)\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t.)'
  saccade = r'(SSACC (L|R)  ([0-9]+))'
  fixation = r'(SFIX (L|R)   ([0-9]+))'
  blink = r'(SBLINK (L|R) ([0-9]+))'
  start = r'(START\t([0-9]+) \tLEFT\tRIGHT\tSAMPLES\tEVENTS)'
  end = r'(END\t([0-9]+) \tSAMPLES\tEVENTS\tRES\t([ 0-9]{4}.[0-9]{2})\t([ 0-9]{4}.[0-9]{2}))'
  frame = r'(MSG\t([0-9]+) VFRAME ([0-9]+) ([a-zA-Z0-9]+.avi))'
  
  def __init__(self, filename=None, saved_state=None):
    assert filename or saved_state, "No data for EyeMovement provided!"
    assert filename and not saved_state or saved_state and not filename, "filename and saved_state provided! Don't know which to take."

    self._status_left = [] # 'fixated', 'saccade' or 'blink'; indexed by frame
    self._status_rigth = [] #  -- " --

    self._looks = [] # (left, right); indexed by frame

    if filename:
      #checks
      self._parseFile(filename)
  
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
	  status_left[current_frame] = 'saccade'
	else:
	  status_rigth[current_frame] = 'saccade'

      fixation = fixation_re.match(line)
      if fixation:
	if fixation.groups()[1] == 'L':
	  status_left[current_frame] = 'fixated'
	else:
	  status_rigth[current_frame] = 'fixated'

      blink = blink_re.match(line)
      if blink:
	if blink.groups()[1] == 'L':
	  status_left[current_frame] = 'blink'
	else:
	  status_rigth[current_frame] = 'blink'

      if (end_re.match(line)):
	break # we reached end of file

    # parsing is over!
    # now complete our containers for faster access of data
    self._looks = self._completeContainer(looks)
    self._status_left = self._completeContainer(status_left)
    self._status_rigth = self._completeContainer(status_rigth)

  def _completeContainer(self, container):
    complete = []
    current_value = None
    for i in xrange(max(container.keys())):
      if container.has_key(i):
	current_value = container[i]
      complete.append(current_value)
    return complete

  def statusLeftEyeAt(self, frame):
    return self._status_left[frame]

  def statusRightEyeAt(self, frame):
    return self._status_rigth[frame]

  def meanStatusAt(self, frame):
    l = self.statusLeftEyeAt(frame)
    r = self.statusRightEyeAt(frame)

    if r == 'fixated' or l == 'fixated':
      return 'fixated'

    if r == 'saccade' or l == 'saccade':
      return 'saccade'

    return 'blink'

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

class EyeMovementError(Exception):
  pass

if __name__ == '__main__':
  e = EyeMovement('../example/t2d1gl.asc')