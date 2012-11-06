import copy
from abjad.tools import notetools
from abjad.tools import tietools


def apply_first_violin_edits(score, durated_reservoir):

    voice = score['First Violin Voice']
    descents = durated_reservoir['First Violin']

    copied_descent = copy.deepcopy(descents[-1])
    voice.extend(copied_descent)

    final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    final_sustain_notes = notetools.make_notes(["c'"], final_sustain_rhythm)
    voice.extend(final_sustain_notes)
    tietools.TieSpanner(final_sustain_notes)
    voice.extend('r4 r2.')
