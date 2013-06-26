import inspect


def list_instruments(klasses=None):
    r'''.. versionadded:: 2.5

    List instruments in ``instrumenttools`` module:

    ::

        >>> for instrument in instrumenttools.list_instruments()[:5]:
        ...     instrument.__name__
        ...
        'Accordion'
        'AltoFlute'
        'AltoSaxophone'
        'AltoTrombone'
        'BaritoneSaxophone'

    Return list.
    '''
    from abjad.tools import instrumenttools

    if klasses is None:
        klasses = (instrumenttools.Instrument, )

    instruments = []
    for value in instrumenttools.__dict__.itervalues():
        try:
            if issubclass(value, klasses) and not inspect.isabstract(value):
                instruments.append(value)
        except TypeError:
            pass
    instruments.sort(key=lambda x: x.__name__.lower())

    return instruments
