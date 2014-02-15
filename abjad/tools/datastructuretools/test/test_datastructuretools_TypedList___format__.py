# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_TypedList___format___01():
    r'''Empty inventory. No keywords.
    '''

    inventory = datastructuretools.TypedList()

    assert systemtools.TestManager.compare(
        repr(inventory),
        'TypedList([])',
        )
    assert systemtools.TestManager.compare(
        format(inventory),
        '''
        datastructuretools.TypedList(
            []
            )
        ''',
        )


def test_datastructuretools_TypedList___format___03():
    r'''Populated inventory. Without keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah',
        ])

    assert systemtools.TestManager.compare(
        format(inventory),
        r'''
        datastructuretools.TypedList(
            [
                'foo',
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
                'bar',
                pitchtools.PitchRange(
                    '[A0, C8]'
                    ),
                'blah',
                ]
            )
        '''
        )


def test_datastructuretools_TypedList___format___04():
    r'''Populated inventory. With keywords.
    '''

    inventory = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'],
        )

    assert systemtools.TestManager.compare(
        format(inventory),
        r'''
        datastructuretools.TypedList(
            [
                'foo',
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
                'bar',
                pitchtools.PitchRange(
                    '[A0, C8]'
                    ),
                'blah',
                ]
            )
        '''
        )
