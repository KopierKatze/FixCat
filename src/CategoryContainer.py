class CategoryContainer(object):
  def __init__(self, max_index):
    """
    max_index : how much frames/fixations should be available
    """
    self.categorisations = {} # index to category
    for i in xrange(max_index):
      self.categorisations[i+1] = None

    self.categories = {} # shortcut to name

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

  def categorise(self, index, shortcut):
    """categorieses an index"""
    if not shortcut in self.categories.keys(): raise CategoryContainerError("Can't categorise! no such shortcut assigned")
    if not index in self.categorisations.keys(): raise CategoryContainerError("Can't categorise! Index out of range")
    self.categorisations[index] = shortcut

  def listCategorisations(self):
    return self.categorisations

  def nameOfShortcut(self, shortcut):
    if not shortcut in self.categories.keys(): raise CategoryContainerError("No such shortcut assigned")
    return self.categories[shortcut]

  def nextNotCategorisedIndex(self):
    for index in self.categorisations.keys():
      if self.categorisations[index] == None:
	return index
    return None

class CategoryContainerError(Exception):
  pass