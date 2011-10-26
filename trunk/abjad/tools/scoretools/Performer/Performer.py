from abjad.tools.instrumenttools._Instrument import _Instrument


class Performer(object):
    r'''.. versionadded:: 2.5

    Abjad model of performer::

        abjad> instrumenttools.Performer('Flutist')
        Performer('Flutist')

    The purpose of the class is to model things like
    Flute I doubling piccolo and alto flute.

    At present the class is a list of instruments.
    '''

    def __init__(self, designation=None, instruments=None):
        self.designation = designation
        self.instruments = instruments

    ### OVERLOADS ###

    def __repr__(self):
        return self._repr_helper(include_tools_package=False)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _repr_with_tools_package(self):
        return self._repr_helper(include_tools_package=True)

    ### PRIVATE METHODS ####

    def _repr_helper(self, include_tools_package=False):
        values = []
        if self.designation is not None:
            values.append(repr(self.designation))
        if self.instruments:
            if include_tools_package:
                instruments = [x._repr_with_tools_package for x in self.instruments]
            else:
                instruments = self.instruments[:]
            values.append(repr(instruments))
        values = ', '.join(values)
        if include_tools_package:
            tools_package = self.__module__.split('.')[-3]
            return '{}.{}({})'.format(tools_package, type(self).__name__, values)
        else:
            return '{}({})'.format(type(self).__name__, values)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def designation():
        def fget(self):
            r'''Score designation of performer::

                abjad> performer = instrumenttools.Performer('Flutist')

            ::

                abjad> performer.designation
                'Flutist'

            Return string.
            '''
            return self._designation
        def fset(self, designation):
            assert isinstance(designation, (str, type(None)))
            self._designation = designation
        return property(**locals())

    @apply
    def instruments():
        def fget(self):
            r'''List of instruments to be played by performer::

                abjad> performer = instrumenttools.Performer('Flutist')

            ::

                abjad> performer.instruments.append(instrumenttools.Flute())
                abjad> performer.instruments.append(instrumenttools.Piccolo())

            ::

                abjad> performer.instruments
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
