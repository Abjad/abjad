# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import mutate


def edit_cello_voice(score, durated_reservoir):
    r'''Edits cello voice.
    '''

    voice = score['Cello Voice']
    descents = durated_reservoir['Cello']

    logical_tie = inspect_(voice[-1]).get_logical_tie()
    for leaf in logical_tie.leaves:
        parent = leaf._get_parentage().parent
        index = parent.index(leaf)
        parent[index] = scoretools.Chord(['e,', 'a,'], leaf.written_duration)

    selection = voice[-len(descents[-1]):]
    unison_descent = mutate(selection).copy()
    voice.extend(unison_descent)
    for chord in unison_descent:
        index = inspect_(chord).get_parentage().parent.index(chord)
        parent[index] = scoretools.Note(
            chord.written_pitches[1], chord.written_duration)
        articulation = indicatortools.Articulation('accent')
        attach(articulation, parent[index])
        articulation = indicatortools.Articulation('tenuto')
        attach(articulation, parent[index])

    voice.extend('a,1. ~ a,2')
    voice.extend('b,1 ~ b,1. ~ b,1.')
    voice.extend('a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2')
    voice.extend('r4 r2.')