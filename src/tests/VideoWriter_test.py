import nose
import os
from VideoWriter import VideoWriter, WriterError

@nose.tools.raises
def init_test():
    #f = os.open('/home/copycat/projects/pypsy/test_fuckyeah.avi', 'w')
    writer = VideoWriter(None, 854, 428, 14, None)
    
