import wx
from pyo import*
PyoGuiControlSlider
class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(parent = None, size = (1000,628), style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX), title='Moog')
        self.Show()
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        pass
 

class KeyboardPanel(wx.Panel):
    def __init__(self, parent=None, obj=None):
        wx.Panel.__init__(self, parent, size=(900, 100), pos=(50, 500))
        self.obj = obj
        self.keyboard = Keyboard(self, -1, outFunction=self.obj._newNote, size=(900, 100))
        self.keyboard.hold = 0
        self.keyboard.SetFocus
        self.Show()
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def AcceptsFocus(self):
        return True

    def OnChar(self, event):
        pass
 
class AppGrid(wx.Panel):
 
    """Draw a line to a panel."""
 
    def __init__(self, parent=None):
        wx.Panel.__init__(self, parent, size=(1000,628), pos=(0,0))
        self.Bind(wx.EVT_PAINT, self.OnPaint)
 
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.BLACK, 4))
        dc.DrawLine(50, 50, 50, 497)
        dc.DrawLine(950, 50, 950, 497)
        dc.DrawLine(380, 50, 380, 497)
        dc.DrawLine(50, 50, 950, 50)
        dc.DrawLine(50, 497, 950, 497)
        dc.DrawLine(380, 290, 950, 290)
        dc.DrawLine(640, 50, 640, 290)
        dc.DrawLine(870, 50, 870, 290)
        #dc.DrawLine(780, 50, 780, 450)
        dc.SetPen(wx.Pen(wx.BLACK, 2))
        dc.DrawLine(75, 190, 365, 190)
        dc.DrawLine(75, 340, 365, 340)
        #dc.DrawLine(280, 250, 760, 250)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        pass

class OscControls(wx.Panel):
    def __init__(self, parent, ancor, osc, dsp, title) -> None:
        self.osc=osc
        self.dsp=dsp
        wx.Panel.__init__(self, parent, size=(300,150), pos=ancor)
        self._switch = wx.CheckBox(parent=self, pos = (0,0), label=title)
        self._switch.SetValue(True)
        self._waveforms=['Triangle', 'Saw', 'Square']
        self._waveform = wx.ComboBox(parent=self, pos=(0, 40), choices=self._waveforms, style=wx.CB_READONLY)
        #wx.StaticText(self, pos=(0,20), label='Waveform')
        self._octave = wx.Choice(parent=self, pos=(95, 40), choices=['-3', '-2', '-1', '0', '+1', '+2'])
        wx.StaticText(self, pos=(95,20), label='Oct')
        self._octave.SetSelection(3)
        self._detune = wx.Slider(parent=self, pos= (0, 80), minValue= -100, maxValue=100, style=wx.SL_VALUE_LABEL | wx.SL_BOTTOM, name= 'detune')
        wx.StaticText(self, pos=(0,76), label='Detune')
        self._volume = wx.Slider(parent=self, pos= (250, 17), minValue= 0, maxValue=10000, style=wx.SL_VERTICAL | wx.SL_INVERSE, size=(21, 100))
        wx.StaticText(self, pos=(220,59), label='Vol')
        self._volume.SetValue(5000)
        self.Bind(wx.EVT_CHECKBOX, self.OnOff)
        self.Bind(wx.EVT_COMBOBOX, self.changeWaveform)
        self.Bind(wx.EVT_CHOICE, self.changeOctave)
        self._volume.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeVolume)
        self._detune.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeDetune)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        pass


    def OnOff(self, event):
        if self._switch.IsChecked() == True:
            self.changeVolume(event)
        else:
            self.osc.osc.setMul(0)

    def changeWaveform(self, event):
        self.osc.setWaveform(self._waveforms.index(self._waveform.GetValue()))

    def changeOctave(self, event):
        self.osc.setOctave(int(event.GetString()))
    def changeDetune(self,event):
        self.osc.setDetune(self._detune.GetValue())

    def changeVolume(self, event):
        if self._switch.IsChecked() == True:
            vol = float(self._volume.GetValue()/10000)
            self.osc.setVolume(vol)
        
