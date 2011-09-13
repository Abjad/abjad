from abjad.tools import mathtools
from abjad.tools import timesignaturetools
from abjad.tools.measuretools.iterate_measures_forward_in_expr import iterate_measures_forward_in_expr
from abjad.tools import durationtools



def move_measure_prolation_to_full_measure_tuplet(expr):
    '''.. versionadded:: 2.0

    Move measure prolation to full-measure tuplet.

    Turn nonbinary measures into binary measures containing a single fixed-duration tuplet.

    This is the inverse of measuretools.move_prolation_of_full_measure_tuplet_to_meter_of_measure().

    Note that not all nonbinary measures can be made binary.

    Returns None because processes potentially many measures.

    .. versionchanged:: 2.0
        renamed ``measuretools.project()`` to
        ``measuretools.move_measure_prolation_to_full_measure_tuplet()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import contexttools
    from abjad.tools import containertools
    from abjad.tools.tuplettools.FixedDurationTuplet import FixedDurationTuplet

    for measure in iterate_measures_forward_in_expr(expr):
        if contexttools.get_effective_time_signature(measure).is_nonbinary:

            # find meter and contents multipliers
            meter_multiplier = contexttools.get_effective_time_signature(measure).multiplier
            contents_multiplier = componenttools.get_likely_multiplier_of_components(measure[:])

            # update nonbinary meter to binary
            binary_meter = timesignaturetools.time_signature_to_binary_time_signature(
                contexttools.get_effective_time_signature(measure), contents_multiplier)
            contexttools.detach_time_signature_marks_attached_to_component(measure)
            binary_meter.attach(measure)

            # find target duration and create tuplet
            target_duration = meter_multiplier * measure.contents_duration
            tuplet = FixedDurationTuplet(target_duration, measure[:])

            # scale tuplet contents, if helpful
            if contents_multiplier is not None:
                #containertools.scale_contents_of_container(tuplet, ~contents_multiplier)
                inverse_multiplier = durationtools.Duration(
                    contents_multiplier.denominator, contents_multiplier.numerator)
                containertools.scale_contents_of_container(tuplet, inverse_multiplier)
