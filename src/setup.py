from distutils.core import setup
import py2exe

setup(console=['start_pypsy.py'],
options={
  'py2exe':{
    'excludes':['email', 'Tkinter',],# 'unittest', 'setuptools', 'urllib', 'urllib2', 'compiler', 'distutils', 'doctest', 'logging', 'optparse', 'pdb', 'pydoc'],
    'includes':['numpy'],
    'optimize':2,
    'bundle_files':3,
    }
  }
)

