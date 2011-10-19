from abjad.tools.instrumenttools._Instrument import _Instrument


class HumanMusician(object):
    r'''.. versionadded:: 2.5

    Abjad model of human musician::

        abjad> instrumenttools.HumanMusician('Flutist')
        HumanMusician('Flutist')

    The purpose of the class is to model things like
    Flute I doubling piccolo and alto flute.

    At present the class is basically a list of instruments.
    '''

    def __init__(self, musician_name=None, instruments=None):
        self.musician_name = musician_name
        self.instruments = instruments

    ### OVERLOADS ###

    def __repr__(self):
        if self.musician_name is not None:
            return '%s(%r)' % (type(self).__name__, self.musician_name)
        else:
            return '%s()' % type(self).__name__

    ### PUBLIC ATTRIBUTES ###

    @apply
    def instruments():
        def fget(self):
            r'''List of instruments to be played by musician::

                abjad> musician = instrumenttools.HumanMusician('Flutist')

            ::

                abjad> musician.instruments.append(instrumenttools.Flute())
                abjad> musician.instruments.append(instrumenttools.Piccolo())

            ::

                abjad> musician.instruments
                [Flute('Flute', 'Fl.'), Piccolo('Piccolo', 'Picc.')]

            Return list.
            '''
            return self._instruments
        def fset(self, instruments):
            if instruments is None:
                self._instruments = []
            elif isinstance(instruments, list):
                assert all([isinstance(x, _Instrument) for x in instruments])
                self._instruments = instruments[:]
            else:
                raise TypeError('instruments %r must be list or none.' % instruments)
        return property(**locals())

    @apply
    def musician_name():
        def fget(self):
            r'''Name of musician::

                abjad> musician = instrumenttools.HumanMusician('Flutist')

            ::

                abjad> musician.musician_name
                'Flutist'

            Return string.
            '''
            return self._musician_name
        def fset(self, musician_name):
            assert isinstance(musician_name, (str, type(None)))
            self._musician_name = musician_name
        return property(**locals())
