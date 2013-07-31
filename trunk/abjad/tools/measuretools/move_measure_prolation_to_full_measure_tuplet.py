# -*- encoding: utf-8 -*-
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import mathtools


def move_measure_prolation_to_full_measure_tuplet(expr):
    '''.. versionadded:: 2.0

    Move measure prolation to full-measure tuplet.

    Turn non-power-of-two measures into power-of-two measures containing
    a single fixed-duration tuplet.

    Note that not all non-power-of-two measures can be made power-of-two.

    Returns None because processes potentially many measures.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools
    from abjad.tools import measuretools
    from abjad.tools import timesignaturetools
    from abjad.tools import tuplettools

    for measure in iterationtools.iterate_measures_in_expr(expr):
        effective_time_signature = measure.get_effective_context_mark(
            contexttools.TimeSignatureMark)
        if effective_time_signature.has_non_power_of_two_denominator:

            # find time signature and contents multipliers
            time_signature_multiplier = effective_time_signature.implied_prolation
            contents_multiplier = measuretools.get_likely_multiplier_of_components(measure[:])

            # update non-power-of-two time signature to power-of-two
            power_of_two_time_signature = effective_time_signature.with_power_of_two_denominator(
                contents_multiplier)
            measure.select().detach_marks(contexttools.TimeSignatureMark)
            power_of_two_time_signature.attach(measure)

            # find target duration and create tuplet
            target_duration = time_signature_multiplier * measure.contents_duration
            tuplet = tuplettools.FixedDurationTuplet(target_duration, measure[:])

            # scale tuplet contents, if helpful
            if contents_multiplier is not None:
                #containertools.scale_contents_of_container(tuplet, ~contents_multiplier)
                inverse_multiplier = durationtools.Duration(
                    contents_multiplier.denominator, contents_multiplier.numerator)
                containertools.scale_contents_of_container(tuplet, inverse_multiplier)
