import wx

class StringImage(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self._PrepareImage)

        # no flickering even in windows
        self.SetDoubleBuffered(True)

        self.original_image = None
        self.bitmap = None
        self.width = None
        self.height = None

    def OnPaint(self, event):
	"""paint the scaled image onto widget.
	
	if there were problems retrieving or scaling the image
	the widget will be black."""
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush('#000'))
        dc.Clear()
        if not self.bitmap is None:
            dc.BeginDrawing()
            # center picture according to scale
            dc.DrawBitmap(self.bitmap, 0, 0)
            dc.EndDrawing()
        return event

    def _PrepareImage(self, event_stub=None):
	"""scale the image to widgets size"""
	try:
	    widget_size = self.GetSize()
	    # scale picture by original width to height scale
	    self.bitmap = wx.BitmapFromImage(self.original_image.Scale(widget_size[0], widget_size[1]))
        except:
            self.bitmap = None # in case of an error paint black

    def SetImage(self, image_string):
	"""set a new image.
	the image is a string containing the rgb value of the pixels.
	
	to restore a real image out of this string this method needs information
	about the size of the image which is encoded in ``image_string``.
	so be sure to give this information with ``SetImageSize`` before calling
	this method.
	"""
	try:
	  # build a wxImage of this image_string and size information
	  self.original_image = wx.ImageFromBuffer(self.width, self.height, image_string)
	except:
	  # this will result in a black widget
	  self.image = None
	else:
	  # scale image to current widget size
	  self._PrepareImage()
	  self.Refresh()

    def SetImageSize(self, width, height):
	"""assigne dimensions of the image encoded in ``image_string`` argument of ``SetImage``.

	this information is needed to retrieve the image out of the ``image_string``."""
        self.width = width
        self.height = height

if __name__ == '__main__':
    import cv
    class MyFrame(wx.Frame):
      def __init__(self):
	wx.Frame.__init__(self, None)

	vid = OpenCVImage(self, wx.ID_ANY)

	c = cv.CaptureFromFile('../new_ingpsy2/example/overlayed_video.avi')
	vid.SetImage(cv.QueryFrame(c).tostring())
    a = wx.App()
    mf = MyFrame()
    mf.Show()
    a.MainLoop()
