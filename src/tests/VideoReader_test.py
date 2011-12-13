from nose.tools import assert_raises
from VideoReader import VideoReader, ReaderError

def init_test():
  assert_raises(ReaderError, VideoReader, None)
  assert_raises(ReaderError, VideoReader, '')
  assert_raises(ReaderError, VideoReader, 'afasfds')

  VideoReader('tests/data/fuckyeah.avi')

def duration_test():
  assert VideoReader('test/data/fuckyeah.avi').duration() == 1124

def fps_test():
  assert VideoReader('test/data/fuckyeah.avi').fps() == 14.985014985014985

