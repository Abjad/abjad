# -*- encoding: utf-8 -*-
from abjad.tools import componenttools
from abjad.tools import notetools
from abjad.tools import selectiontools
from abjad.tools import spannertools


def edit_first_violin_voice(score, durated_reservoir):

    voice = score['First Violin Voice']
    descents = durated_reservoir['First Violin']
    descents = selectiontools.ContiguousSelection(descents)

    last_descent = selectiontools.ContiguousSelection(descents[-1])
    copied_descent = last_descent.copy_and_detach_spanners()

    voice.extend(copied_descent)

    final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    final_sustain_notes = notetools.make_notes(["c'"], final_sustain_rhythm)
    voice.extend(final_sustain_notes)
    spannertools.TieSpanner(final_sustain_notes)
    voice.extend('r4 r2.')
