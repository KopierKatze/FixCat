from Saveable import Saveable, SaveController

class CategoryContainer(Saveable):
    """The `CategoryContainer` is the central model for all categorisation
    stuff.

    It categorises "objects" (either frames or fixations). Every object has an
    index.
    Frames are indexed by their number (of occurence in the video).
    Fixations are indexed by their time of occurence in the edf-file in
    milliseconds.
    The object indices are used in the gui CategoryList and on csv export.
    Object have a duration. They "exist" only a certain time. A frame
    for example has a duration of 1 frame. A fixation can have a duration of
    multiple frames.
    So every object has one start and one endframe. Between (inclusiv start
    and endframe) it "is".

    A user will always categorise one frame! If there is a object at this from
    this object will be categories if not nothing happens (you are categorising
    fixations but currently there is a blink).

    When you categorise a object this class takes a key code and assignes it to
    the object. (But only if there is a category(name) with that key code.

    This key code is translated to the category name to which it belongs on
    output.

    Apart from categorising, deleting categorisations, editing categories
    this class is able to export the categorisations into a csv-file."""
    def __init__(self, indices=None, saved_state={}):
        """
        ``indices`` is a dict mapping a tuple (begin frame number, end frame number)
        to indices of the objects (either frames or fixations) which are categoriesed.

        Fixations are indexed by the second in the edf file the fixation starts.
        frames are indexed by their number (of occurrence in the video). So in the
        case of categoriesed frames this mapping maps (1,1) to 1, (2,2) to 2, (i,i) to i ...
        If we categoriese fixations it could be (4, 140) to 234252, (245, 500) to 2135462.
        """
        assert not (indices is None and saved_state == {})

        self.indices = saved_state.get('indices', indices)
        # used to iterate in order over all object under categorisation
        self.start_end_frames = self.indices.keys()
        self.start_end_frames.sort()
        # index to category
        self.categorisations = saved_state.get('categorisations', {})
        if not indices is None:
            for index in self.indices.keys():
                self.categorisations[index] = None

        # keyboard shortcut to category name
        self.categories = saved_state.get('categories', {})

    def getState(self):
        """Supply the current state of this `CategoryContainer` instance
        for saving.

        The state is composed of the categorie to key code mapping (categories),
        the object to key code mapping (categorisations) and the object to
        object index mapping (indices).

        Here object referrs to a tuple (start_frame, end_frame)."""
        return {'categories':self.categories, 'categorisations':self.categorisations, 'indices':self.indices}

    def export(self, filepath):
        """Export the current categorisations into a csv-file.
        The csv-file will contain the index, start, endframe and
        the assigned categoryname.

        This function is accessible from the gui."""
        f = open(filepath, "wb")
        # header
        f.write('Start frame, End frame, Index, Category\n')
        for start_frame, end_frame in self.start_end_frames:
            f.write('%s, %s, %s, %s\n' %(start_frame, end_frame, self.indices[(start_frame, end_frame)], self.categories.get(self.categorisations[(start_frame, end_frame)], "-")))
        f.close()

    def importCategories(self, filepath):
        """Import categories from another saved project.

        This will erased all existing categories and
        categorisations.

        This function is accessible from the gui"""
        sc = SaveController()
        sc.loadFromFile(filepath)

        saved_state = sc.getSavedState('category_container')

        # load saved categories
        self.categories = saved_state['categories']

        # delete all categorisations
        for key in self.categorisations.keys():
            self.categorisations[key] = None

    def getCategoryOfFrame(self, frame):
        """Return the category of frame `frame`.

        This function is used in the category loopthrough feature
        to check wheter we should categoriese a frame (it is not yet
        categoriesed) or not."""
        for start_frame, end_frame in self.start_end_frames:
            if frame >= start_frame and frame <= end_frame:
                return self.categorisations[(start_frame, end_frame)]
        return None

    def editCategory(self, old_shortcut, new_shortcut, category_name):
        """Edit a category.

        `old_shortcut` or `new_shortcut` can be None (create a new category,
        delete a old category).

        This function is accessible from the gui."""
        if not new_shortcut is None and new_shortcut in self.categories.keys() and new_shortcut != old_shortcut: raise CategoryContainerError('This hotkey is already assigned.')
        if not old_shortcut is None and not old_shortcut in self.categories.keys(): raise CategoryContainerError('The hotkey cannot be deleted, because it does not exist.')
        if not new_shortcut is None and (category_name is None or len(category_name) < 1): raise CategoryContainerError('Please enter a name for the category.')

        if not new_shortcut is None:
            self.categories[new_shortcut] = category_name

            if new_shortcut != old_shortcut and not old_shortcut is None:
                # move already categoriesed objects to new shortcut
                for index in self.categorisations.keys():
                    if self.categorisations[index] == old_shortcut:
                        self.categorisations[index] = new_shortcut

        if new_shortcut != old_shortcut and not old_shortcut is None:
            del self.categories[old_shortcut]
            for index in self.categorisations.keys():
                if self.categorisations[index] == old_shortcut:
                    self.categorisations[index] = None

    def categorise(self, frame, shortcut):
        """Categorises frame `frame` to the category
        which is assigned to the key code `shortcut`.

        As we categorise objects and not frames this functions
        searchs all objects and checks whether the `frame` lies
        between (inclusively) start and endframe of a object.
        If so the found object will get categorised. If not
        nothing happens.

        On succesfull object categorisation this function will
        return a tuple of the objects index and the category name.
        This tuple is used to update the GUI CategoryList on the
        right side of the application.

        This function is used in the MainFrame KeyEvent handler.
        (When a key gets pressed)"""
        if not shortcut in self.categories.keys(): raise CategoryContainerError("Can't categorise! no such shortcut assigned (%s)" % shortcut)
        if frame > self.start_end_frames[len(self.start_end_frames)-1][1]: raise CategoryContainerError("Can't categorise! Index out of range")
        for index in self.start_end_frames:
            if frame >= index[0] and frame <= index[1]:
                self.categorisations[index] = shortcut
                return (index, self.categories[shortcut])
        return False

    def deleteCategorisation(self, frame):
        """Same as `categorise` but deletes and doesn't
        return anything.

        This function is used when you mark objects in the
        CategoryList and press the delete hotkey."""
        for index in self.start_end_frames:
            if frame >= index[0] and frame <= index[1]:
                self.categorisations[index] = None

    def listCategories(self):
        return self.categories

    def dictOfCategorisations(self):
        """Return a dict which maps object indices to
        category names.

        This function is used when the CategoryList is
        populated in the load phase or after categories
        have been edited."""
        d = {}
        for index in self.start_end_frames:
            d[index]=(self.indices[index], self.categories.get(self.categorisations[index], "-"))

        return d

    def nextNotCategorisedIndex(self, current_frame):
        """Returns the starting frame of the next object
        which has not yet been categorised.

        This function is accessed from the GUI."""
        for start_frame, end_frame in self.start_end_frames:
            if start_frame > current_frame:
                if self.categorisations[(start_frame, end_frame)] == None:
                    return start_frame
        return None

class CategoryContainerError(Exception):
    pass