class NoiseOscControls(wx.Panel):
    def __init__(self, parent, ancor, oscNP, oscNW, dsp) -> None:
        self.oscNP=oscNP
        self.oscNW=oscNW
        self.dsp=dsp
        wx.Panel.__init__(self, parent, size=(210,150), pos=ancor)
        self._switch = wx.CheckBox(parent=self, pos = (0,0), label='Noise')
        self._switch.SetValue(False)
        self.OnOff(None)
        self._type = wx.ToggleButton(parent=self, pos=(0, 25), label='WHITE')
        self._volume = wx.Slider(parent=self, pos= (0, 70), minValue= 0, maxValue=10000, style=wx.SL_VALUE_LABEL | wx.SL_BOTTOM, name= 'volume')
        wx.StaticText(self, pos=(0,66), label='Volume')
        self.Bind(wx.EVT_CHECKBOX, self.OnOff)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.ChangeType)
        self.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeVolume)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        pass


    def OnOff(self, event):
        if self._switch.IsChecked() == True:
            self.changeVolume(event)
        else:
            self.oscNP.setMul(0)
            self.oscNW.setMul(0)

    def ChangeType(self, event):
        if self._type.GetValue() == True:
            self._type.SetLabel('PINK')
            self.changeVolume(None)
        else:
            self._type.SetLabel('WHITE')
            self.changeVolume(None)
    def changeVolume(self, event):
        if self._switch.IsChecked() == True:
            vol = float(self._volume.GetValue()/100000)
            if self._type.GetValue() == True:
                self.dsp.setPinkNoiseVolume(vol)
                self.dsp.setWhiteNoiseVolume(0)
            else:
                self.dsp.setPinkNoiseVolume(0)
                self.dsp.setWhiteNoiseVolume(vol)

class LoudnessContour(wx.Panel):
    def __init__(self, parent, ancor, dsp) -> None:
        wx.Panel.__init__(self, parent, size=(250,240), pos=ancor)
        self.dsp = dsp
        #self._Attack = wx.Slider(parent=self, pos= ( ), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Attack')
        self._Attack = PyoGuiControlSlider(parent=self, pos=(0,0), minvalue=0.1, maxvalue=100, orient= wx.VERTICAL, size=(30, 150))
        wx.StaticText(self, pos=(13,160), label='A')
        wx.StaticText(self, pos=(63,160), label='D')
        wx.StaticText(self, pos=(113,160), label='S')
        wx.StaticText(self, pos=(163,160), label='R')
        #self._Decay = wx.Slider(parent=self, pos= (40, ), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Decay')
        self._Decay = PyoGuiControlSlider(parent=self,pos=(50,0), minvalue=0.1, maxvalue=100, orient= wx.VERTICAL, size=(30, 150))
        #self._Sustain = wx.Slider(parent=self, pos= (80, ), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Sustain')
        self._Sustain = PyoGuiControlSlider(parent=self,pos=(100,0), minvalue=0, maxvalue=100, orient= wx.VERTICAL, size=(30, 150))
        self._Release = PyoGuiControlSlider(parent=self,pos=(150,0), minvalue=1, maxvalue=100, orient= wx.VERTICAL, size=(30, 150))
        self._Sustain.setValue(100)
        self._Attack.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self._Decay.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self._Sustain.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self._Release.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        pass


    def changeADSR(self, event):
        self.dsp.AmpEnv.setAttack(self._Attack.GetValue()/100)
        self.dsp.AmpEnv.setDecay(self._Decay.GetValue()/100)
        self.dsp.AmpEnv.setSustain(self._Sustain.GetValue()/100)
        self.dsp.AmpEnv.setRelease(self._Release.GetValue()/100)

