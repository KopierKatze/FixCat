import wx
import cv
from time import sleep, time
import cProfile

v = cv.CaptureFromFile('/home/fg/ingpsyprojekt/example/overlayed_video.avi')

print cv.GetCaptureProperty(v, cv.CV_CAP_PROP_FOURCC)

def nextImageOf(v):
    f = cv.QueryFrame(v)
    i = wx.ImageFromData(f.width, f.height, f.tostring())
    b = wx.BitmapFromImage(i)
    return b

class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, size=wx.Size(720, 480))
    self.Bind(wx.EVT_PAINT, self.onPaint)
    
    self.t = wx.StaticText(self)
    
  def onPaint(self, evt):
    dc = wx.PaintDC(self)
    
    dc.BeginDrawing()
    dc.DrawBitmap(nextImageOf(v), 0, 0)
    dc.EndDrawing()
    
    # set "new" label to text -> emit repaint event
    #self.t.SetLabel("")
    #cmd = wx.CommandEvent(wx.EVT_ERASE_BACKGROUND.evtType[0])
    #cmd.SetEventObject(self)
    #cmd.SetId(self.GetId())
    #self.ProcessEvent(cmd)
    self.Refresh()
  
  def onErase(self, evt):
    cmd = wx.CommandEvent(wx.EVT_PAINT.evtType[0])
    cmd.SetEventObject(self)
    cmd.SetId(self.GetId())
    self.ProcessEvent(cmd)

if __name__ == '__main__':
  app = wx.App()
  mframe = MyFrame()
  mframe.Show()
  
  cProfile.run("app.MainLoop()")
  #app.MainLoop()

