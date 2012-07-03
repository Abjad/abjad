from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.scoretools.PerformerInventory import PerformerInventory


class InstrumentationSpecifier(AbjadObject):
    r'''.. versionadded:: 2.5

    Abjad model of score instrumentation::

        >>> flute = scoretools.Performer('Flute')
        >>> flute.instruments.append(instrumenttools.Flute())
        >>> flute.instruments.append(instrumenttools.AltoFlute())

    ::

        >>> guitar = scoretools.Performer('Guitar')
        >>> guitar.instruments.append(instrumenttools.Guitar())

    ::

        >>> instrumentation_specifier = scoretools.InstrumentationSpecifier([flute, guitar])

    ::

        >>> z(instrumentation_specifier)
        scoretools.InstrumentationSpecifier(
            performers=scoretools.PerformerInventory([
                scoretools.Performer(
                    name='Flute',
                    instruments=instrumenttools.InstrumentInventory([
                        instrumenttools.Flute(),
                        instrumenttools.AltoFlute()
                        ])
                    ),
                scoretools.Performer(
                    name='Guitar',
                    instruments=instrumenttools.InstrumentInventory([
                        instrumenttools.Guitar()
                        ])
                    )
                ])
            )

    Return instrumentation specifier.
    '''

    def __init__(self, performers=None):
        self._performers = PerformerInventory()
        self.performers = performers

    ### SPECIAL METHODS ###
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            # TODO: implement perform sort
            #if sorted(self.performers) == sorted(other.performers):
            if self.performers == other.performers:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Read-only number of instruments in score::
    
            >>> instrumentation_specifier.instrument_count
            3

        Return nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def instruments(self):
        r'''Read-only list of instruments derived from performers::

            >>> instrumentation_specifier.instruments
            [Flute(), AltoFlute(), Guitar()]

        Return list.
        '''        
        instruments = []
        for performer in self.performers:
            instruments.extend(performer.instruments)
        return instruments

    @property
    def performer_count(self):
        r'''Read-only number of performers in score::

            >>> instrumentation_specifier.performer_count
            2

        Return nonnegative integer.
        '''
        return len(self.performers)

    @property
    def performer_name_string(self):
        r'''Read-only string of performer names::

            >>> instrumentation_specifier.performer_name_string
            'Flute, Guitar'

        Return string.
        '''
        if self.performers:
            return ', '.join([performer.name for performer in self.performers])
        else:
            return ''

    @apply
    def performers():
        def fget(self):
            r'''Read / write list of performers in score::

                >>> z(instrumentation_specifier.performers)
                scoretools.PerformerInventory([
                    scoretools.Performer(
                        name='Flute',
                        instruments=instrumenttools.InstrumentInventory([
                            instrumenttools.Flute(),
                            instrumenttools.AltoFlute()
                            ])
                        ),
                    scoretools.Performer(
                        name='Guitar',
                        instruments=instrumenttools.InstrumentInventory([
                            instrumenttools.Guitar()
                            ])
                        )
                    ])

            Return performer inventory.
            '''
            return self._performers
        def fset(self, performers):
            from abjad.tools import scoretools
            assert isinstance(performers, (list, type(None)))
            if performers is None:
                self._performers[:] = []
            else:
                assert all([isinstance(x, scoretools.Performer) for x in performers])
                self._performers[:] = list(performers[:])
        return property(**locals())
