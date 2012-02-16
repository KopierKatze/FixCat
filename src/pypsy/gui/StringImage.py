import wx

class StringImage(wx.Window):
    """This window/widget will show a image.

    It will resize the image to fit the space provided
    to this widget.

    The image is expected to be coded as a rgb string with
    specified width, height and therefore string length.

    This widget uses double buffering to prevent flickering."""
    def __init__(self, parent, id):
        """Create a new `StringImage`."""
        wx.Window.__init__(self, parent, id)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self._PrepareImage)

        # no flickering even in windows
        self.SetDoubleBuffered(True)

        self.original_image = None
        self.bitmap = None
        self.width = None
        self.height = None

        # offset of image display begin -> center image in widget
        self.offseth = 0
        self.offsetw = 0

    def OnPaint(self, event=None):
	"""paint the scaled image onto widget.
	
	if there were problems retrieving or scaling the image
	the widget will be black."""
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush('#000'))
        dc.Clear()
        if not self.bitmap is None:
            dc.BeginDrawing()
            # center picture according to scale
            dc.DrawBitmap(self.bitmap, self.offsetw, self.offseth)
            dc.EndDrawing()
        return event

    def _PrepareImage(self, event_stub=None):
	"""scale the image to widgets size"""
	try:
	    widgetw, widgeth = self.GetSize()
	    imagew, imageh = self.original_image.GetSize()
	    ratio = float(imagew) / float(imageh)
	    
	    if widgetw < (widgeth * ratio):
	      imagew_scale = widgetw
	      imageh_scale = widgetw / ratio
              # center image in widget
              self.offsetw = 0
              self.offseth = (widgeth - imageh_scale) / 2
	    else:
	      imagew_scale = widgeth * ratio
	      imageh_scale = widgeth
              # center image in widget
              self.offsetw = (widgetw - imagew_scale) / 2
              self.offseth = 0

	    # scale picture by original width to height scale
	    self.bitmap = wx.BitmapFromImage(self.original_image.Scale(imagew_scale, imageh_scale))
        except:
            self.bitmap = None # in case of an error paint black
        self.Refresh()

    def SetImage(self, image_string):
	"""set a new image.
	the image is a string containing the rgb value of the pixels.
	
	to restore a real image out of this string this method needs information
	about the size of the image which is encoded in `image_string`.
	so be sure to give this information with `SetImageSize` before calling
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
	"""assigne dimensions of the image encoded in `image_string` argument of `SetImage`.

	this information is needed to retrieve the image out of the `image_string`."""
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
