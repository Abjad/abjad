# -*- encoding: utf-8 -*-
from abjad import *


def edit_first_violin_voice(score, durated_reservoir):
    r'''Edits first violin voice.
    '''

    voice = score['First Violin Voice']
    descents = durated_reservoir['First Violin']
    descents = selectiontools.ContiguousSelection(descents)

    last_descent = select(descents[-1], contiguous=True)
    copied_descent = mutate(last_descent).copy()
    voice.extend(copied_descent)

    final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    final_sustain_notes = scoretools.make_notes(["c'"], final_sustain_rhythm)
    voice.extend(final_sustain_notes)
    tie = spannertools.Tie()
    attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')