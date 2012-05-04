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
"""
from distutils.core import setup
import py2exe

setup(
  console=[{
    'script':'fixcat.py',
    'icon_resources':[(1, 'icon.ico')]}],
  zipfile=None, # integrate library into .exe
  options={
    'py2exe':{
      'excludes':['_gtkagg', '_tkagg', 'bsddb',
                  'curses', 'email', 'pywin.debugger',
                  'pywin.debugger.dbgcon', 'pywin.dialogs',
                  'tcl', 'Tkconstants', 'Tkinter', 'email',
                  'pydoc_data', 'doctest', 'compiler',
                  'xml', 'distutils', 'setuptools',
                  'logging', 'pydoc', 'tarfile',
                  'urllib', 'urllib2', 'cookielib',
                  'optparse', 'xmlrpclib', 'zipfile',
                  'httplib', 'xmllib', 'inspect',
                  'urlparse', 'warnigns', 'ssl', '_ssl',
                  'pdb', 'calendar',
                  'pyreadline', 'pstats', 'ConfigParser',
                  'plistlib', 'stringprep', 'gzip',],
      'includes':['numpy'],
      'optimize':2,
      'bundle_files':3,
      'ascii':False, # somehow we need encodings
      'compressed':True,
      'dll_excludes':['AVICAP32.dll', 'AVIFIL32.dll',
                      'MSACM32.dll', 'MSVFW32.dll'],
    }
  }
)
