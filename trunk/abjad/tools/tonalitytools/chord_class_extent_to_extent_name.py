def chord_class_extent_to_extent_name(extent):
    '''.. versionadded:: 2.0

    Change integer chord class `extent` to extent name. ::

        abjad> from abjad.tools import tonalitytools

    ::

        abjad> tonalitytools.chord_class_extent_to_extent_name(7)
        'seventh'

    The call above shows that a tertian chord subtending 7 staff spaces
    qualifies as a seventh chord.
    '''

    if not isinstance(extent, int):
        raise TypeError('chord class extent must be int: %s' % extent)

    extent_to_extent_name = {
        5: 'triad',
        7: 'seventh',
        9: 'ninth',
        11: 'eleventh',
        13: 'thirteenth'
    }

    try:
        extent_name = extent_to_extent_name[extent]
    except KeyError:
        raise TonalHarmonyError('unknown chord class extent: %s' % extent)

    return extent_name
