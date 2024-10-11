import wx
from pyo import*
class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, 
                         #style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
                         style = wx.DEFAULT_FRAME_STYLE )
        self.Show()

class KeyboardPanel(wx.Panel):
    def __init__(self, parent=None, obj=None):
        wx.Panel.__init__(self, parent, size=(1200, 100), pos=(50, 500))
        self.obj = obj
        self.keyboard = Keyboard(self, -1, outFunction=self.obj._newNote, size=(1200, 100))
        self.keyboard.hold = 0
        self.keyboard.SetFocus
        self.Show()
 
class AppGrid(wx.Panel):
 
    """Draw a line to a panel."""
 
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, size=(1300,600), pos=(0,0))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
 
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(260, 50, 260, 450)
        dc.DrawLine(780, 50, 780, 450)
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.DrawLine(280, 150, 760, 150)
        dc.DrawLine(280, 250, 760, 250)
        dc.DrawLine(280, 350, 760, 350)

class OscControls(wx.Panel):
    def __init__(self, parent, osc, dsp, title) -> None:
        self.osc=osc
        self.dsp=dsp
        wx.Panel.__init__(self, parent, size=(500,500))
        self._switch = wx.CheckBox(parent=self, label=title)
        self._switch.SetValue(True)
        self._waveforms=['Triangle', 'Saw', 'Square']
        self._waveform = wx.ComboBox(parent=self, choices=self._waveforms, style=wx.CB_READONLY)
        self._octave = wx.Choice(parent=self, choices=['-3', '-2', '-1', '0', '+1', '+2'])
        self._octave.SetSelection(3)
        self._detune = wx.Slider(parent=self, minValue= -100, maxValue=100, style=wx.SL_VALUE_LABEL | wx.SL_BOTTOM, name= 'detune')
        self._volume = wx.Slider(parent=self, minValue= 0, maxValue=10000, style=wx.SL_VERTICAL, size=(21, 100))
        layout = wx.GridBagSizer(vgap=10, hgap=10)
        layout.Add(self._switch,pos=(0,0))
        layout.Add(self._waveform,pos=(1,0))
        layout.Add(self._octave,pos=(1,1))
        layout.Add(self._detune, pos=(2,0))
        layout.Add(self._volume, pos=(3,0))
        self.SetSizer(layout)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnOff)
        self.Bind(wx.EVT_COMBOBOX, self.changeWaveform)
        self.Bind(wx.EVT_CHOICE, self.changeOctave)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeVolume)


    def OnOff(self, event):
        if self._switch.IsChecked() == True:
            print('ON')
            self.osc.osc.setMul(self.dsp.AmpEnv)
        else:
            print('OFF')
            self.osc.osc.setMul(0)

    def changeWaveform(self, event):
        self.osc.setWaveform(self._waveforms.index(self._waveform.GetValue()))

    def changeOctave(self, event):
        self.osc.setOctave(int(event.GetString()))

    def changeVolume(self, event):
        vol = float(self._volume.GetValue()/10000)
        self.osc.setVolume(vol)
        
class NoiseOscControls(wx.Panel):
    def __init__(self, parent, ancor) -> None:
        wx.Panel.__init__(self, parent, size=(780,133), pos=ancor)
        self._switch = wx.CheckBox(parent=self, pos = ancor, label='ON/OFF')
        self._switch.SetValue(False)
        self._type = wx.ToggleButton(parent=self, pos=(ancor[0], ancor[1]+25), label='WHITE')
        self._volume = wx.Slider(parent=self, pos= (ancor[0], ancor[1]+50), minValue= 0, maxValue=100, style=wx.SL_VALUE_LABEL | wx.SL_BOTTOM |wx.SL_INVERSE, name= 'volume')
        
        self.Bind(wx.EVT_CHECKBOX, self.OnOff)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.ChangeType)


    def OnOff(self, event):
        pass

    def ChangeType(self, event):
        if self._type.GetValue() == True:
            self._type.SetLabel('PINK')
        else:
            self._type.SetLabel('WHITE')

class LoudnessContour(wx.Panel):
    def __init__(self, parent, ancor, dsp) -> None:
        wx.Panel.__init__(self, parent, size=(780,300), pos=ancor)
        self.dsp = dsp
        self._Attack = wx.Slider(parent=self, pos= (ancor[0], ancor[1]), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Attack')
        self._Decay = wx.Slider(parent=self, pos= (ancor[0]+40, ancor[1]), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Decay')
        self._Sustain = wx.Slider(parent=self, pos= (ancor[0]+80, ancor[1]), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Sustain')
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeADSR)

    def changeADSR(self, event):
        self.dsp.AmpEnv.setAttack(self._Attack.GetValue()/100)
        self.dsp.AmpEnv.setDecay(self._Decay.GetValue()/100)
        self.dsp.AmpEnv.setSustain(self._Sustain.GetValue()/100)

class FilterControls(wx.Panel):
    def __init__(self, parent, ancor, filter) -> None:
        wx.Panel.__init__(self, parent, size=(780,500), pos=ancor)
        self.filter = filter
        self._Cutoff = wx.Slider(parent=self, pos= (ancor[0], ancor[1]), minValue= 20, maxValue=20000, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Cutoff')
        self._Enphasis = wx.Slider(parent=self, pos= (ancor[0]+40, ancor[1]), minValue= 0, maxValue=2000, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Enphasis')
        self._Ammount = wx.Slider(parent=self, pos= (ancor[0]+80, ancor[1]), minValue= 0, maxValue=1000, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Ammount')
        self._Attack = wx.Slider(parent=self, pos= (ancor[0], ancor[1]+200), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Attack')
        self._Decay = wx.Slider(parent=self, pos= (ancor[0]+40, ancor[1]+200), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Decay')
        self._Sustain = wx.Slider(parent=self, pos= (ancor[0]+80, ancor[1]+200), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Sustain')
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeFilterValues)

    def changeFilterValues(self, event):
        self.filter.setEnv(self._Attack.GetValue()/100,
                           self._Decay.GetValue()/100,
                           self._Sustain.GetValue()/100)
        self.filter.setRes(self._Enphasis.GetValue()/1000)
        self.filter.setFreq(self._Cutoff.GetValue(), self._Ammount.GetValue())

def startGUI(dsp):
    root = MainWindow()
    #frame = AppGrid(root)
    #frame.Show()
    #KeyboardPanel(parent=root, obj=dsp._notes)
    osc1 = OscControls(root, dsp._osc1, dsp, 'OSC 1')
    #osc2 = OscControls(root, dsp._osc2, dsp, 'OSC 2')
    #osc3 = OscControls(root, (1010, 310), dsp._osc2, dsp, 'OSC 3')

    layout = wx.BoxSizer(wx.VERTICAL)
    layout.Add(osc1, proportion=1, flag=wx.ALIGN_LEFT|wx.ALIGN_TOP, border=10)
    #layout.Add(osc2, proportion=1, flag=wx.ALIGN_LEFT|wx.ALIGN_TOP, border=10)
    root.SetSizer(layout)


    #FilterControls(root, (10,10), dsp._filter)
    #LoudnessContour(root, (0,0), dsp)

    

