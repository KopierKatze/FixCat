try:
    import cPickle as pickle
except ImportError:
    import pickle

class Saveable(object):
    """This is the parent class for all classes
    which have to save date in order to restore
    the current program state (project).

    The getState method has to be overwritten
    in the child.
    It should return a pickable standart python
    object (list, dict, str, integer, ...).

    Pay attention that the loading process is
    only a convention. Saving on the other hand
    is implemented by the `SaveController`
    class.
    You have to take care about loading on your
    own."""

    def __init__(self, saved_state=None):
        """When the saved program state is loaded
        this object will be passed to the `__init__`
        constructor as keyword argument `saved_state`."""
        raise NotImplementedError('This method should be overwritten in the child.')

    def getState(self):
        """This method should return a standart python
        object which contains the whole state of this
        object."""
        raise NotImplementedError('This method should be overwritten in the child.')

class SaveController(object):
    """This class implements saving of childs of the `Saveable` class.

    Example:

    .. python::

        # saveing:
        sc = SaveController()
        # adding states
        sc.addSaveble('Identifier1', savable1)
        sc.addSaveble('SomethingOther', savable2)
        # write to file
        sc.saveToFile('program_state.save')

        # loading:
        sc = SaveController()
        # load from file
        sc.loadFromFile('program_state.save')
        # retrieve saved states
        saved_state1 = sc.getSavedState('Identifier1')
        saved_state2 = sc.getSavedState('SomethingOther')
        # now do something with saved_state1 and
        # saved_state2 ;)

    This class uses json to write the python object
    into a file and parse them back on loading into
    python objects.

    You are free to use another technology than json.
    Simply subclass this class and overwrite
    loadFromFile and saveToFile accordiently."""
    def __init__(self):
        """Creates state container."""
        self.savable_objects = {}

    def addSaveable(self, savable_name, obj):
        """Adds the current state of `obj` to this
        SaveController. It will be written to file
        when the `saveToFile` method is invoked.

        `savable_name` is a arbitary identifier
        with which you can retrieve the state of
        `obj` after you loaded it from file
        (SaveController.getSavedState('savable_name')).

        `obj` has to have a `Saveable.getState` method which
        should return the current state as a python
        standart object (see `Saveable` class)."""
        if not hasattr(obj, "getState"): raise SaveControllerError('You tried to add a object without ``getState`` method into a SaveController.')

        self.savable_objects[savable_name] = obj.getState()

    def saveToFile(self, filepath):
        """Writes the added states (`addSaveable()` method) to the
        file specified by `filepath` using the python pickle module.

        Will raise `SaveControllerError` s on failures."""
        try:
            fh = open(filepath, "wb")
        except IOError as e:
            raise SaveControllerError("Couldn't open %s for saving program state. (%s)" % (filepath, e))
        try:
            pickle.dump(self.savable_objects, fh)
        except Exception as e:
            raise SaveControllerError("%s" % e)
        fh.close()

    def loadFromFile(self, filepath):
        """Loads saved states from the file specified by `filepath`.

        You can access the saved states with the `getSavedState()`
        method.

        This method will raise `SaveControllerError` s on failures."""
        try:
            fh = open(filepath, "rb")
        except IOError as e:
            raise SaveControllerError("Couldn't open %s for loading. (%s)" % (filepath, e))
        try:
            self.savable_objects = pickle.load(fh)
        except Exception as e:
            raise SaveControllerError("%s" % e)
        fh.close()

    def getSavedState(self, savable_name):
        """Return the saved state which is identified by
        `savable_name`.

        You can use this method to retrieve the saved states
        after loading them from a file with `loadFromFile()`
        and also directly after adding them with `addSaveable()`."""
        return self.savable_objects[savable_name]


class SaveControllerError(Exception):
    """Is raised when:

     - You try to add a Saveable with addSaveable that has no getState method.
     - On failures while loading loadFromFile or saving saveToFile
    """
    pass
