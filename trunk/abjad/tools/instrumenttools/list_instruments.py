import inspect


def list_instruments(klasses=None):
    r'''.. versionadded:: 2.5

    List instruments in ``instrumenttools`` module::

        >>> for instrument in instrumenttools.list_instruments()[:5]:
        ...     instrument
        ...
        <class 'abjad.tools.instrumenttools.Accordion.Accordion.Accordion'>
        <class 'abjad.tools.instrumenttools.AltoFlute.AltoFlute.AltoFlute'>
        <class 'abjad.tools.instrumenttools.AltoSaxophone.AltoSaxophone.AltoSaxophone'>
        <class 'abjad.tools.instrumenttools.AltoTrombone.AltoTrombone.AltoTrombone'>
        <class 'abjad.tools.instrumenttools.BFlatClarinet.BFlatClarinet.BFlatClarinet'>

    Return list.
    '''
    from abjad.tools import instrumenttools
    from abjad.tools.instrumenttools.Instrument import Instrument

    if klasses is None:
        klasses = (Instrument, )

    instruments = []
    for value in instrumenttools.__dict__.itervalues():
        try:
            if issubclass(value, klasses) and not inspect.isabstract(value):
                instruments.append(value)
        except TypeError:
            pass
    instruments.sort(lambda x, y: cmp(x.__name__, y.__name__))

    return instruments
