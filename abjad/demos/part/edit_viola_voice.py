# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import select


def edit_viola_voice(score, durated_reservoir):
    r'''Edits viola voice.
    '''

    voice = score['Viola Voice']
    descents = durated_reservoir['Viola']

    for leaf in descents[-1]:
        articulation = indicatortools.Articulation('accent')
        attach(articulation, leaf)
        articulation = indicatortools.Articulation('tenuto')
        attach(articulation, leaf)
    last_descent = select(descents[-1])
    copied_descent = mutate(last_descent).copy()
    for leaf in copied_descent:
        if leaf.written_duration == durationtools.Duration(4, 4):
            leaf.written_duration = durationtools.Duration(8, 4)
        else:
            leaf.written_duration = durationtools.Duration(4, 4)
    voice.extend(copied_descent)

    bridge = scoretools.Note('e1')
    articulation = indicatortools.Articulation('tenuto')
    attach(articulation, bridge)
    articulation = indicatortools.Articulation('accent')
    attach(articulation, bridge)
    voice.append(bridge)

    final_sustain_rhythm = [(6, 4)] * 21 + [(1, 2)]
    final_sustain_notes = scoretools.make_notes(['e'], final_sustain_rhythm)
    articulation = indicatortools.Articulation('accent')
    attach(articulation, final_sustain_notes[0])
    articulation = indicatortools.Articulation('tenuto')
    attach(articulation, final_sustain_notes[0])
    voice.extend(final_sustain_notes)
    tie = spannertools.Tie()
    attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')