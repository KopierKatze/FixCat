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
try:
    from cv2 import cv
except ImportError:
    import cv

class VideoWriter(object):
    """Creates a new video file using a cv videowriter. Frames are added to it by
    using the `addFrame()` method. """
    def __init__(self, filepath, size, fps, codec):
        """Creates the video file with the given properties.
        The `codec` is specified in the config file as a string and is
        transformed into a valid fourcc codec here.
        The `size` of the output file has to be of type cv size.
        The framerate(`fps`) of the new video should be that of the video that is
        currently worked on.
        In case of an expected error, a `WriterError` will be thrown. """
        self.width = size[0]
        self.height = size[1]

        if filepath is None:
            raise WriterError("Please select a valid file path")

        codec = cv.CV_FOURCC(codec[0], codec[1], codec[2], codec[3])

        if fps is None or fps < 1:
            raise WriterError("Framerate has to be higher than 1.")
        if (self.width is None or self.height is None or
            self.width < 1 or self.height < 1):
            raise WriterError("Please specify a valid height/width of your video.")

        self.writer = cv.CreateVideoWriter(filepath, codec, fps, (size), 1)

    def addFrame(self, new_frame):
        """Adds a new frame to the end of the video file. Before the frame is
        added, the colors are converted from the color scheme used by opencv to
        the normal rgb color scheme. cv.CvtColor takes care of this.
        `new_frame` has to be of type IplImage.

        This method might fail if the disk is full. This is not checked at the
        moment. """
        if new_frame is None:
            raise WriterError("The new frame may not be none.")
        else:
            cv.CvtColor(new_frame, new_frame, cv.CV_BGR2RGB)
            cv.WriteFrame(self.writer, new_frame)

    def releaseWriter(self):
        """Closes VideoWriter after use. """
        del self.writer

class WriterError(Exception):
    """This error will be thrown in the following methods.
        0. A `WriterError` is thrown in `VideoWriter.__init__()` if:
            - no `VideoWriter.__init__.filepath` was specified
            - `VideoWriter.__init__.fps` was not specified or is lower than 1
            - the cv size of the output file was not specified or is smaller than 1

        1. A `WriterError` is thrown in `VideoWriter.addFrame()` if:
            - `VideoWriter.addFrame.new_frame` is none

    """
    pass
