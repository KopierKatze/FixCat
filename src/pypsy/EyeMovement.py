from Saveable import Saveable
import os.path
import re

class EyeMovement(Saveable):
    """Provides eye positions and states.

    Therefore it parses in ascii text exported edf-files
    with regular expressions.

    The data is frame based organized and accessible."""
    #: regular expression for a number in the exported edf-file
    number = r'([ 0-9]{5}.[0-9])'
    #: regular expression for a eye position statement in the exported edf-file
    eye_look = r'(([0-9]+)\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t'+number+r'\t.)'
    #: regular expression for a the beginning of a saccade in the exported edf-file
    saccade = r'(SSACC (L|R)  ([0-9]+))'
    #: regular expression for a the beginning of a fixation in the exported edf-file
    fixation = r'(SFIX (L|R)   ([0-9]+))'
    #: regular expression for a the beginning of a blink in the exported edf-file
    blink = r'(SBLINK (L|R) ([0-9]+))'
    #: regular expression for a the end of eye movement data in the exported edf-file
    end = r'(END\t([0-9]+) \tSAMPLES\tEVENTS\tRES\t([ 0-9]{4}.[0-9]{2})\t([ 0-9]{4}.[0-9]{2}))'
    #: regular expression for a frame indication in the exported edf-file
    frame = r'(MSG\t([0-9]+) VFRAME ([0-9]+) ([a-zA-Z0-9]+.avi))'
    #: regular expression for a the trialid in the exported edf-file
    trialid = r'(MSG\t([0-9]+) TRIALID ([0-9]+))'

    def __init__(self, filepath=None, trialid_target=None, saved_state={}):
        """Parse a new exported edf-file or recreate a saved state.

        You can either give a filepath and a `trialid_target` or a `saved_state`.

        A exported edf-file can contain various experiments (trials).
        Specify the wanted trial with `trialid_target`."""
        if (filepath is None or trialid_target is None) and saved_state=={}: raise EyeMovementError("No eyemovement data given.")
        if saved_state and (filepath and trialid_target): raise EyeMovementError("You gave a saved eyemovement state and a new eyemovement file. Don't know what to do.")

        self._status_left = saved_state.get('left', []) # 'fixated', 'saccade', 'blink' or None; indexed by frame
        self._status_right = saved_state.get('right', []) #  -- " --
        self._status_mean = saved_state.get('mean', []) #  -- " --

        self._looks = saved_state.get('looks', []) # (left, right); indexed by frame

        if filepath and trialid_target:
            if not os.path.isfile(filepath): raise EyeMovementError("Die angegebene Augenbewegungsdatei existiert nicht")
            if not os.access(filepath, os.R_OK): raise EyeMovementError("Auf die angegebene Augenbewegungsdatei kann nicht zugegriffen werden (keine Leseberechtigung).")
            self._parseFile(filepath, trialid_target)

    def getState(self):
        return {'left':self._status_left, 'right':self._status_right, 'mean':self._status_mean, 'looks':self._looks}

    def _parseFile(self, filepath, trialid_target):
        """Parse the exported edf-file `filepath` and extract
        eye position and state information with the help the regular
        expressions."""

        # regular expressions
        eye_look_re = re.compile(self.eye_look)
        saccade_re = re.compile(self.saccade)
        fixation_re = re.compile(self.fixation)
        blink_re = re.compile(self.blink)
        end_re = re.compile(self.end)
        frame_re = re.compile(self.frame)
        trialid_re = re.compile(self.trialid)

        # create containers
        looks = {}
        status_left = {}
        status_rigth = {}

        # set start time to None, before anything can be added we have to know the starttime!
        starttime = None

        # open file
        fd = open(filepath)

        current_frame = None

        #: if this is True we already reached our target trial
        in_trial = False

        #checks are ordered in likelieness of statements
        for line in fd:
            if not in_trial:
                trialid = trialid_re.match(line)
                if trialid and trialid.groups()[2] == str(trialid_target):
                    # we reached the first line of our target trial
                    in_trial = False
                else:
                    # we are not yet at our target trial -> jump to next line
                    continue

            frame = frame_re.match(line)
            if frame:
                current_frame = int(frame.groups()[2])

            # we index by frames... so everything bevor a frame indication is thrown away!
            if current_frame == None:
                continue

            eye_look = eye_look_re.match(line)
            if eye_look:
                looks[current_frame] = (
                    (float(eye_look.groups()[2]), float(eye_look.groups()[3])),
                    (float(eye_look.groups()[5]), float(eye_look.groups()[6])),
                )
                continue

            saccade = saccade_re.match(line)
            if saccade:
                if saccade.groups()[1] == 'L':
                    status_left[current_frame] = (saccade.groups()[2], 'saccade')
                else:
                    status_rigth[current_frame] = (saccade.groups()[2], 'saccade')

            fixation = fixation_re.match(line)
            if fixation:
                if fixation.groups()[1] == 'L':
                    status_left[current_frame] = (fixation.groups()[2], 'fixated')
                else:
                    status_rigth[current_frame] = (fixation.groups()[2], 'fixated')

            blink = blink_re.match(line)
            if blink:
                if blink.groups()[1] == 'L':
                    status_left[current_frame] = (blink.groups()[2], 'blink')
                else:
                    status_rigth[current_frame] = (blink.groups()[2], 'blink')

            if (end_re.match(line)):
                break # we reached end of file

        # parsing is over!
        if not in_trial:
            # we never reached the target trialid
            raise EyeMovementError("Couldn't find the given trial id in the eyemovement file.")
        # now complete our containers for faster access of data
        self._looks = self._completeContainer(looks)
        self._status_left = self._completeContainer(status_left)
        self._status_right = self._completeContainer(status_rigth)
        self._calculateMeanStatusList()

    def _completeContainer(self, container):
        complete = []
        current_value = None
        for i in xrange(max(container.keys())):
            if container.has_key(i):
                current_value = container[i]
            complete.append(current_value)
        return complete

    def _calculateMeanStatus(self, left, right):
        if left is None and right is None:
            return None
        elif left is None:
            return right
        elif right is None:
            return left

        if left[1] == 'fixated' or right[1] == 'fixated':
            return (max(int(left[0]), int(right[0])), 'fixated')

        elif left[1] == 'saccade' or right[1] == 'saccade':
            return (max(int(left[0]), int(right[0])), 'saccade')

        else:
            return (max(int(left[0]), int(right[0])), 'blink')

    def _calculateMeanStatusList(self):
        self._status_mean = []
        previous_state = None
        previous_index = None

        for frame in xrange(max(len(self._status_left), len(self._status_right))):
            # shouldn't be needed as we complete them until the last frame
            # but safety first
            if frame > len(self._status_left):
                left = (0,None)
            else:
                left = self._status_left[frame]
            if frame > len(self._status_right):
                right = (0,None)
            else:
                right = self._status_right[frame]

            inference = self._calculateMeanStatus(left, right)
            # if this is the first entry simply take the inference
            if previous_index is None or previous_state is None:
                self._status_mean.append(inference)
                continue

            # if the state didn't change retain the current index
            if previous_state == inference[1]:
                self._status_mean.append((previous_index, previous_state))
            else:
                # otherwise take new state and maximum index (see _calculateMeanStatus)
                self._status_mean.append(inference)

    def _getListTupleItem(self, list, list_index, tuple_index):
        try:
            return list[list_index][tuple_index]
            # happens if eye info is None -> no status for this frame
        except TypeError:
            return None
            # if frame is not in the list -> video longer than eye status
        except IndexError:
            return None

    def statusLeftEyeAt(self, frame):
        return self._getListTupleItem(self._status_left, frame, 1)

    def statusRightEyeAt(self, frame):
        return self._getListTupleItem(self._status_right, frame, 1)

    def meanStatusAt(self, frame):
        return self._getListTupleItem(self._status_mean, frame, 1)

    def rightLookAt(self, frame):
        return self._getListTupleItem(self._looks, frame, 1)

    def leftLookAt(self, frame):
        return self._getListTupleItem(self._looks, frame, 0)

    def meanLookAt(self, frame):
        l = self.leftLookAt(frame)
        r = self.rightLookAt(frame)

        if l is None or r is None:
            return None

        return ((l[0] + r[0])/2.0, (l[1] + r[1])/2.0)

    def nextFixationFrame(self, frame, left):
        if left is True:
            return self._prev_nextFixationFrame(frame, 1, self.statusLeftEyeAt, len(self._status_left))
        elif left is False:
            return self._prev_nextFixationFrame(frame, 1, self.statusRightEyeAt, len(self._status_right))
        elif left is None:
            return self._prev_nextFixationFrame(frame, 1, self.meanStatusAt, len(self._status_mean))
        else:
            raise Exception("left has to be True, False or None!")

    def prevFixationFrame(self, frame, left):
        if left is True:
            return self._prev_nextFixationFrame(frame, -1, self.statusLeftEyeAt, len(self._status_left))
        elif left is False:
            return self._prev_nextFixationFrame(frame, -1, self.statusRightEyeAt, len(self._status_right))
        elif left is None:
            return self._prev_nextFixationFrame(frame, -1, self.meanStatusAt, len(self._status_mean))
        else:
            raise Exception("left has to be True, False or None!")

    def _prev_nextFixationFrame(self, frame, direction, func, max_frame):
        saw_other_state = False
        current_frame = frame

        while not saw_other_state or not func(current_frame) == 'fixated':
            if current_frame >= max_frame:
                return None
            current_frame = current_frame + direction
            if func(current_frame) != 'fixated':
                saw_other_state = True
        return current_frame

    def fixations(self, left):
        """returns a list of fixation indexes (times of their occurence in edf file)
        indexed by (start of fixation video frame, end of fixation video frame)"""
        if left is True:
            status = self._status_left
        elif left is False:
            status = self._status_right
        elif left is None:
            status = self._status_mean
        else:
            raise Exception("left has to be True or False or None!")

        result = {}
        last_index = None
        current_start_frame = None
        current_index = None
        for frame in xrange(len(status)):
            stat = status[frame]
            if stat is None:
                continue
            if stat[1] == 'fixated' and current_start_frame is None:
                last_index = stat[0]
                current_start_frame = frame
                current_index = stat[0]
            elif not current_index is None and not current_start_frame is None and stat[1] != 'fixated':
                result[(current_start_frame, frame-1)] = current_index
                current_start_frame = None
                current_index = None

        if not current_index is None and not current_start_frame is None:
            result[(current_start_frame, len(status)-1)] = current_index
        return result
        
    def maxFrames(self):
        """Returns maximum length of the containers `looks`, `status_left` and 
        `status_rigth`. This is used fot the plausibility check for the creation
        of a new project(does video and eyemovement data belong together?)."""
        return max(len(looks), len(status_left), len(status_rigth))
      


class EyeMovementError(Exception):
    pass

if __name__ == '__main__':
    e = EyeMovement('../example/t2d1gl.asc')
