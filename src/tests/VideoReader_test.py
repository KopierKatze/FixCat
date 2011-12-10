import nose
from VideoReader import VideoReader, ReaderError

@nose.tools.raises(ReaderError)
def init_test():
    reader = VideoReader('')

#    @nose.tools.raises(ReaderError) 
#    def frameAt_test():
#        #duration, -1, 
#        reader = VideoReader('/home/copycat/projects/pypsy/fuckyeah.avi')
#        frame_wrongduration = reader.frameAt(30)
        #frame_invalid = reader.frameAt(-1)
        
@nose.tools.raises(ReaderError)
def duration_test():
    reader = VideoReader(None)
    duration = reader.duration()
    
@nose.tools.raises(ReaderError)
def fps_test():
    reader = VideoReader(None)
    fps = reader.fps()

