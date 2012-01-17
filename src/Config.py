import json
import wx

config_filepath = None

categories_and_attributes = {
  'keyboard_shortcuts':
    ['play/pause', 'prev_frame', 'next_frame', 'faster', 'slower'],
  'cursors':
    ['blink', 'fixated', 'saccade'],
}

class Config(object):
  def __init__(self):
    # will hold configuration information in a dict
    self.raw = None

  def load(self):
    """load and check configuration from a file."""
    try:
      fp = open(config_filepath)
      try:
        self.raw = json.load(fp)
      except ValueError:
        raise ConfigError('Konfigurationsdatei nicht valid formatiert (JSON).')
      else:
        self.raw = []
    except IOError:
      raise ConfigError('Konfigurationsdatei nicht lesbar.')
    else:
      fp.close()
    
    # check consistency of configuration
    self.check()

  def _check(self, soll, haben, category_name=None):
    """compare soll and haben """
    soll = set(soll)
    haben = set(haben)
    
    to_less = soll - haben
    if not len(to_less) == 0:
      if category_name:
	raise ConfigError('In Kategorie %s der Konfigurationsdatei fehlen folgende Attribute: %s' % (category_name, to_less))
      else:
	raise ConfigError('Fehlende Kategorien in der Konfigurationsdatei: %s.' % to_less)

    to_much = (haben - set(['__comment'])) - soll
    if not len(to_much) == 0:
      if category_name:
	raise ConfigError('In Kategorie %s der Konfigurationsdatei sind folgende unbekannte Attribute: %s' % (category_name, to_much))
      else:
	raise ConfigError('Unbekannte Kategorien in der Konfigurationsdatei: %s.' % to_much)

  def check(self):
    """evaluate the current raw dict whether it is a valid pypsy config."""

    # vollstaendigkeit und nicht uebervoll
    self._check(categories_and_attributes.keys(), self.raw.keys())
    for category in categories_and_attributes.keys():
      self._check(categories_and_attributes[category], self.raw[category].keys())

    # keyboard_shortcuts
    for category in categories_and_attributes.keys():
      for attr in categories_and_attributes[category]:
	# will raise errors
	self.get(category, attr)

  def write_default(self):
    f = open(config_filepath, "wb")
    f.write(default_config)
    f.close()

  def get(self, category, attr):
    if category == 'keyboard_shortcuts':
      value = self.raw[category][attr]
      if type(value) == str:
	if value.isdigit():
	  return int(value)
	elif hasattr(wx, "WXK_"+value.upper()):
	  return getattr(wx, "WXK_"+value.upper())
      elif type(value) == int:
	return value
      elif value == None:
	return None
      else:
	raise ConfigError('Konfigurationsdatei enthaelt falschen Keyboard Shortcut fuer %s (Wert: %s).' % (attr, value))
    else:
      return self.raw[category][attr]

class ConfigError(Exception):
  pass

# default configuration
default_config_raw = {
'__comment':"This is the pypsy configuration. It is writen in JSON Format. So be shure to write valid JSON. (http://www.json.org/)",
'keyboard_shortcuts':{
    '__comment': 'You could use the ascii code of a key or the wxPython key name without WXK_ prefix (see http://wxpython.org/docs/api/wx.KeyEvent-class.html).',
    'play/pause': 97,
    'prev_frame': "98",
    'next_frame': "LEFT",
    'faster': "up",
    'slower': None
  },
'cursors': {
    '__comment': 'Path of pictures used as cursors for the different eye states. (supported filetypes: http://opencv.willowgarage.com/documentation/python/highgui_reading_and_writing_images_and_video.html#loadimage )',
    'blink': '',
    'fixated': '',
    'saccade': '',
  },
}
default_config = json.dumps(default_config_raw, indent=4)


if __name__ == '__main__':
  c = Config()
  c.raw = default_config_raw
  c.check()