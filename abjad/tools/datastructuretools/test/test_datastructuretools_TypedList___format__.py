# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_TypedList___format___01():

    list_ = datastructuretools.TypedList()

    assert format(repr(list_)) == stringtools.normalize(
        'TypedList([])',
        )
    assert format(list_) == stringtools.normalize(
        '''
        datastructuretools.TypedList(
            []
            )
        ''',
        )


def test_datastructuretools_TypedList___format___02():

    list_ = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah',
        ])

    assert format(list_) == stringtools.normalize(
        r'''
        datastructuretools.TypedList(
            [
                'foo',
                instrumenttools.Flute(
                    instrument_name='flute',
                    short_instrument_name='fl.',
                    instrument_name_markup=markuptools.Markup(
                        contents=['Flute'],
                        ),
                    short_instrument_name_markup=markuptools.Markup(
                        contents=['Fl.'],
                        ),
                    allowable_clefs=instrumenttools.ClefList(
                        [
                            indicatortools.Clef(
                                name='treble',
                                ),
                            ]
                        ),
                    pitch_range=pitchtools.PitchRange(
                        range_string='[C4, D7]',
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                    ),
                'bar',
                pitchtools.PitchRange(
                    range_string='[A0, C8]',
                    ),
                'blah',
                ]
            )
        '''
        )


def test_datastructuretools_TypedList___format___03():
    r'''Populated list. With keywords.
    '''

    list_ = datastructuretools.TypedList([
        'foo',
        instrumenttools.Flute(),
        'bar',
        pitchtools.PitchRange('[A0, C8]'),
        'blah'],
        )

    assert format(list_) == stringtools.normalize(
        r'''
        datastructuretools.TypedList(
            [
                'foo',
                instrumenttools.Flute(
                    instrument_name='flute',
                    short_instrument_name='fl.',
                    instrument_name_markup=markuptools.Markup(
                        contents=['Flute'],
                        ),
                    short_instrument_name_markup=markuptools.Markup(
                        contents=['Fl.'],
                        ),
                    allowable_clefs=instrumenttools.ClefList(
                        [
                            indicatortools.Clef(
                                name='treble',
                                ),
                            ]
                        ),
                    pitch_range=pitchtools.PitchRange(
                        range_string='[C4, D7]',
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                    ),
                'bar',
                pitchtools.PitchRange(
                    range_string='[A0, C8]',
                    ),
                'blah',
                ]
            )
        '''
        )
