def default_instrument_name_to_instrument_class(default_instrument_name):
    r'''.. versionadded:: 2.5

    Change `default_instrument_name` to class name::

        >>> instrumenttools.default_instrument_name_to_instrument_class('clarinet in E-flat')
        <class 'abjad.tools.instrumenttools.EFlatClarinet.EFlatClarinet.EFlatClarinet'>

    Return class.

    When `default_instrument_name` matches no instrument class::

        >>> instrumenttools.default_instrument_name_to_instrument_class('foo') is None
        True

    Return none.
    '''
    from abjad.tools import instrumenttools

    for instrument_class in instrumenttools.list_instruments():
        instrument = instrument_class()
        if instrument.default_instrument_name == default_instrument_name:
            return instrument_class
