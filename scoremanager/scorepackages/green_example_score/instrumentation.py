# -*- encoding: utf-8 -*-
from abjad import *


instrumentation=instrumenttools.InstrumentationSpecifier(
    performers=instrumenttools.PerformerInventory(
        [
            instrumenttools.Performer(
                name='flutist',
                instruments=instrumenttools.InstrumentInventory(
                    [
                        instrumenttools.AltoFlute(
                            instrument_name='alto flute',
                            short_instrument_name='alt. fl.',
                            instrument_name_markup=markuptools.Markup(
                                contents=('Alto flute',),
                                ),
                            short_instrument_name_markup=markuptools.Markup(
                                contents=('Alt. fl.',),
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
                        instrumenttools.Flute(
                            instrument_name='flute',
                            short_instrument_name='fl.',
                            instrument_name_markup=markuptools.Markup(
                                contents=('Flute',),
                                ),
                            short_instrument_name_markup=markuptools.Markup(
                                contents=('Fl.',),
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
                        ]
                    ),
                ),
            instrumenttools.Performer(
                name='guitarist',
                instruments=instrumenttools.InstrumentInventory(
                    [
                        instrumenttools.Guitar(
                            instrument_name='guitar',
                            short_instrument_name='gt.',
                            instrument_name_markup=markuptools.Markup(
                                contents=('Guitar',),
                                ),
                            short_instrument_name_markup=markuptools.Markup(
                                contents=('Gt.',),
                                ),
                            allowable_clefs=indicatortools.ClefInventory(
                                [
                                    indicatortools.Clef(
                                        name='treble',
                                        ),
                                    ]
                                ),
                            default_tuning=indicatortools.Tuning(
                                pitches=pitchtools.PitchSegment(
                                    (
                                        pitchtools.NamedPitch('e,'),
                                        pitchtools.NamedPitch('a,'),
                                        pitchtools.NamedPitch('d'),
                                        pitchtools.NamedPitch('g'),
                                        pitchtools.NamedPitch('b'),
                                        pitchtools.NamedPitch("e'"),
                                        ),
                                    item_class=pitchtools.NamedPitch,
                                    ),
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