class Cursor(object):
  """associates eye states(blinking, saccade, fixation) to cursor images.
  on initialation the class already has cursor images.
  those can be altered."""
  def __init__(self):
    """load standard images"""
    self.cursor = dict([('blinking', 'standard_cursors/blinking.png'), 
        ('saccade', 'standard_cursors/saccade.png'), 
        ('fixation', 'standard_cursors/fixation.png')])

  def setCursorFor(self, state, file_or_image):
    """set new cursor image for specific state.
    image can be given as file or image
    raises Errors on file problems (not readable, not existing, ...) or
    if no proper image data is given"""
    self.cursor[state] = file_or_image

  def cursorFor(self, state):
    """return the cursor image for a certain state"""
    return self.cursor[state]
