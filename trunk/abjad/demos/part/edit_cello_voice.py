# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import chordtools
from abjad.tools import marktools
from abjad.tools import notetools


def edit_cello_voice(score, durated_reservoir):

    voice = score['Cello Voice']
    descents = durated_reservoir['Cello']

    tie_chain = voice[-1].select_tie_chain()
    for leaf in tie_chain.leaves:
        parent = leaf.parent
        index = parent.index(leaf)
        parent[index] = chordtools.Chord(['e,', 'a,'], leaf.written_duration)

    unison_descent = componenttools.copy_components_and_detach_spanners(
        voice[-len(descents[-1]):])
    voice.extend(unison_descent)
    for chord in unison_descent:
        index = chord.parent.index(chord)
        parent[index] = notetools.Note(
            chord.written_pitches[1], chord.written_duration)
        marktools.Articulation('accent')(parent[index])
        marktools.Articulation('tenuto')(parent[index])

    voice.extend('a,1. ~ a,2 b,1 ~ b,1. ~ b,1. a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2 r4 r2.')
