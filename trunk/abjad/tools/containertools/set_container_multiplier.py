from abjad.tools import durationtools


# TODO: reimplement as settable attribute of container duration interface.
def set_container_multiplier(container, multiplier):
    r'''Set `container` `multiplier`::

        >>> tuplet = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    ::

        >>> f(tuplet)
        \times 2/3 {
            c'8
            d'8
            e'8
        }

    ::

        >>> containertools.set_container_multiplier(tuplet, Multiplier(3, 4))

    ::

        >>> f(tuplet)
        \fraction \times 3/4 {
            c'8
            d'8
            e'8
        }

    Return none.
    '''
    from abjad.tools import contexttools
    from abjad.tools import measuretools
    from abjad.tools import tuplettools

    # check input
    if multiplier is not None:
        multiplier = durationtools.Multiplier(multiplier)

    if isinstance(container, tuplettools.FixedDurationTuplet):
        container.target_duration = multiplier * container.contents_duration
    elif isinstance(container, tuplettools.Tuplet):
        container.multiplier = multiplier
    elif isinstance(container, measuretools.Measure):
        new_duration = multiplier * container.contents_duration
        new_time_signature = contexttools.TimeSignatureMark(new_duration)
        contexttools.detach_time_signature_marks_attached_to_component(container)
        new_time_signature.attach(container)
