from distutils.core import setup
import py2exe

setup(
  console=['start_pypsy.py'],
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

