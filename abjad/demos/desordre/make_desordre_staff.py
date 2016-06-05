# -*- coding: utf-8 -*-
import abjad
from abjad.tools import scoretools


def make_desordre_staff(pitches):
    r'''Makes Désordre staff.
    '''

    staff = scoretools.Staff()
    for sequence in pitches:
        measure = abjad.demos.desordre.make_desordre_measure(sequence)
        staff.append(measure)
    return staff