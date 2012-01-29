
def KeyCodeToHumanReadable(KeyCode):
  if not type(KeyCode) == int: return '?'

  if KeyCode in xrange(32, 256):
    return chr(KeyCode)

  return str(KeyCode)