from abjad.tools.instrumenttools._Instrument import _Instrument


class Performer(object):
    r'''.. versionadded:: 2.5

    Abjad model of performer::

        abjad> scoretools.Performer(name='flutist')
        Performer(name='flutist')

    The purpose of the class is to model things like
    flute I doubling piccolo and alto flute.

    At present the class is a list of instruments.
    '''

    def __init__(self, name=None, instruments=None):
        self.name = name
        self.instruments = instruments

    ### OVERLOADS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.name == other.name:
                if sorted(self.instruments) == sorted(other.instruments):
                    return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self._repr_helper(include_tools_package=False)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _repr_with_tools_package(self):
        return self._repr_helper(include_tools_package=True)

    ### PRIVATE METHODS ####


    def _repr_helper(self, include_tools_package=False):
        values = []
        if self.name is not None:
            values.append('name={!r}'.format(self.name))
        if self.instruments:
            if include_tools_package:
                instruments = ', '.join([x._repr_with_tools_package for x in self.instruments])
                instruments = 'instruments=[{}]'.format(instruments)
            else:
                instruments = 'instruments={}'.format(str(self.instruments[:]))
            values.append(instruments)
        values = ', '.join(values)
        if include_tools_package:
            tools_package = self.__module__.split('.')[-3]
            return '{}.{}({})'.format(tools_package, type(self).__name__, values)
        else:
            return '{}({})'.format(type(self).__name__, values)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def instruments():
        def fget(self):
            r'''List of instruments to be played by performer::

                abjad> performer = scoretools.Performer('flutist')

            ::

                abjad> performer.instruments.append(instrumenttools.Flute())
                abjad> performer.instruments.append(instrumenttools.Piccolo())

            ::

                abjad> performer.instruments
                [Flute(), Piccolo()]

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

    @property
    def instrument_count(self):
        r'''Read-only number of instruments to be played by performer::

            abjad> performer = scoretools.Performer('flutist')

        ::

            abjad> performer.instruments.append(instrumenttools.Flute())
            abjad> performer.instruments.append(instrumenttools.Piccolo())

        ::

            abjad> performer.instrument_count
            2

        Return nonnegative integer
        '''
        return len(self.instruments)

    @property
    def is_doubling(self):
        r'''Is performer to play more than one instrument? ::

            abjad> performer = scoretools.Performer('flutist')

        ::

            abjad> performer.instruments.append(instrumenttools.Flute())
            abjad> performer.instruments.append(instrumenttools.Piccolo())

        ::

            abjad> performer.is_doubling
            True

        Return boolean.
        '''
        return 1 < self.instrument_count

    @property
    def likely_instruments_based_on_performer_name(self):
        r'''.. versionadded:: 2.5

        Likely instruments based on performer name::

            abjad> flutist = scoretools.Performer(name='flutist')
            abjad> for likely_instrument in flutist.likely_instruments_based_on_performer_name:
            ...     likely_instrument
            ... 
            <class 'abjad.tools.instrumenttools.AltoFlute.AltoFlute.AltoFlute'>
            <class 'abjad.tools.instrumenttools.BassFlute.BassFlute.BassFlute'>
            <class 'abjad.tools.instrumenttools.ContrabassFlute.ContrabassFlute.ContrabassFlute'>
            <class 'abjad.tools.instrumenttools.Flute.Flute.Flute'>
            <class 'abjad.tools.instrumenttools.Piccolo.Piccolo.Piccolo'>

        Return list.
        '''
        dictionary = self.make_performer_name_instrument_dictionary()
        try:
            result = dictionary[self.name]
        except KeyError:
            result = []
        return result

    @property
    def most_likely_instrument_based_on_performer_name(self):
        r'''.. versionadded:: 2.5

        Most likely instrument based on performer name::

            abjad> flutist = scoretools.Performer(name='flutist')    
            abjad> flutist.most_likely_instrument_based_on_performer_name
            <class 'abjad.tools.instrumenttools.Flute.Flute.Flute'>

        Return instrument class.
        '''
        for likely_instrument_class in self.likely_instruments_based_on_performer_name:
            likely_instrument = likely_instrument_class()
            if likely_instrument.is_primary_instrument:
                return likely_instrument_class

    @apply
    def name():
        def fget(self):
            r'''Score name of performer::

                abjad> performer = scoretools.Performer('flutist')

            ::

                abjad> performer.name
                'flutist'

            Return string.
            '''
            return self._name
        def fset(self, name):
            assert isinstance(name, (str, type(None)))
            self._name = name
        return property(**locals())

    ### PUBLIC METHODS ###

    # TODO: return ordered dict instead of unordered dict
    # TODO: then add usage example that will pass doctests
    def make_performer_name_instrument_dictionary(self, locale=None):
        r'''.. versionadded:: 2.5

        Make performer name / instrument dictionary.
    
        Return dictionary.
        '''
        from abjad.tools import instrumenttools
        result = {}
        for instrument_class in instrumenttools.list_instruments():
            instrument = instrument_class()
            #performer_name = instrument.get_default_performer_name(locale=locale)
            for performer_name in instrument.get_performer_names():
                if performer_name in result:
                    result[performer_name].append(instrument_class)
                else:
                    result[performer_name] = [instrument_class]
        return result
