from abjad.tools.instrumenttools.list_instruments import list_instruments


def default_instrument_name_to_instrument_class(default_instrument_name):
    r'''.. versionadded:: 2.5

    Change `default_instrument_name` to class name::

        abjad> instrumenttools.default_instrument_name_to_instrument_class('clarinet in E-flat')
        <class 'abjad.tools.instrumenttools.EFlatClarinet.EFlatClarinet.EFlatClarinet'>

    Return class.

    When `default_instrument_name` matches no instrument class::

        abjad> instrumenttools.default_instrument_name_to_instrument_class('foo') is None
        True

    Return none.
    '''

    for instrument_class in list_instruments():
        instrument = instrument_class()
        if instrument.default_instrument_name == default_instrument_name:
            return instrument_class
