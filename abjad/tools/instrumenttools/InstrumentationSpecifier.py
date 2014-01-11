# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class InstrumentationSpecifier(AbjadObject):
    r'''Instrumentation specifier for an entire score.

    ::

        >>> flute = instrumenttools.Performer('Flute')
        >>> flute.instruments.append(instrumenttools.Flute())
        >>> flute.instruments.append(instrumenttools.AltoFlute())

    ::

        >>> guitar = instrumenttools.Performer('Guitar')
        >>> guitar.instruments.append(instrumenttools.Guitar())

    ::

        >>> instrumentation_specifier = \
        ...     instrumenttools.InstrumentationSpecifier([flute, guitar])

    ::

        >>> print format(instrumentation_specifier)
        instrumenttools.InstrumentationSpecifier(
            performers=instrumenttools.PerformerInventory(
                [
                    instrumenttools.Performer(
                        name='Flute',
                        instruments=instrumenttools.InstrumentInventory(
                            [
                                instrumenttools.Flute(
                                    instrument_name='flute',
                                    short_instrument_name='fl.',
                                    instrument_name_markup=markuptools.Markup(
                                        ('Flute',)
                                        ),
                                    short_instrument_name_markup=markuptools.Markup(
                                        ('Fl.',)
                                        ),
                                    allowable_clefs=indicatortools.ClefInventory(
                                        [
                                            indicatortools.Clef(
                                                name='treble',
                                                ),
                                            ]
                                        ),
                                    pitch_range=pitchtools.PitchRange(
                                        '[C4, D7]'
                                        ),
                                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                                    ),
                                instrumenttools.AltoFlute(
                                    instrument_name='alto flute',
                                    short_instrument_name='alt. fl.',
                                    instrument_name_markup=markuptools.Markup(
                                        ('Alto flute',)
                                        ),
                                    short_instrument_name_markup=markuptools.Markup(
                                        ('Alt. fl.',)
                                        ),
                                    allowable_clefs=indicatortools.ClefInventory(
                                        [
                                            indicatortools.Clef(
                                                name='treble',
                                                ),
                                            ]
                                        ),
                                    pitch_range=pitchtools.PitchRange(
                                        '[G3, G6]'
                                        ),
                                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('g'),
                                    ),
                                ]
                            ),
                        ),
                    instrumenttools.Performer(
                        name='Guitar',
                        instruments=instrumenttools.InstrumentInventory(
                            [
                                instrumenttools.Guitar(
                                    instrument_name='guitar',
                                    short_instrument_name='gt.',
                                    instrument_name_markup=markuptools.Markup(
                                        ('Guitar',)
                                        ),
                                    short_instrument_name_markup=markuptools.Markup(
                                        ('Gt.',)
                                        ),
                                    allowable_clefs=indicatortools.ClefInventory(
                                        [
                                            indicatortools.Clef(
                                                name='treble',
                                                ),
                                            ]
                                        ),
                                    pitch_range=pitchtools.PitchRange(
                                        '[E2, E5]'
                                        ),
                                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('c'),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            )

    Returns instrumentation specifier.
    '''

    def __init__(self, performers=None):
        from abjad.tools import instrumenttools
        self._performers = instrumenttools.PerformerInventory()
        self.performers = performers

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is an instrumentation specifier with performers
        equal to those of instrumentation specifier. Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.performers == expr.performers:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats instrumentation specifier.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Number of instruments in score.

        ::

            >>> instrumentation_specifier.instrument_count
            3

        Returns nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def instruments(self):
        r'''List of instruments derived from performers.

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
        r'''Number of performers in score.

        ::

            >>> instrumentation_specifier.performer_count
            2

        Returns nonnegative integer.
        '''
        return len(self.performers)

    @property
    def performer_name_string(self):
        r'''String of performer names.

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

    @property
    def performers(self):
        r'''Gets and sets list of performers in score.

        ::

            >>> print format(instrumentation_specifier.performers)
            instrumenttools.PerformerInventory(
                [
                    instrumenttools.Performer(
                        name='Flute',
                        instruments=instrumenttools.InstrumentInventory(
                            [
                                instrumenttools.Flute(
                                    instrument_name='flute',
                                    short_instrument_name='fl.',
                                    instrument_name_markup=markuptools.Markup(
                                        ('Flute',)
                                        ),
                                    short_instrument_name_markup=markuptools.Markup(
                                        ('Fl.',)
                                        ),
                                    allowable_clefs=indicatortools.ClefInventory(
                                        [
                                            indicatortools.Clef(
                                                name='treble',
                                                ),
                                            ]
                                        ),
                                    pitch_range=pitchtools.PitchRange(
                                        '[C4, D7]'
                                        ),
                                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                                    ),
                                instrumenttools.AltoFlute(
                                    instrument_name='alto flute',
                                    short_instrument_name='alt. fl.',
                                    instrument_name_markup=markuptools.Markup(
                                        ('Alto flute',)
                                        ),
                                    short_instrument_name_markup=markuptools.Markup(
                                        ('Alt. fl.',)
                                        ),
                                    allowable_clefs=indicatortools.ClefInventory(
                                        [
                                            indicatortools.Clef(
                                                name='treble',
                                                ),
                                            ]
                                        ),
                                    pitch_range=pitchtools.PitchRange(
                                        '[G3, G6]'
                                        ),
                                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('g'),
                                    ),
                                ]
                            ),
                        ),
                    instrumenttools.Performer(
                        name='Guitar',
                        instruments=instrumenttools.InstrumentInventory(
                            [
                                instrumenttools.Guitar(
                                    instrument_name='guitar',
                                    short_instrument_name='gt.',
                                    instrument_name_markup=markuptools.Markup(
                                        ('Guitar',)
                                        ),
                                    short_instrument_name_markup=markuptools.Markup(
                                        ('Gt.',)
                                        ),
                                    allowable_clefs=indicatortools.ClefInventory(
                                        [
                                            indicatortools.Clef(
                                                name='treble',
                                                ),
                                            ]
                                        ),
                                    pitch_range=pitchtools.PitchRange(
                                        '[E2, E5]'
                                        ),
                                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('c'),
                                    ),
                                ]
                            ),
                        ),
                    ]
                )

        Returns performer inventory.
        '''
        return self._performers

    @performers.setter
    def performers(self, performers):
        from abjad.tools import instrumenttools
        assert isinstance(performers, 
            (list, datastructuretools.TypedList, type(None)))
        if performers is None:
            self._performers[:] = []
        else:
            assert all(isinstance(x, instrumenttools.Performer) 
                for x in performers)
            self._performers[:] = list(performers[:])
