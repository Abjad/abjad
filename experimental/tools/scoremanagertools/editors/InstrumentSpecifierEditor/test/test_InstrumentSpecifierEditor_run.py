# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_InstrumentSpecifierEditor_run_01():
    r'''In score.
    '''

    editor = scoremanagertools.editors.InstrumentSpecifierEditor()
    editor.session.snake_case_current_score_name = 'red_example_score'
    editor._run(pending_user_input='id foo instrument horn done')

    assert systemtools.TestManager.compare(
        format(editor.target),
        r'''
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.FrenchHorn(
                instrument_name='horn',
                short_instrument_name='hn.',
                instrument_name_markup=markuptools.Markup(
                    ('Horn',)
                    ),
                short_instrument_name_markup=markuptools.Markup(
                    ('Hn.',)
                    ),
                allowable_clefs=indicatortools.ClefInventory(
                    [
                        indicatortools.Clef(
                            name='bass',
                            ),
                        indicatortools.Clef(
                            name='treble',
                            ),
                        ]
                    ),
                pitch_range=pitchtools.PitchRange(
                    '[B1, F5]'
                    ),
                sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('f'),
                ),
            custom_identifier='foo',
            )
        '''
        )


def test_InstrumentSpecifierEditor_run_02():
    r'''Home.
    '''

    editor = scoremanagertools.editors.InstrumentSpecifierEditor()
    editor._run(pending_user_input='id foo instrument untuned ratt done')

    assert systemtools.TestManager.compare(
        format(editor.target),
        r'''
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.UntunedPercussion(
                instrument_name='rattle',
                short_instrument_name='rattle',
                instrument_name_markup=markuptools.Markup(
                    ('Untuned percussion',)
                    ),
                short_instrument_name_markup=markuptools.Markup(
                    ('Perc.',)
                    ),
                allowable_clefs=indicatortools.ClefInventory(
                    [
                        indicatortools.Clef(
                            name='percussion',
                            ),
                        ]
                    ),
                pitch_range=pitchtools.PitchRange(
                    '[A0, C8]'
                    ),
                sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c'"),
                ),
            custom_identifier='foo',
            )
        '''
        )
