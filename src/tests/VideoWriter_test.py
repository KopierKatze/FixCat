import nose
import os
from VideoWriter import VideoWriter, WriterError
import cv

@nose.tools.raises(WriterError)
def init_test():
    writer = VideoWriter(None, 854, 428, 14, None)
    

@nose.tools.raises(WriterError)
def addFrame_test():
    writer = VideoWriter('/home/copycat/Desktop/pypsy/test_fuckyeah.avi', 854, 428, 14, cv.CV_FOURCC('X', 'V', 'I', 'D'))
    writer.addFrame(None)
    
