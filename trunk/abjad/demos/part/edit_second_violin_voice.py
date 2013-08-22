# -*- encoding: utf-8 -*-
from abjad import *


def edit_second_violin_voice(score, durated_reservoir):

    voice = score['Second Violin Voice']
    descents = durated_reservoir['Second Violin']

    last_descent = selectiontools.select(descents[-1], contiguous=True)
    copied_descent = mutate(last_descent).copy()
    copied_descent = list(copied_descent)
    copied_descent[-1].written_duration = durationtools.Duration(1, 1)
    copied_descent.append(notetools.Note('a2'))
    for leaf in copied_descent:
        marktools.Articulation('accent')(leaf)
        marktools.Articulation('tenuto')(leaf)
    voice.extend(copied_descent)

    final_sustain = []
    for _ in range(32):
        final_sustain.append(notetools.Note('a1.'))
    final_sustain.append(notetools.Note('a2'))
    marktools.Articulation('accent')(final_sustain[0])
    marktools.Articulation('tenuto')(final_sustain[0])

    voice.extend(final_sustain)
    spannertools.TieSpanner(final_sustain)
    voice.extend('r4 r2.')
