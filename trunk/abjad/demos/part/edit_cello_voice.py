# -*- encoding: utf-8 -*-
from abjad import *


def edit_cello_voice(score, durated_reservoir):

    voice = score['Cello Voice']
    descents = durated_reservoir['Cello']

    tie_chain = inspect(voice[-1]).get_tie_chain()
    for leaf in tie_chain.leaves:
        parent = leaf._get_parentage().parent
        index = parent.index(leaf)
        parent[index] = scoretools.Chord(['e,', 'a,'], leaf.written_duration)

    selection = voice[-len(descents[-1]):]
    unison_descent = mutate(selection).copy()
    voice.extend(unison_descent)
    for chord in unison_descent:
        index = inspect(chord).get_parentage().parent.index(chord)
        parent[index] = notetools.Note(
            chord.written_pitches[1], chord.written_duration)
        articulation = marktools.Articulation('accent')
        attach(articulation, parent[index])
        articulation = marktools.Articulation('tenuto')
        attach(articulation, parent[index])

    voice.extend('a,1. ~ a,2')
    voice.extend('b,1 ~ b,1. ~ b,1.')
    voice.extend('a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2')
    voice.extend('r4 r2.')
