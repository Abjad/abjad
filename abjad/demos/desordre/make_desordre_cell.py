# -*- encoding: utf-8 -*-
import math
from abjad import *


def make_desordre_cell(pitches):
    '''The function constructs and returns a *Désordre cell*.
    `pitches` is a list of numbers or, more generally, pitch tokens.
    '''
    notes = [scoretools.Note(pitch, (1, 8)) for pitch in pitches]
    beam = spannertools.BeamSpanner()
    attach(beam, notes)
    slur = spannertools.SlurSpanner()
    attach(slur, notes)
    clef = marktools.Dynamic('f')
    attach(clef, notes[0])
    dynamic = marktools.Dynamic('p')
    attach(dynamic, notes[1])

    # make the lower voice
    lower_voice = scoretools.Voice(notes)
    lower_voice.name = 'RH Lower Voice'
    command = marktools.LilyPondCommandMark('voiceTwo')
    attach(command, lower_voice)
    n = int(math.ceil(len(pitches) / 2.))
    chord = scoretools.Chord([pitches[0], pitches[0] + 12], (n, 8))
    articulation = marktools.Articulation('>')
    attach(articulation, chord)

    # make the upper voice
    upper_voice = scoretools.Voice([chord])
    upper_voice.name = 'RH Upper Voice'
    command = marktools.LilyPondCommandMark('voiceOne')
    attach(command, upper_voice)

    # combine them together
    container = scoretools.Container([lower_voice, upper_voice])
    container.is_simultaneous = True

    # make all 1/8 beats breakable
    for leaf in lower_voice.select_leaves()[:-1]:
        bar_line = marktools.BarLine('')
        attach(bar_line, leaf)

    return container
