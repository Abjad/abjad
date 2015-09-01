# -*- coding: utf-8 -*-
'''
Abjad-IPython Extension
-----------------------

Integrates audio and visual rendering of Abjad scores in IPython notebooks.

This extension requires `fluidsynth` be in your $PATH. If you do not have
`fluidsynth` installed, it is likely available in your platform's package
manager:

On OSX::

    ~$ brew install fluidsynth --with-libsndfile
    ~$ sudo port install fluidsynth

On Debian or Ubuntu:

    ~$ apt-get install fluidsynth

To activate the IPython notebook extension, add the following line in your
notebook:

    %load_ext abjad.ext.ipython

'''

def load_ipython_extension(ipython):
    import abjad
    from abjad.tools import ipythontools
    from abjad.tools import topleveltools
    ipythontools.IPythonConfiguration()
    play = ipythontools.Play()
    show = ipythontools.Show()
    abjad.play = play
    abjad.show = show
    topleveltools.play = play
    topleveltools.show = show
    names = {
        'load_sound_font': play.load_sound_font,
        'play': play,
        'show': show,
        }
    ipython.push(names)