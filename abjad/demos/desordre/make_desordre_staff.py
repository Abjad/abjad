# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.desordre.make_desordre_measure import make_desordre_measure


def make_desordre_staff(pitches):
    r'''Makes Désordre staff.
    '''

    staff = scoretools.Staff()
    for sequence in pitches:
        measure = make_desordre_measure(sequence)
        staff.append(measure)
    return staff