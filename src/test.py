import wx
import cv
from time import sleep, time
import cProfile

picture = None


class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, size=wx.Size(720, 480))
    self.Bind(wx.EVT_PAINT, self.onPaint)
    
    self.t = wx.StaticText(self)
    
  def onPaint(self, evt):
    dc = wx.PaintDC(self)
    
    dc.BeginDrawing()
    i = wx.ImageFromData(picture.width, picture.height, picture.tostring())
    b = wx.BitmapFromImage(i)
    dc.DrawBitmap(b, 0, 0)
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

