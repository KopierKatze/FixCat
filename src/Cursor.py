from cv import LoadImage

class Cursor(object):
  """associates eye states(blinking, saccade, fixation) to cursor images.
  on initialation the class already has cursor images.
  those can be altered."""
  def __init__(self):
    """load standard images"""
    # cv.loadimage von den bildern
    self.cursor = dict([('blink', LoadImage('standard_cursors/blinking.png')),
        ('saccade', LoadImage('standard_cursors/saccade.png')),
        ('fixated', LoadImage('standard_cursors/fixation.png'))])

  def setCursorFor(self, state, file_or_image):
    """set new cursor image for specific state.
    image can be given as file or image
    raises Errors on file problems (not readable, not existing, ...) or
    if no proper image data is given"""
    self.cursor[state] = file_or_image

  def cursorFor(self, state):
    """return the cursor image for a certain state"""
    if state == None: return None
    if state == "don't know": return None
    return self.cursor[state]
