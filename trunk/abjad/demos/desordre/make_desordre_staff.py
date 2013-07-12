# -*- encoding: utf-8 -*-
from abjad.tools import stafftools
from abjad.demos.desordre.make_desordre_measure import make_desordre_measure


def make_desordre_staff(pitches):
    staff = stafftools.Staff()
    for sequence in pitches:
        measure = make_desordre_measure(sequence)
        staff.append(measure)
    return staff
