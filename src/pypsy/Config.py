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
    ['play/pause', 'prev_frame', 'next_frame', 'next_fixation', 'prev_fixation', 'faster', 'slower', 'delete'],
  'cursors':
    ['blink_left', 'fixated_left', 'saccade_left', 'blink_right', 'fixated_right', 'saccade_right', 'blink_mean', 'fixated_mean', 'saccade_mean'],
  'general':
    ['autosave_minutes', 'video_export_codec'],
}

class Config(object):
    """This class is used for creating a .json config file for pyPsy, if 
    necessary, and it takes care of performing a `check()` if the config 
    file is valid.
    All data is stored in a dictionary. 
    The config file has to be called config.json in order for pyPsy to 
    recognize and use it. """
    def __init__(self):
        """Checks if there is already an existing config file. If not, a new 
        one will be created. After that, the config file will be loaded via the 
        `load()` method. """
        self.raw = None

        if not self.file_available():
            self.write_default()

        self.load()

    def file_available(self):
        """Checks, if the config file at `config_filepath` exists. Returns
        True if the file exists. """
        return os.path.isfile(config_filepath)

    def load(self):
        """Loads and checks configuration of a file."""
        try:
            fp = open(config_filepath)
            try:
                self.raw = json.load(fp)
            except ValueError:
                raise ConfigError('Config file not formatted correctly (JSON).')
        except IOError:
            raise ConfigError('Could not read config file.')
        finally:
            fp.close()

        # check consistency of configuration
        self.check()

    def _check(self, debit, credit, category_name=None):
        """Helper function of `check()`. This function actually compares the 
        amounts of needed data(`debit`) and existing data(`credit`). """
        debit = set(debit)
        credit = set(credit)

        to_less = debit - credit
        if not len(to_less) == 0:
            if category_name:
                raise ConfigError('The %s category lacks the following attributes: %s' % (category_name, to_less))
            else:
                raise ConfigError('The following categories are missing in the config file: %s.' % to_less)

        to_much = (credit - set(['__comment'])) - debit
        if not len(to_much) == 0:
            if category_name:
                raise ConfigError('The %s category has the following unknown attributes: %s' % (category_name, to_much))
            else:
                raise ConfigError('The following unknown categories were found in the config file: %s.' % to_much)

    def check(self):
        """Evaluate the current raw dictionary whether it is a valid pypsy config
        by compary needed data and existing data of the config file. 
        Both amounts are compared in the `_check()` method. """

        # completeness and not too much
        self._check(categories_and_attributes.keys(), self.raw.keys())
        for category in categories_and_attributes.keys():
            self._check(categories_and_attributes[category], self.raw[category].keys())

        for category in categories_and_attributes.keys():
            for attr in categories_and_attributes[category]:
                # will raise errors
                self.get(category, attr)

    def write_default(self):
        """ Writes the data of the `default_config` into a new config file at
        `config_filepath`."""
        try:
            f = open(config_filepath, "wb")
            f.write(default_config)
            f.close()
        except Exception, e:
            raise ConfigError('Could not write config file (%s).' % e.message)

    def get(self, category, attr):
        """ This method is used by `check()` in order to retreive configuration 
        data from the dictionary. Individual shortcuts (`attr`) are listed within
        the keyboard_shortcuts `category`. 
        autosave_minutes and the codec used for the video export
        are stored in the general `category`. """
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
            raise ConfigError('The config file contains the following wrong keyboard shortcut for %s (value: %s).' % (attr, value))
        elif category == 'cursors':
            try:
                return cv.LoadImage(self.raw[category][attr])
            except IOError, e:
                raise ConfigError('Could not open cursor %s (%s) (path: %s).' % (attr, e.message, self.raw[category][attr]))
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
                        raise ConfigError('The time interval for autosaving has to be either 0 or null (deactivated) or a digit; you inserted: %s' % self.raw[category][attr])
            elif attr == 'video_export_codec':
                if not (type(self.raw[category][attr]) == unicode and len(self.raw[category][attr]) == 4):
                    raise ConfigError('The codec for exporting a video has to be a valid FOURCC codec (eg: "DIVX").')
                else:
                    return str(self.raw[category][attr])
        return self.raw[category][attr]

class ConfigError(Exception):
    """A ConfigError is thrown in case of errors in the config file, for example:
        1. If the config file is not formatted correctly in the json syntax.
        2. If the file could not be read correctly (eg. a read error of the 
            operating system occured.
        3. If attributes or categories are missing or uknown attributes or 
            categories are found. 
        4. If the config file could not be written to disk. This includes errors
            from the operating system as well, eg. if the user has no write 
            permissions in the directory.
        5. If a keyboard shortcut is not spelled properly, meaning that it is 
            not part of the standard keycodes used for eg. the space key. 
            For examples please see the standard configuration below in 
            `default_config_raw`. 
        6. If one of the cursor files could not be opened, eg. because of a 
            reading error thrown by the operating system.
        7. If the time interval in autosave_minutes is less than 0 (or null) 
            or not a number at all.
        8. If the codec in the `video_export_codec` field is not a valid FOURCC 
            codec. Please see fourcc.org for information about FOURCC codecs. """
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
    'delete': 'delete',
  },
'cursors': {
    '__comment': 'Path of pictures used as cursors for the different eye states. (supported filetypes: http://opencv.willowgarage.com/documentation/python/highgui_reading_and_writing_images_and_video.html#loadimage )',
    'blink_left': 'cursors/blinking_left.png',
    'fixated_left': 'cursors/fixation_left.png',
    'saccade_left': 'cursors/saccade_left.png',
    'blink_right': 'cursors/blinking_right.png',
    'fixated_right': 'cursors/fixation_right.png',
    'saccade_right': 'cursors/saccade_right.png',
    'blink_mean': 'cursors/blinking_mean.png',
    'fixated_mean': 'cursors/fixation_mean.png',
    'saccade_mean': 'cursors/saccade_mean.png',
  },
'general': {
    'autosave_minutes' : 5,
    "__comment": "Please only edit this, if you know which codecs you have installed. The string for the codec is composed of the four letters of the fourcc codec without spaces or other characters. For more information about fourcc please see http://www.fourcc.org/codecs.php",
    'video_export_codec' : 'DIVX',
  }
}
default_config = json.dumps(default_config_raw, indent=4)


if __name__ == '__main__':
    c = Config()
    c.raw = default_config_raw
    c.check()
