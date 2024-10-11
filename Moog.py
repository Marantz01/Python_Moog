import wx
from pyo import*
from GUI import*
from DSP import*

s = Server().boot().start()
app = wx.App()
dsp = MiniMoogDSP()
gui = startGUI(dsp)

app.MainLoop()