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
	try:
	    size = self.GetSize()
	    # scale picture by original width to height scale
	    self.bitmap = wx.BitmapFromImage(self.original_image.Scale(size[0], size[1]))
        except:
            self.bitmap = None # in case of an error paint black

    def SetImage(self, image_string):
	try:
	  self.original_image = wx.ImageFromBuffer(self.width, self.height, image_string)
	except:
	  self.image = None
	else:
	  self._PrepareImage()
	  self.Refresh()

    def SetImageSize(self, width, height):
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
