# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate


def move_measure_prolation_to_full_measure_tuplet(expr):
    '''Move measure prolation to full-measure tuplet.

    Turn non-power-of-two measures into power-of-two measures containing
    a single fixed-duration tuplet.

    Note that not all non-power-of-two measures can be made power-of-two.

    Returns None because processes potentially many measures.
    '''
    from abjad.tools import indicatortools
    from abjad.tools import scoretools

    for measure in iterate(expr).by_class(scoretools.Measure):
        effective_time_signature = measure.time_signature
        if effective_time_signature.has_non_power_of_two_denominator:

            # find time signature and contents multipliers
            time_signature_multiplier = effective_time_signature.implied_prolation
            contents_multiplier = \
                measure._get_likely_multiplier_of_components(measure[:])

            # update non-power-of-two time signature to power-of-two
            power_of_two_time_signature = effective_time_signature.with_power_of_two_denominator(
                contents_multiplier)
            detach(indicatortools.TimeSignature, measure)
            attach(power_of_two_time_signature, measure)

            # find target duration and create tuplet
            target_duration = time_signature_multiplier * measure._contents_duration
            tuplet = scoretools.FixedDurationTuplet(target_duration, measure[:])

            # scale tuplet contents, if helpful
            if contents_multiplier is not None:
                numerator = contents_multiplier.numerator
                denominator = contents_multiplier.denominator
                pair = (denominator, numerator)
                inverse_multiplier = durationtools.Multiplier(*pair)
                tuplet._scale_contents(inverse_multiplier)
