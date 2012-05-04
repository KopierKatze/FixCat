"""
Copyright 2012 Alexandra Weiss, Franz Gregor

This file is part of FixCat.

FixCat is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

FixCat is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with FixCat.  If not, see <http://www.gnu.org/licenses/>.
"""
from Saveable import Saveable

from threading import Thread
from time import sleep, time
import os.path
try:
    from cv2 import cv
except ImportError:
    import cv

class VideoReader(Saveable):
    """This class provides an image-by-image access to a video file. """

    def __init__(self, filepath=None, saved_state={}):
        """Opens the video file at `filepath` by using a cv capture.
        The capture provides access to the frame size and frame count of the video
        file.
        `_determine_frame_count()` is used to precisely figure out the number of
        frames of the video file, since the result returned by the capture is not
        very precise.

        If an expected error occurs, a `ReaderError` is thrown."""

        if saved_state=={} and (filepath is None or filepath == ''):
            raise ReaderError('No video file specified.')
        if saved_state and not filepath is None:
            raise ReaderError('A video file has already been defined in the project file.')
        self.filepath = saved_state.get('filepath', filepath)

        if not os.path.isfile(self.filepath):
            raise ReaderError('The file you selected does not exist.')
        if not os.access(self.filepath, os.R_OK):
            raise ReaderError('This file cannot be accessed (no permission to read).')
        self.reader = cv.CaptureFromFile(self.filepath)
        # have to check if codec is available!
        test_frame = cv.QueryFrame(self.reader)
        if test_frame is None or test_frame.width == 0 or test_frame.height == 0:
            raise ReaderError('Video file could not be opened. Either the codec could not be retrieved or the file is broken.')
        self.height = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_HEIGHT))
        self.width = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_WIDTH))
        self.frame_count = self._determine_frame_count()
        self.fps = cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FPS)
        self.duration = self.frame_count * self.fps

    def getState(self):
        return {'filepath':self.filepath}

    def _determine_frame_count(self):
        current_frame = int(cv.GetCaptureProperty(self.reader, cv.CV_CAP_PROP_FRAME_COUNT))
        captured_frame = False
        while not captured_frame:
            try:
                self.frame(current_frame)
            except ReaderError:
                current_frame -= 1
            else:
                captured_frame = True
        exception_raised = False
        while not exception_raised:
            try:
                self.frame(current_frame+1)
            except ReaderError:
                exception_raised = True
            else:
                current_frame += 1
        return current_frame

    def frame(self, frame_number):
        """Returns the IplImage that you would see when accessing the frame of
        the video at the specified `frame_number`."""
        if (frame_number is not None and frame_number >= 0 and
            (not hasattr(self, "frame_count") or frame_number <= self.frame_count)):
            cv.SetCaptureProperty(self.reader, cv.CV_CAP_PROP_POS_FRAMES, frame_number)
            frame = cv.QueryFrame(self.reader) #IplImage
            return_frame = cv.CreateImage((self.width, self.height), cv.IPL_DEPTH_8U, 3)
            try:
                cv.Copy(frame, return_frame)
            except (TypeError, cv.error):
                """Copy will fail if no video frame was delivered by queryframe."""
                raise ReaderError("A problem occured while retrieving a frame.")
            return return_frame
        else:
            return ReaderError("The number of the frame has to be at least 0 and smaller than the amount of frames.")

    def releaseReader(self):
        """Closes VideoReader after use. """
        cv.ReleaseCapture(reader)

class ReaderError(Exception):
    """This error will be thrown in the following methods.
        0. A `ReaderError` is thrown in `VideoReader.__init__()` if:
            - `VideoReader.__init__.filepath` is None or empty and
                `VideoReader.__init__.saved_state` is empty. This means that no new
                file and no saved state are being opened.
            - `VideoReader.__init__.saved_state` is not empty and a
                `VideoReader.__init__.filepath` for a new file is specified. This means
                that it is unclear if we start from a saved state or start with a
                new video file.
            - the file at `VideoReader.__init__.filepath` does not exist or you
                do not have the rights to read it.
            - the codec could not be retrieved from the cv capture or the file
                might be broken.

        1. A `ReaderError` is thrown in `VideoReader.frame()` if:
            - a problem occured during retrieving a frame at the specified
                `VideoReader.frame.frame_number`
            - `VideoReader.frame.frame_number` is not a valid frame number, meaning
                that it is higher than the total number of frames or smaller than 0

    """
    pass
