from pyo import*

s = Server().boot().start()
osc = Noise().out()

Spectrum(osc)
s.gui(locals())