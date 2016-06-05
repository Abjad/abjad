# -*- coding: utf-8 -*-
import abjad
from abjad.tools import mathtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import inspect_


def make_desordre_measure(pitches):
    '''Makes a measure composed of *Désordre cells*.

    `pitches` is a list of lists of number (e.g., [[1, 2, 3], [2, 3, 4]])

    The function returns a measure.
    '''

    for sequence in pitches:
        container = abjad.demos.desordre.make_desordre_cell(sequence)
        time_signature = inspect_(container).get_duration()
        time_signature = mathtools.NonreducedFraction(time_signature)
        time_signature = time_signature.with_denominator(8)
        measure = scoretools.Measure(time_signature, [container])

    return measure