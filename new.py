import wx
from pyo import*
class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, 
                         #style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
                         style = wx.DEFAULT_FRAME_STYLE )
        self.Show()




class slider():
    def __init__(self, parent):
        sl = PyoGuiControlSlider(parent=parent)
def stuff(event):
    print('stuff')

s = Server().boot().start()
app = wx.App()
root = MainWindow()
sl = PyoGuiControlSlider(parent=root, minvalue=0, maxvalue=100)
sl.Bind(EVT_PYO_GUI_CONTROL_SLIDER, stuff)

app.MainLoop()

self._Cutoff = PyoGuiControlSlider(parent=self, pos= (0,0), minValue= 20, maxValue=20000, orient=wx.VERTICAL, log=True, name= 'Cutoff')
self._Enphasis = PyoGuiControlSlider(parent=self, pos= (40, 0), minValue= 0, maxValue=1000, orient=wx.VERTICAL, log=True, name= 'Enphasis')
self._Ammount = PyoGuiControlSlider(parent=self, pos= (80, 0), minValue= 0, maxValue=1000, orient=wx.VERTICAL, name= 'Ammount')
self._Attack = PyoGuiControlSlider(parent=self, pos= (0, 200), minValue= 0, maxValue=100, orient=wx.VERTICAL, name= 'Attack')
self._Decay = PyoGuiControlSlider(parent=self, pos= (40, 200), minValue= 0, maxValue=100, orient=wx.VERTICAL, name= 'Decay')
self._Sustain = PyoGuiControlSlider(parent=self, pos= (80, 200), minValue= 0, maxValue=100, orient=wx.VERTICAL, name= 'Sustain')