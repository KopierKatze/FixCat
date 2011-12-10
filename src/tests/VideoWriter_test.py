import nose
import os
from VideoWriter import VideoWriter, WriterError

@nose.tools.raises(VideoWriter)
def init_test():
    writer = VideoWriter(None, 854, 428, 14, None)
    
