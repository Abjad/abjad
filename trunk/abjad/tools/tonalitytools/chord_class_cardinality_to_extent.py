from abjad.exceptions import TonalHarmonyError


def chord_class_cardinality_to_extent(cardinality):
    '''..versionadded:: 2.0

    Change integer chord class `cardinality` to integer chord class extent::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> tonalitytools.chord_class_cardinality_to_extent(4)
        7

    The function above indicates that a tertian chord with 4 unique
    pitches qualifies as a seventh chord.
    '''

    cardinality_to_extent = {
        3: 5,
        4: 7,
        5: 9,
        6: 11,
        7: 13
    }

    if not isinstance(cardinality, int):
        raise TypeError('chord class cardinality must be int: %s' % cardinality)

    try:
        extent = cardinality_to_extent[cardinality]
    except KeyError:
        raise TonalHarmonyError('unknown chord class cardinality: %s' %
            cardinality)

    return extent
