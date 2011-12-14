import re
from math import floor

class EyeMovement(object):
  number = r'([ 0-9]{5}.[0-9])'
  eye_look = r'(([0-9]+)\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t.)'
  saccade = r'(ESACC (L|R)  ([0-9]+)\t([0-9]+)\t[0-9]+\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t([ 0-9]{4}.[0-9]{2})\t[ 0-9]+)'
  fixation = r'(EFIX (L|R)   ([0-9]+)\t([0-9]+)\t([0-9]+)\t'+number+r'\t'+number+r'\t[ 0-9]+)'
  blink = r'(EBLINK (L|R) ([0-9]+)\t([0-9]+)\t([0-9]+))'
  start = r'(START\t([0-9]+) \tLEFT\tRIGHT\tSAMPLES\tEVENTS)'
  end = r'(END\t([0-9]+) \tSAMPLES\tEVENTS\tRES\t([ 0-9]{4}.[0-9]{2})\t([ 0-9]{4}.[0-9]{2}))'
  
  def __init__(self, filename=None, saved_state=None):
    assert filename or saved_state, "No data for EyeMovement provided!"
    assert filename and not saved_state or saved_state and not filename, "filename and saved_state provided! Don't know which to take."

    self._status_left = {} # time -> status
    self._status_rigth = {} # time -> status

    self._looks = {} # time -> (left, right)

    self._duration = 0
    
    if filename:
      #checks
      self._parseFile(filename)

  def _findIndexOfSecond(self, second, sec_list):
    index = int(floor(second*1000))
    while not index in sec_list:
      print "index", index, "not in list"
      index -= 1
      if index <= 0:
	index = None
	break
    print "index is:", index
	
    if index == None:
      raise EyeMovementError("list doesn't contain anything!?")
    return index

      
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

    # set start time to None, before anything can be added we have to know the starttime!
    starttime = None
    
    # open file
    fd = open(filename)

    #checks are ordered in likelieness of statements
    for line in fd:
      eye_look = eye_look_re.match(line)
      if eye_look:
	assert starttime, "parsed eye look before startime is known! wrong source?"
	#add eye_look
	self._looks[int(eye_look.groups()[1]) - starttime] = (
	    (float(eye_look.groups()[2]), float(eye_look.groups()[3])),
	    (float(eye_look.groups()[5]), float(eye_look.groups()[6])),
	  )
	pass
      else:
	saccade = saccade_re.match(line)
	if saccade:
	  assert starttime, "parsed saccade before startime is known! wrong source?"
	  #add saccade
	  if saccade.groups()[1] == 'L':
	    self._status_left[int(saccade.groups()[2]) - starttime] = 'saccade'
	  else:
	    self._status_rigth[int(saccade.groups()[2]) - starttime] = 'saccade'
	else:
	  fixation = fixation_re.match(line)
	  if fixation:
	    assert starttime, "parsed fixation before startime is known! wrong source?"
	    #add fixation
	    if fixation.groups()[1] == 'L':
	      self._status_left[int(fixation.groups()[2]) - starttime] = 'fixated'
	    else:
	      self._status_rigth[int(fixation.groups()[2]) - starttime] = 'fixated'
	  else:
	    blink = blink_re.match(line)
	    if blink:
	      assert starttime, "parse blink before startime is known! wrong source?"
	      #add blink
	      if blink.groups()[1] == 'L':
		self._status_left[int(blink.groups()[2]) - starttime] = 'blink'
	      else:
		self._status_rigth[int(blink.groups()[2]) - starttime] = 'blink'
	    else:
	      start = start_re.match(line)
	      if start:
		#set start_time
		starttime = int(start.groups()[1])
	      else:
		end = end_re.match(line)
		if end:
		  assert starttime, "parsed end before startime is known! wrong source?"
		  #end parsing
		  self._duration = int(end.groups()[1]) - starttime
		  break

  def _statusEyeAt(self, second, status_list):
    if second*1000 > self._duration:
      raise EyeMovementError('Duration is %i msecs. You want data for %i msec.' %(self._duration, second*1000))
    
    try:
      index = self._findIndexOfSecond(second, status_list.keys())
      return status_list[index]
    except EyeMovementError:
      return None

  def statusLeftEyeAt(self, second):
    return self._statusEyeAt(second, self._status_left)

  def statusRightEyeAt(self, second):
    return self._statusEyeAt(second, self._status_rigth)

  def meanStatusAt(self, second):
    l = self.statusLeftEyeAt(second)
    r = self.statusRightEyeAt(second)

    if r == l:
      return r
    
    if l == 'blink':
      return r

    if r == 'blink':
      return l

    return "don't know"

  def duration(self):
    return self._duration / 1000.0

  def _lookAt(self, second, element):
    if second*1000 > self._duration:
      raise EyeMovementError('Duration is %i msecs. You want data for %i msec.' %(self._duration, second*1000))

    try:
      index = self._findIndexOfSecond(second, self._looks.keys())
      return self._looks[index][element]
    except EyeMovementError:
      return None
      
  def rightLookAt(self, second):
    return self._lookAt(second, 1)

  def leftLookAt(self, second):
    return self._lookAt(second, 0)

  def meanLookAt(self, second):
    l = self.leftLookAt(second)
    r = self.rightLookAt(second)
    if r is None or l is None: return None

    return ((l[0] + r[0])/2.0, (l[1] + r[1])/2.0)

class EyeMovementError(Exception):
  pass