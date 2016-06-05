# -*- coding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import spannertools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import mutate
from abjad.tools.topleveltools import select


def edit_first_violin_voice(score, durated_reservoir):
    r'''Edits first violin voice.
    '''

    voice = score['First Violin Voice']
    descents = durated_reservoir['First Violin']
    descents = selectiontools.Selection(descents)

    last_descent = select(descents[-1])
    copied_descent = mutate(last_descent).copy()
    voice.extend(copied_descent)

    final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    final_sustain_notes = scoretools.make_notes(["c'"], final_sustain_rhythm)
    voice.extend(final_sustain_notes)
    tie = spannertools.Tie()
    attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')