class CategoryContainer(object):
  def __init__(self, indices):
    """
    ``indices`` is a dict mapping a tuple (begin frame number, end frame number)
    to indices of the object which are categoriesed.
    Fixations are indexed by the second in the edf file the fixation starts.
    Frames are indexed by their number (of occurrence in the video). So in the
    case of categoriesed frames this mapping maps (1,1) to 1, (2,2) to 2, (i,i) to i ...
    """

    self.indices = indices
    # used to iterate in order over all object under categorisation
    self.start_end_frames = self.indices.keys()
    self.start_end_frames.sort()
    # index to category
    self.categorisations = {}
    for index in self.indices.keys():
      self.categorisations[index] = None

    # keyboard shortcut to category name
    self.categories = {}

  def addCategory(self, shortcut, category_name):
    if not shortcut or len(shortcut) != 1: raise CategoryContainerError("Shortcut has to be a char")
    if shortcut in self.categories.keys(): raise CategoryContainerError("Shortcut already assigned")
    self.categories[shortcut] = category_name

  def listCategories(self):
    return self.categories

  def removeCategory(self, shortcut):
    if not self.categories.has_key(shortcut): raise CategoryContainerError("Can't delete this category: no such shortcut assigned")
    del self.categories[shortcut]

    for index in self.categorisations.keys():
      if self.categorisations[index] == shortcut:
	self.categorisations[index] = None

  def changeCategory(self, old_shortcut, new_shortcut, category_name):
    if not self.categories.has_key(old_shortcut): raise CategoryContainerError("Can't change this category: no such shortcut assigned")
    # add new category, does checking :)
    self.addCategory(new_shortcut, category_name)
    
    # replace already assigned indexes to new shortcut
    for index in self.categorisations.keys():
      if self.categorisations[index] == old_shortcut:
	self.categorisations[index] = new_shortcut
	
    # remove old shortcut
    self.removeCategory(old_shortcut)

  def categorise(self, frame, shortcut):
    """categorieses an index"""
    if not shortcut in self.categories.keys(): raise CategoryContainerError("Can't categorise! no such shortcut assigned (%s)" % shortcut)
    if frame > self.start_end_frames[len(self.start_end_frames)-1][1]: raise CategoryContainerError("Can't categorise! Index out of range")
    for index in self.start_end_frames:
      if frame >= index[0] and frame <= index[1]:
        self.categorisations[index] = shortcut

  def listCategorisations(self):
    return self.categorisations

  def nextNotCategorisedIndex(self, current_frame):
    i = 0
    while self.start_end_frames[i][0] < current_frame:
      i += 1

    while i < len(self.start_end_frames):
      if self.categorisations[self.start_end_frames[i]] == None:
	return self.start_end_frames[i][0]
    return None

class CategoryContainerError(Exception):
  pass