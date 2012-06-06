def list_checks():
    '''.. versionadded:: 2.8

    List checks::

        >>> from abjad.tools import wellformednesstools

    ::

        >>> for check in wellformednesstools.list_checks(): check
        ... 
        BeamedQuarterNoteCheck()
        DiscontiguousSpannerCheck()
        DuplicateIdCheck()
        EmptyContainerCheck()
        IntermarkedHairpinCheck()
        MisduratedMeasureCheck()
        MisfilledMeasureCheck()
        MispitchedTieCheck()
        MisrepresentedFlagCheck()
        MissingParentCheck()
        NestedMeasureCheck()
        OverlappingBeamCheck()
        OverlappingGlissandoCheck()
        OverlappingOctavationCheck()
        ShortHairpinCheck()

    Return list of checks.
    '''
    from abjad.tools import wellformednesstools
    
    result = []
    for name in dir(wellformednesstools):
        if not name == 'Check':
            if name[0].isupper():
                exec('check = wellformednesstools.{}()'.format(name))
                result.append(check)
    return result
