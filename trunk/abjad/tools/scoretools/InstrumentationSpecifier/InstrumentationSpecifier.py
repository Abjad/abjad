# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.scoretools.PerformerInventory import PerformerInventory


class InstrumentationSpecifier(AbjadObject):
    r'''Abjad model of score instrumentation:

    ::

        >>> flute = scoretools.Performer('Flute')
        >>> flute.instruments.append(instrumenttools.Flute())
        >>> flute.instruments.append(instrumenttools.AltoFlute())

    ::

        >>> guitar = scoretools.Performer('Guitar')
        >>> guitar.instruments.append(instrumenttools.Guitar())

    ::

        >>> instrumentation_specifier = \
        ...     scoretools.InstrumentationSpecifier([flute, guitar])

    ::

        >>> print instrumentation_specifier.storage_format
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

    Returns instrumentation specifier.
    '''

    def __init__(self, performers=None):
        self._performers = PerformerInventory()
        self.performers = performers

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.performers == expr.performers:
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Number of instruments in score:

        ::

            >>> instrumentation_specifier.instrument_count
            3

        Returns nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def instruments(self):
        r'''List of instruments derived from performers:

        ::

            >>> instrumentation_specifier.instruments
            [Flute(), AltoFlute(), Guitar()]

        Returns list.
        '''
        instruments = []
        for performer in self.performers:
            instruments.extend(performer.instruments)
        return instruments

    @property
    def performer_count(self):
        r'''Number of performers in score:

        ::

            >>> instrumentation_specifier.performer_count
            2

        Returns nonnegative integer.
        '''
        return len(self.performers)

    @property
    def performer_name_string(self):
        r'''String of performer names:

        ::

            >>> instrumentation_specifier.performer_name_string
            'Flute, Guitar'

        Returns string.
        '''
        if self.performers:
            return ', '.join([performer.name 
                for performer in self.performers])
        else:
            return ''

    @apply
    def performers():
        def fget(self):
            r'''Read / write list of performers in score:

            ::

                >>> print instrumentation_specifier.performers.storage_format
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

            Returns performer inventory.
            '''
            return self._performers
        def fset(self, performers):
            from abjad.tools import scoretools
            assert isinstance(performers, 
                (list, datastructuretools.TypedList, type(None)))
            if performers is None:
                self._performers[:] = []
            else:
                assert all(isinstance(x, scoretools.Performer) 
                    for x in performers)
                self._performers[:] = list(performers[:])
        return property(**locals())

    @property
    def storage_format(self):
        r'''Storage format of instrumentation specifier.

        Returns string.
        '''
        return self._tools_package_qualified_indented_repr
