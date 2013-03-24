# -*- encoding: utf-8 -*-
import math
from abjad import *


def make_desordre_cell(pitches):
    '''The function constructs and returns a *Désordre cell*.
    `pitches` is a list of numbers or, more generally, pitch tokens.
    '''
    notes = [Note(pitch, (1, 8)) for pitch in pitches]
    beamtools.BeamSpanner(notes)
    spannertools.SlurSpanner(notes)
    contexttools.DynamicMark('f')(notes[0])
    contexttools.DynamicMark('p')(notes[1])

    # make the lower voice
    lower_voice = Voice(notes)
    lower_voice.name = 'RH Lower Voice'
    marktools.LilyPondCommandMark('voiceTwo')(lower_voice)
    n = int(math.ceil(len(pitches) / 2.))
    chord = Chord([pitches[0], pitches[0] + 12], (n, 8))
    marktools.Articulation('>')(chord)

    # make the upper voice
    upper_voice = Voice([chord])
    upper_voice.name = 'RH Upper Voice'
    marktools.LilyPondCommandMark('voiceOne')(upper_voice)

    # combine them together
    container = Container([lower_voice, upper_voice])
    container.is_parallel = True

    # make all 1/8 beats breakable
    for leaf in lower_voice.leaves[:-1]:
        marktools.BarLine('')(leaf)

    return container
