from abjad.exceptions import TonalHarmonyError


def chord_class_extent_to_cardinality(extent):
    '''..versionadded:: 2.0

    Change integer chord class `extent` to integer chord class cardinality::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> tonalitytools.chord_class_extent_to_cardinality(7)
        4

    The call above shows that a seventh chord comprises 4 unique pitch-classes.
    '''

    cardinality_to_extent = {
        5: 3,
        7: 4,
        9: 5,
        11: 6,
        13: 7
    }

    if not isinstance(extent, int):
        raise TypeError('chord class extent must be int: %s' % extent)

    try:
        cardinality = cardinality_to_extent[extent]
    except KeyError:
        raise TonalHarmonyError('unknown chord class extent: %s' %
            extent)

    return cardinality
