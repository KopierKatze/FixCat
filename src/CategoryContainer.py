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
    self.categories = {68:'HALLO WELT!'}

  def export(self, filepath):
    f = open(filepath, "wb")
    # header
    f.write('Startframe, Endframe, Index, Kategorie\n')
    for start_frame, end_frame in self.start_end_frames:
      f.write('%s, %s, %s, %s\n' %(start_frame, end_frame, self.indices[(start_frame, end_frame)], self.categories.get(self.categorisations[(start_frame, end_frame)], "-")))
    f.close()

  def editCategory(self, old_shortcut, new_shortcut, category_name):
    if not new_shortcut is None and new_shortcut in self.categories.keys(): raise CategoryContainerError('Dieses Tastenkuerzel ist schon vergeben.')
    if not old_shortcut is None and not old_shortcut in self.categories.keys(): raise CategoryContainerError('Fehler: Das zu loeschende Tastenkuerzel ist nicht vorhanden.')
    if category_name is None or len(category_name) < 1: raise CategoryContainerError('Bitte Namen der Kategorie angeben.')

    if not new_shortcut is None:
      self.categories[new_shortcut] = category_name

      if not old_shortcut is None:
	# move already categoriesed objects to new shortcut
	for index in self.categorisations.keys():
	  if self.categorisations[index] == old_shortcut:
	    self.categorisations[index] = new_shortcut

    if not old_shortcut is None:
      del self.categories[old_shortcut]
      for index in self.categorisations.keys():
	if self.categorisations[index] == old_shortcut:
	  self.categorisations[index] = None

  def categorise(self, frame, shortcut):
    """categorieses an index"""
    if not shortcut in self.categories.keys(): raise CategoryContainerError("Can't categorise! no such shortcut assigned (%s)" % shortcut)
    if frame > self.start_end_frames[len(self.start_end_frames)-1][1]: raise CategoryContainerError("Can't categorise! Index out of range")
    for index in self.start_end_frames:
      if frame >= index[0] and frame <= index[1]:
        self.categorisations[index] = shortcut
        return (index, self.categories[shortcut])
    return False

  def listCategories(self):
    return self.categories

  def dictOfCategorisations(self):
    d = {}
    for index in self.start_end_frames:
      d[index]=(self.indices[index], self.categories.get(self.categorisations[index], "-"))

    return d

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