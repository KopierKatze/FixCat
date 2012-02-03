import json
import os

import wx

try:
  from cv2 import cv
except ImportError:
  import cv


config_filepath = 'config.json'

categories_and_attributes = {
  'keyboard_shortcuts':
    ['play/pause', 'prev_frame', 'next_frame', 'next_fixation', 'prev_fixation', 'faster', 'slower'],
  'cursors':
    ['blink_left', 'fixated_left', 'saccade_left', 'blink_right', 'fixated_right', 'saccade_right', 'blink_mean', 'fixated_mean', 'saccade_mean'],
  'general':
    ['autosave_minutes'],
}

class Config(object):
  def __init__(self):
    # will hold configuration information in a dict
    self.raw = None

    if not self.file_available():
      self.write_default()

    self.load()

  def file_available(self):
    return os.path.isfile(config_filepath)

  def load(self):
    """load and check configuration from a file."""
    try:
      fp = open(config_filepath)
      try:
        self.raw = json.load(fp)
      except ValueError:
        raise ConfigError('Konfigurationsdatei nicht valid formatiert (JSON).')
    except IOError:
      raise ConfigError('Konfigurationsdatei nicht lesbar.')
    finally:
      fp.close()
    
    # check consistency of configuration
    self.check()

  def _check(self, debit, credit, category_name=None):
    """compare debit and credit"""
    debit = set(debit)
    credit = set(credit)

    to_less = debit - credit
    if not len(to_less) == 0:
      if category_name:
	raise ConfigError('In Kategorie %s der Konfigurationsdatei fehlen folgende Attribute: %s' % (category_name, to_less))
      else:
	raise ConfigError('Fehlende Kategorien in der Konfigurationsdatei: %s.' % to_less)

    to_much = (credit - set(['__comment'])) - debit
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

    for category in categories_and_attributes.keys():
      for attr in categories_and_attributes[category]:
	# will raise errors
	self.get(category, attr)

  def write_default(self):
    try:
      f = open(config_filepath, "wb")
      f.write(default_config)
      f.close()
    except Exception, e:
      raise ConfigError('Konnte die Konfigurationsdatei nicht anlegen (%s).' % e.message)

  def get(self, category, attr):
    if category == 'keyboard_shortcuts':
      value = self.raw[category][attr]
      if hasattr(value, "isdigit"):
	if value.isdigit():
	  return int(value)
	elif hasattr(wx, "WXK_"+value.upper()):
	  return getattr(wx, "WXK_"+value.upper())
      elif type(value) == int:
	return value
      elif value == None:
	return None
      # if none of the above found the correct key not valid
      raise ConfigError('Konfigurationsdatei enthaelt falschen Keyboard Shortcut fuer %s (Wert: %s).' % (attr, value))
    elif category == 'cursors':
      try:
	return cv.LoadImage(self.raw[category][attr])
      except IOError, e:
	raise ConfigError('Konnte Cursor fuer %s nicht oeffnen (%s) (Pfad: %s).' % (attr, e.message, self.raw[category][attr]))
    elif category == 'general':
      if attr == 'autosave_minutes':
	if self.raw[category][attr] is None:
	  return None
	else:
	  try:
	    val = float(self.raw[category][attr])
	    if val == 0:
	      return None
	    else:
	      return val
	  except TypeError:
	    raise ConfigError('Die Angabe der Zeit zwischen dem automatischem Speichern muss entweder 0 o. null sein (deaktiviert) oder eine Zahl, nicht %s' % self.raw[category][attr])
    else:
      return self.raw[category][attr]

class ConfigError(Exception):
  pass

# default configuration
default_config_raw = {
'__comment':"This is the pypsy configuration. It is writen in JSON Format. So be shure to write valid JSON. (http://www.json.org/)",
'keyboard_shortcuts':{
    '__comment': 'You could use the ascii code of a key or the wxPython key name without WXK_ prefix (see http://wxpython.org/docs/api/wx.KeyEvent-class.html).',
    'play/pause': "space",
    'prev_frame': "left",
    'next_frame': "right",
    'prev_fixation': "up",
    'next_fixation': "down",
    'faster': None,
    'slower': None,
  },
'cursors': {
    '__comment': 'Path of pictures used as cursors for the different eye states. (supported filetypes: http://opencv.willowgarage.com/documentation/python/highgui_reading_and_writing_images_and_video.html#loadimage )',
    'blink_left': 'cursors/blinking.png',
    'fixated_left': 'cursors/fixation.png',
    'saccade_left': 'cursors/saccade.png',
    'blink_right': 'cursors/blinking.png',
    'fixated_right': 'cursors/fixation.png',
    'saccade_right': 'cursors/saccade.png',
    'blink_mean': 'cursors/blinking.png',
    'fixated_mean': 'cursors/fixation.png',
    'saccade_mean': 'cursors/saccade.png',
  },
'general': {
    'autosave_minutes' : 5,
  }
}
default_config = json.dumps(default_config_raw, indent=4)


if __name__ == '__main__':
  c = Config()
  c.raw = default_config_raw
  c.check()
