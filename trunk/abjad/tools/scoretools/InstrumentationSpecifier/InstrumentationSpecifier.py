class InstrumentationSpecifier(object):
    r'''.. versionadded:: 2.5

    Abjad model of score instrumentation::

        abjad> flute = scoretools.Performer('Flute')
        abjad> flute.instruments.append(instrumenttools.Flute())
        abjad> flute.instruments.append(instrumenttools.AltoFlute())

    ::

        abjad> guitar = scoretools.Performer('Guitar')
        abjad> guitar.instruments.append(instrumenttools.Guitar())

    ::

        abjad> instrumentation_specifier = scoretools.InstrumentationSpecifier([flute, guitar])

    ::

        abjad> instrumentation_specifier
        InstrumentationSpecifier([Performer('Flute', [Flute(), AltoFlute()]), Performer('Guitar', [Guitar()])])

    Return instrumentation specifier.
    '''

    def __init__(self, performers=None):
        self.performers = performers

    ### OVERLOADS ###
    
    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.performers)

    ### PUBLIC ATTRIBUTES ###

    @property
    def instruments(self):
        r'''Read-only list of instruments derived from performers::

            abjad> instrumentation_specifier.instruments
            [Flute(), AltoFlute(), Guitar()]

        Return list.
        '''        
        instruments = []
        for performer in self.performers:
            instruments.extend(performer.instruments)
        return instruments

    @property
    def instrument_count(self):
        r'''Read-only number of instruments in score::
    
            abjad> instrumentation_specifier.instruments
            3

        Return nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def performer_count(self):
        r'''Read-only number of performers in score::

            abjad> instrumentation_specifier.instruments
            2

        Return nonnegative integer.
        '''
        return len(self.performers)

    @apply
    def performers():
        def fget(self):
            r'''Read / write list of performers in score::

                abjad> instrumentation_specifier.performers
                [Performer('Flute', [Flute(), AltoFlute()]), Performer('Guitar', [Guitar()])]

            Return list.
            '''
            return self._performers
        def fset(self, performers):
            from abjad.tools import scoretools
            assert isinstance(performers, (list, type(None)))
            if performers is None:
                self._performers = []
            else:
                assert all([isinstance(x, scoretools.Performer) for x in performers])
                self._performers = list(performers[:])
        return property(**locals())
