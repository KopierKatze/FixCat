"""
Copyright 2012 Alexandra Weiß, Franz Gregor

This file is part of FixCat.

FixCat is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FixCat is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FixCat.  If not, see <http://www.gnu.org/licenses/>.

This module contains helping functions which are
quite generic and likely to be handy in other projects
to."""

def KeyCodeToHumanReadable(KeyCode):
    """Return a human readable expression for
    a wxPython key code."""
    if not type(KeyCode) == int: return '?'

    if KeyCode in xrange(32, 256):
        return chr(KeyCode)

    return str(KeyCode)
