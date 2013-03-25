# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.desordre.make_desordre_cell import make_desordre_cell


def make_desordre_measure(pitches):
    '''Constructs a measure composed of *Désordre cells*.

    `pitches` is a list of lists of number (e.g., [[1, 2, 3], [2, 3, 4]])

    The function returns a measure.
    '''

    for sequence in pitches:
        container = make_desordre_cell(sequence)
        time_signature = container.duration
        time_signature = mathtools.NonreducedFraction(time_signature)
        time_signature = time_signature.with_denominator(8)
        measure = Measure(time_signature, [container])

    return measure
