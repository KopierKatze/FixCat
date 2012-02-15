"""This module contains helping functions which are
quite generic and likely to be handy in other projects
to."""

def KeyCodeToHumanReadable(KeyCode):
    """Return a human readable expression for
    a wxPython key code."""
    if not type(KeyCode) == int: return '?'

    if KeyCode in xrange(32, 256):
        return chr(KeyCode)

    return str(KeyCode)
