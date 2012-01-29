import cPickle

class Savable(object):
  def getState(self):
    raise NotImplementedError('')

class SaveController(object):
  def __init__(self):
    self.savable_objects = {}

  def addSavable(self, savable_name, obj):
    if not hasattr(obj, "getState"): raise SaveControllerError('You tried to add a object without ``getState`` method into a SaveController.')

    self.savable_objects[savable_name] = obj.getState()

  def saveToFile(self, filepath):
    fh = open(filepath, "wb")
    cPickle.dump(self.savable_objects, fh)
    fh.close()

  def loadFromFile(self, filepath):
    fh = open(filepath, "rb")
    self.savable_objects = cPickle.load(fh)
    fh.close()

  def getSavedState(self, savable_name):
    return self.savable_objects[savable_name]


class SaveControllerError(Exception):
  pass
