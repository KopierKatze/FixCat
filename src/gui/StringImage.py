import wx

class StringImage(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.image = None
        self.width = None
        self.height = None

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        dc.SetBackground(wx.Brush('#000'))
        dc.Clear()
        if not self.image is None:
            dc.BeginDrawing()
            dc.DrawBitmap(self.image, 0, 0)
            dc.EndDrawing()
        return event

    def SetImage(self, image):
        try:
            self.image = wx.BitmapFromBuffer(self.width, self.height, image)
        except:
            self.image = None # in case of an error paint black
        self.Refresh()

    def SetSize(self, width, height):
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