class FilterControls(wx.Panel):
    def __init__(self, parent, ancor, filter) -> None:
        wx.Panel.__init__(self, parent, size=(500,150), pos=ancor)
        self.filter = filter
        '''
        self._Cutoff = wx.Slider(parent=self, pos= (0,0), minValue= 20, maxValue=20000, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Cutoff')
        self._Enphasis = wx.Slider(parent=self, pos= (40, 0), minValue= 0, maxValue=2000, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Enphasis')
        self._Ammount = wx.Slider(parent=self, pos= (80, 0), minValue= 0, maxValue=1000, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Ammount')
        self._Attack = wx.Slider(parent=self, pos= (0, 200), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Attack')
        self._Decay = wx.Slider(parent=self, pos= (40, 200), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Decay')
        self._Sustain = wx.Slider(parent=self, pos= (80, 200), minValue= 0, maxValue=100, style=wx.SL_VERTICAL|wx.SL_INVERSE, name= 'Sustain')
        '''
        self._Cutoff = PyoGuiControlSlider(parent=self, pos= (0,20), minvalue= 20, maxvalue=20000, log=True)
        wx.StaticText(self, pos=(0,0), label='Cutoff')
        self._Enphasis = PyoGuiControlSlider(parent=self, pos= (0, 70), minvalue= 1, maxvalue=1000, log=True)
        wx.StaticText(self, pos=(0,50), label='Resonance')
        self._Ammount = PyoGuiControlSlider(parent=self, pos= (0, 120), minvalue= 0, maxvalue=1000)
        wx.StaticText(self, pos=(0,100), label='Env Ammount')
        self._Attack = PyoGuiControlSlider(parent=self, pos= (250, 20), minvalue= 0, maxvalue=100)
        wx.StaticText(self, pos=(250,0), label='Attack')
        self._Decay = PyoGuiControlSlider(parent=self, pos= (250, 70), minvalue= 0, maxvalue=100)
        wx.StaticText(self, pos=(250,50), label='Decay')
        self._Sustain = PyoGuiControlSlider(parent=self, pos= (250, 120), minvalue= 0, maxvalue=100)
        wx.StaticText(self, pos=(250,100), label='Sustain')
        self._Cutoff.setValue(20000)
        self._Attack.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self._Decay.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self._Sustain.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeADSR)
        self._Enphasis.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeResonance)
        self._Cutoff.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeCutoff)
        self._Ammount.Bind(EVT_PYO_GUI_CONTROL_SLIDER, self.changeCutoff)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def OnChar(self, event):
        pass


    def changeADSR(self, event):
        self.filter.setEnv(self._Attack.GetValue()/100,
                           self._Decay.GetValue()/100,
                           self._Sustain.GetValue()/100)
        
    def changeResonance(self, event):
        self.filter.setRes(self._Enphasis.GetValue()/1000)

    def changeCutoff(self, event):
        self.filter.setFreq(self._Cutoff.GetValue(), self._Ammount.GetValue())

class MainVolume(wx.Panel):
    def __init__(self, parent ,ancor, dsp):
        wx.Panel.__init__(self,parent=parent, pos=ancor,size=(80,240))
        self._volume = wx.Slider(parent=self, pos=(29, 50), minValue= 0, maxValue=1000, style=wx.SL_VERTICAL | wx.SL_INVERSE, name= 'volume')
        wx.StaticText(self, pos=(15,20), label='Volume')
        self._volume.Bind(wx.EVT_COMMAND_SCROLL_THUMBTRACK, self.changeVolume)
        self._dsp =dsp
        self._volume.SetValue(1000)
    
    def changeVolume(self, evt):
        self._dsp.setMainVolume(self._volume.GetValue()/1000)

def startGUI(dsp):
    root = MainWindow()
    AppGrid(root)
    KeyboardPanel(parent=root, obj=dsp._notes)
    OscControls(root, (60, 60), dsp._osc1, dsp, 'OSC 1')
    OscControls(root, (60, 210), dsp._osc2, dsp, 'OSC 2')
    OscControls(root, (60, 360), dsp._osc3, dsp, 'OSC 3')
    LoudnessContour(root, (410, 100), dsp)
    FilterControls(root, (410, 340), dsp._filter)
    NoiseOscControls(root, (660, 100), dsp._oscNP, dsp._oscNW, dsp)
    wx.StaticText(root, pos=(450,70), label='Loudness Contour')
    wx.StaticText(root, pos=(600,290), label='Filter Controls')
    MainVolume(root, (870, 50), dsp)

    
    

