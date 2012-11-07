# -*- encoding: utf-8 -*-
from abjad import *
from abjad.demos.desordre.make_desordre_cell import make_desordre_cell


def make_desordre_measure(pitches):
    '''Constructs a measure composed of *Désordre cells*.
    `pitches` is a list of lists of number (e.g., [[1, 2, 3], [2, 3, 4]])
    The function returns a DynamicMeasure.
    '''
    measure = measuretools.DynamicMeasure([ ])
    for sequence in pitches:
        measure.append(make_desordre_cell(sequence))

    # make denominator 8
    if contexttools.get_effective_time_signature(measure).denominator == 1:
        measure.denominator = 8

    return measure
