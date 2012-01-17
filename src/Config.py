import json
import wx

config_filepath = None

categories_and_attributes = {
  'keyboard_shortcuts':
    ['play/pause', 'prev_frame', 'next_frame', 'faster', 'slower']
}

class Config(object):
  def __init__(self):
    # will hold configuration information in a dict
    self.raw = None

  def load(self):
    """load and check configuration from a file."""
    self.raw = json.loads(config_filepath)
    self.check()

  def check(self):
    """evaluate the current raw dict whether it is a valid pypsy config."""
    pass
    # keyboard_shortcuts

  def write_default(self):
    f = open(config_filepath, "wb")
    f.write(default_config)
    f.close()

  def get(self, category, attr):
    if category == 'keyboard_shortcuts':
      return 0 
    else:
      return self.raw[category][attr]

class ConfigError(Exception):
  pass

# default configuration
default_config_raw = {}
default_config = json.dumps(default_config_raw, indent=4)
