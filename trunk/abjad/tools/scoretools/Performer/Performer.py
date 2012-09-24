from abjad.tools.abctools.AbjadObject import AbjadObject


class Performer(AbjadObject):
    r'''.. versionadded:: 2.5

    Abjad model of performer::

        >>> scoretools.Performer(name='flutist')
        Performer(name='flutist', instruments=InstrumentInventory([]))

    The purpose of the class is to model things like
    flute I doubling piccolo and alto flute.

    At present the class is a list of instruments.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None, instruments=None):
        from abjad.tools.instrumenttools.InstrumentInventory import InstrumentInventory
        self._instruments = InstrumentInventory()
        self.name = name
        self.instruments = instruments

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.name == other.name:
                if self.instruments == other.instruments:
                    return True
        return False

    def __hash__(self):
        return hash((type(self).__name__, self.name, tuple(self.instruments)))

    def __ne__(self, other):
        return not self == other

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        if not self.instruments:
            result = '{}: no instruments'.format(self.name)
        elif len(self.instruments) == 1 and self.name == \
            self.instruments[0].instrument_name:
            result = '{}'.format(self.name)
        else:
            instruments = ', '.join([x.instrument_name for x in self.instruments])
            result = '{}: {}'.format(self.name, instruments)
        return result
            
    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Read-only number of instruments to be played by performer::

            >>> performer = scoretools.Performer('flutist')

        ::

            >>> performer.instruments.append(instrumenttools.Flute())
            >>> performer.instruments.append(instrumenttools.Piccolo())

        ::

            >>> performer.instrument_count
            2

        Return nonnegative integer
        '''
        return len(self.instruments)

    @apply
    def instruments():
        def fget(self):
            r'''List of instruments to be played by performer::

                >>> performer = scoretools.Performer('flutist')

            ::

                >>> performer.instruments.append(instrumenttools.Flute())
                >>> performer.instruments.append(instrumenttools.Piccolo())

            ::

                >>> performer.instruments
                InstrumentInventory([Flute(), Piccolo()])

            Return list.
            '''
            return self._instruments
        def fset(self, instruments):
            from abjad.tools.instrumenttools._Instrument import _Instrument
            if instruments is None:
                self._instruments[:] = []
            elif isinstance(instruments, list):
                assert all([isinstance(x, _Instrument) for x in instruments])
                self._instruments[:] = instruments[:]
            else:
                raise TypeError('instruments %r must be list or none.' % instruments)
        return property(**locals())

    @property
    def is_doubling(self):
        r'''Is performer to play more than one instrument? ::

            >>> performer = scoretools.Performer('flutist')

        ::

            >>> performer.instruments.append(instrumenttools.Flute())
            >>> performer.instruments.append(instrumenttools.Piccolo())

        ::

            >>> performer.is_doubling
            True

        Return boolean.
        '''
        return 1 < self.instrument_count

    @property
    def likely_instruments_based_on_performer_name(self):
        r'''.. versionadded:: 2.5

        Likely instruments based on performer name::

            >>> flutist = scoretools.Performer(name='flutist')
            >>> for likely_instrument in flutist.likely_instruments_based_on_performer_name:
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

            >>> flutist = scoretools.Performer(name='flutist')    
            >>> flutist.most_likely_instrument_based_on_performer_name
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

                >>> performer = scoretools.Performer('flutist')

            ::

                >>> performer.name
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
            for performer_name in instrument.get_performer_names():
                if performer_name in result:
                    result[performer_name].append(instrument_class)
                else:
                    result[performer_name] = [instrument_class]
        return result
