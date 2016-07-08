# -*- coding: utf-8 -*-
'''
Abjad-IPython Extension
-----------------------

Integrates audio and visual rendering of Abjad scores in IPython notebooks.

This extension requires `timidity` be in your $PATH. If you do not have
`timidity` installed, it is likely available in your platform's package
manager:

On OSX::

    ~$ brew install timidity

On Debian or Ubuntu:

    ~$ apt-get install timidity

To activate the IPython notebook extension, add the following line in your
notebook:

    %load_ext abjad.ext.ipython

'''


def load_ipython_extension(ipython):
    import abjad
    from abjad.tools import ipythontools
    from abjad.tools import topleveltools
    play = ipythontools.Play()
    show = ipythontools.Show()
    graph = ipythontools.Graph()
    abjad.play = play
    abjad.show = show
    abjad.graph = graph
    topleveltools.play = play
    topleveltools.show = show
    topleveltools.graph = graph
    names = {
        'play': play,
        'show': show,
        'graph': graph,
        }
    ipython.push(names)
