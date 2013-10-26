# -*- encoding: utf-8 -*-
import math
from abjad import *


def make_desordre_cell(pitches):
    '''The function constructs and returns a *Désordre cell*.
    `pitches` is a list of numbers or, more generally, pitch tokens.
    '''
    notes = [notetools.Note(pitch, (1, 8)) for pitch in pitches]
    beam = spannertools.BeamSpanner()
    beam.attach(notes)
    slur = spannertools.SlurSpanner()
    slur.attach(notes)
    clef = contexttools.DynamicMark('f')
    clef.attach(notes[0])
    dynamic = contexttools.DynamicMark('p')
    dynamic.attach(notes[1])

    # make the lower voice
    lower_voice = voicetools.Voice(notes)
    lower_voice.name = 'RH Lower Voice'
    command = marktools.LilyPondCommandMark('voiceTwo')
    command.attach(lower_voice)
    n = int(math.ceil(len(pitches) / 2.))
    chord = chordtools.Chord([pitches[0], pitches[0] + 12], (n, 8))
    articulation = marktools.Articulation('>')
    articulation.attach(chord)

    # make the upper voice
    upper_voice = voicetools.Voice([chord])
    upper_voice.name = 'RH Upper Voice'
    command = marktools.LilyPondCommandMark('voiceOne')
    command.attach(upper_voice)

    # combine them together
    container = containertools.Container([lower_voice, upper_voice])
    container.is_simultaneous = True

    # make all 1/8 beats breakable
    for leaf in lower_voice.select_leaves()[:-1]:
        bar_line = marktools.BarLine('')
        bar_line.attach(leaf)

    return container
