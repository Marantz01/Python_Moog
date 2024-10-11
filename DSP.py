
from pyo import*

class MoogOsc():
    #Oscillatore Moog
    def __init__(self, dsp, freqs):
        self._dsp = dsp
        #coefficente di detuning
        self._detune = 1
        #coefficiente moltiplicate la frequenza dell'oscillatore per fornire uno switch dinamico di ottava
        self._oct = 0
        #Possibili waveforms asegnabili all'oscillatore
        self._waveforms = [TriangleTable(order=1000).normalize(),
                       SawTable(order=1000).normalize(),
                       SquareTable(order=1000).normalize()]
        self.osc = Osc(table=self._waveforms[0], 
                       freq=self._dsp._freqs)
        self.setVolume(0.5)
        
    def setWaveform(self, windex):
        #replace attributo table di Osc()
        self.osc.setTable(self._waveforms[windex])

    def setOctave(self, oct):
        #cambio di ottava
        self._oct = oct
        self.osc.setFreq((self._dsp._freqs*(2**oct))*self._detune)
    
    def setDetune(self, det):
        #replace dell'attributo detune
        self._detune = 2**((det/100)*0.8/12)
        self.osc.setFreq((self._dsp._freqs*(2**self._oct))*self._detune)

    
    def setVolume(self, vol):
        self.osc.setMul(0.1*vol*self._dsp.AmpEnv)

class Moogfilter(MoogLP):
    #implementazione della classe Moogfilter(filtro passa-basso 24db)
    def __init__(self, envinput, input):
        #inviluppo ADSR per modulare la frequenza di taglio
        self._filterEnv = MidiAdsr(input = envinput, attack=.1, decay=.5, sustain=0)
        #coefficiente di modulazione della frequenza di taglio
        self._AmmountofContour = 100
        #frequenza di taglio
        self._FixedFrequency = 100
        self._filterfreq=self._FixedFrequency*(1+(self._AmmountofContour*self._filterEnv))
        #costruttore MoogLP
        MoogLP.__init__(self, input=input, freq=self._filterfreq)
    
    def setFreq(self, fix, amt):
        #Replace del parametro freq dell'oggetto MoogLP
        self._FixedFrequency = fix
        self._AmmountofContour = amt
        self._filterfreq=(self._FixedFrequency*(1+(self._AmmountofContour*self._filterEnv)))
        x = self._filterfreq
        return super().setFreq(x)
    
    def setEnv(self, a, d, s):
        #Replace dei parametri ADS dell'inviluppo modulante la frequanza di taglio
        self._filterEnv.setAttack(a)
        self._filterEnv.setDecay(d)
        self._filterEnv.setSustain(s)
        
class MiniMoogDSP():
    def __init__(self):
        self._notes = Notein(scale=1)
        self._freqs = self._notes["pitch"]
        self.AmpEnv = MidiAdsr(self._notes["velocity"], attack=.3, sustain=1, release=0.3)
        self.osc1 = MoogOsc(freqs=self._freqs,dsp=self)
        self.osc2 = MoogOsc(freqs=self._freqs,dsp=self)
        self.osc3 = MoogOsc(freqs=self._freqs,dsp=self)
        self.oscNP = PinkNoise(mul=0.1*self.AmpEnv) #oscillatore Pink noise
        self.oscNW = Noise(mul=0.1*self.AmpEnv) #oscillatore White noise
        #mix dei segnali provenienti dagli oscillatori
        self._oscillatorsmix = Mix([self.osc1.osc, self.osc2.osc, self.osc3.osc, self.oscNP, self.oscNW], voices=1)
        self.filter = Moogfilter(self._notes["velocity"],self._oscillatorsmix)
        #output stereofonico
        self._outSig = Mix(self.filter, voices=1)
        self._p = Pan(self._outSig, outs=2, pan=0.5).out()

    def setMainVolume(self, vol):
        #set del volume generale del synth
        self._p.setMul(vol)
    
    def setPinkNoiseVolume(self, vol):
        self.oscNP.setMul(0.1*vol*self.AmpEnv)
    
    def setWhiteNoiseVolume(self, vol):
        self.oscNW.setMul(0.1*vol*self.AmpEnv)
    


    
    
    
    