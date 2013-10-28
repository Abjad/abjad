# -*- encoding: utf-8 -*-
from abjad import *


def apply_rehearsal_marks(score):

    bell_voice = score['Bell Voice']

    measure_indices = [
        6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84,
        90, 96, 102,
        ]

    for measure_index in measure_indices:
        command = marktools.LilyPondCommandMark(r'mark \default', 'before')
        command.attach(bell_voice[measure_index])
