# -*- coding: utf-8 -*-
import abjad


def make_desordre_staff(pitches):
    r'''Makes Désordre staff.
    '''

    staff = abjad.Staff()
    for sequence in pitches:
        measure = abjad.demos.desordre.make_desordre_measure(sequence)
        staff.append(measure)
    return staff
