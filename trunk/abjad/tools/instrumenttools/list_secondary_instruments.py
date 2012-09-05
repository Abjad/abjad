def list_secondary_instruments():
    r'''.. versionadded:: 2.5

    List secondary instruments::

        >>> for secondary_instrument in instrumenttools.list_secondary_instruments()[:5]:
        ...     secondary_instrument
        ... 
        <class 'abjad.tools.instrumenttools.AltoFlute.AltoFlute.AltoFlute'>
        <class 'abjad.tools.instrumenttools.AltoTrombone.AltoTrombone.AltoTrombone'>
        <class 'abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone.BaritoneSaxophone'>
        <class 'abjad.tools.instrumenttools.BassClarinet.BassClarinet.BassClarinet'>
        <class 'abjad.tools.instrumenttools.BassFlute.BassFlute.BassFlute'>

    Return list
    '''
    from abjad.tools import instrumenttools

    secondary_instruments = []

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()
        if instrument.is_secondary_instrument:
            secondary_instruments.append(instrument_class)

    return secondary_instruments        
