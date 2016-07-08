# -*- coding: utf-8 -*-
import math
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import select


def make_desordre_cell(pitches):
    '''The function constructs and returns a *Désordre cell*.
    `pitches` is a list of numbers or, more generally, pitch tokens.
    '''

    notes = [scoretools.Note(pitch, (1, 8)) for pitch in pitches]
    beam = spannertools.Beam()
    attach(beam, notes)
    slur = spannertools.Slur()
    attach(slur, notes)
    clef = indicatortools.Dynamic('f')
    attach(clef, notes[0])
    dynamic = indicatortools.Dynamic('p')
    attach(dynamic, notes[1])

    # make the lower voice
    lower_voice = scoretools.Voice(notes)
    lower_voice.name = 'RH Lower Voice'
    command = indicatortools.LilyPondCommand('voiceTwo')
    attach(command, lower_voice)
    n = int(math.ceil(len(pitches) / 2.))
    chord = scoretools.Chord([pitches[0], pitches[0] + 12], (n, 8))
    articulation = indicatortools.Articulation('>')
    attach(articulation, chord)

    # make the upper voice
    upper_voice = scoretools.Voice([chord])
    upper_voice.name = 'RH Upper Voice'
    command = indicatortools.LilyPondCommand('voiceOne')
    attach(command, upper_voice)

    # combine them together
    container = scoretools.Container([lower_voice, upper_voice])
    container.is_simultaneous = True

    # make all 1/8 beats breakable
    leaves = select(lower_voice).by_leaf()
    for leaf in leaves[:-1]:
        bar_line = indicatortools.BarLine('')
        attach(bar_line, leaf)

    return container
