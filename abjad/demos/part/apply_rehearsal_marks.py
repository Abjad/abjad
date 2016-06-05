# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools.topleveltools import attach


def apply_rehearsal_marks(score):
    r'''Applies rehearsal marks to score.
    '''

    bell_voice = score['Bell Voice']

    measure_indices = [
        6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84,
        90, 96, 102,
        ]

    for measure_index in measure_indices:
        command = indicatortools.LilyPondCommand(r'mark \default', 'before')
        attach(command, bell_voice[measure_index])