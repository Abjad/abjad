# -*- coding: utf-8 -*-
import abjad


def edit_cello_voice(score, durated_reservoir):
    r'''Edits cello voice.
    '''

    voice = score['Cello Voice']
    descents = durated_reservoir['Cello']

    logical_tie = abjad.inspect(voice[-1]).get_logical_tie()
    for leaf in logical_tie.leaves:
        parent = leaf._get_parentage().parent
        index = parent.index(leaf)
        parent[index] = abjad.Chord(['e,', 'a,'], leaf.written_duration)

    selection = voice[-len(descents[-1]):]
    unison_descent = abjad.mutate(selection).copy()
    voice.extend(unison_descent)
    for chord in unison_descent:
        index = abjad.inspect(chord).get_parentage().parent.index(chord)
        parent[index] = abjad.Note(
            chord.written_pitches[1], chord.written_duration)
        articulation = abjad.Articulation('accent')
        abjad.attach(articulation, parent[index])
        articulation = abjad.Articulation('tenuto')
        abjad.attach(articulation, parent[index])

    voice.extend('a,1. ~ a,2')
    voice.extend('b,1 ~ b,1. ~ b,1.')
    voice.extend('a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2')
    voice.extend('r4 r2.')
