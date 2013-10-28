# -*- encoding: utf-8 -*-
from abjad import *


def edit_viola_voice(score, durated_reservoir):

    voice = score['Viola Voice']
    descents = durated_reservoir['Viola']

    for leaf in descents[-1]:
        articulation = marktools.Articulation('accent')
        articulation.attach(leaf)
        articulation = marktools.Articulation('tenuto')
        articulation.attach(leaf)
    last_descent = selectiontools.select(descents[-1], contiguous=True)
    copied_descent = mutate(last_descent).copy()
    for leaf in copied_descent:
        if leaf.written_duration == durationtools.Duration(4, 4):
            leaf.written_duration = durationtools.Duration(8, 4)
        else:
            leaf.written_duration = durationtools.Duration(4, 4)
    voice.extend(copied_descent)

    bridge = notetools.Note('e1')
    articulation = marktools.Articulation('tenuto')
    articulation.attach(bridge)
    articulation = marktools.Articulation('accent')
    articulation.attach(bridge)
    voice.append(bridge)

    final_sustain_rhythm = [(6, 4)] * 21 + [(1, 2)]
    final_sustain_notes = notetools.make_notes(['e'], final_sustain_rhythm)
    articulation = marktools.Articulation('accent')
    articulation.attach(final_sustain_notes[0])
    articulation = marktools.Articulation('tenuto')
    articulation.attach(final_sustain_notes[0])
    voice.extend(final_sustain_notes)
    tie = spannertools.TieSpanner()
    tie.attach(final_sustain_notes)
    voice.extend('r4 r2.')
