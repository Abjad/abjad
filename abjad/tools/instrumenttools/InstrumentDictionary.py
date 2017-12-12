from abjad.tools.datastructuretools.TypedOrderedDict import TypedOrderedDict


class InstrumentDictionary(TypedOrderedDict):
    r'''Instrument dictionary.

    ..  container:: example

        >>> instruments = abjad.InstrumentDictionary([
        ...     ('flute', abjad.Flute()),
        ...     ('guitar', abjad.Guitar()),
        ...     ])

        >>> abjad.f(instruments)
        abjad.InstrumentDictionary(
            [
                (
                    'flute',
                    abjad.Flute(
                        name='flute',
                        short_name='fl.',
                        name_markup=abjad.Markup(
                            contents=['Flute'],
                            ),
                        short_name_markup=abjad.Markup(
                            contents=['Fl.'],
                            ),
                        allowable_clefs=('treble',),
                        context='Staff',
                        middle_c_sounding_pitch=abjad.NamedPitch("c'"),
                        pitch_range=abjad.PitchRange('[C4, D7]'),
                        ),
                    ),
                (
                    'guitar',
                    abjad.Guitar(
                        name='guitar',
                        short_name='gt.',
                        name_markup=abjad.Markup(
                            contents=['Guitar'],
                            ),
                        short_name_markup=abjad.Markup(
                            contents=['Gt.'],
                            ),
                        allowable_clefs=('treble',),
                        context='Staff',
                        default_tuning=abjad.Tuning(
                            pitches=abjad.PitchSegment(
                                (
                                    abjad.NamedPitch('e,'),
                                    abjad.NamedPitch('a,'),
                                    abjad.NamedPitch('d'),
                                    abjad.NamedPitch('g'),
                                    abjad.NamedPitch('b'),
                                    abjad.NamedPitch("e'"),
                                    ),
                                item_class=abjad.NamedPitch,
                                ),
                            ),
                        middle_c_sounding_pitch=abjad.NamedPitch('c'),
                        pitch_range=abjad.PitchRange('[E2, E5]'),
                        ),
                    ),
                ]
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()
