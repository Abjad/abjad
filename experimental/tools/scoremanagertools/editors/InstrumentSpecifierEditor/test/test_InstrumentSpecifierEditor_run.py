# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_InstrumentSpecifierEditor_run_01():
    r'''In score.
    '''

    editor = scoremanagertools.editors.InstrumentSpecifierEditor()
    editor.session.snake_case_current_score_name = 'red_example_score'
    editor._run(pending_user_input='name foo instrument horn done')

    assert systemtools.TestManager.compare(
        format(editor.target),
        r'''
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.FrenchHorn(),
            name='foo'
            )
        '''
        )


def test_InstrumentSpecifierEditor_run_02():
    r'''Home.
    '''

    editor = scoremanagertools.editors.InstrumentSpecifierEditor()
    editor._run(pending_user_input='name foo instrument untuned ratt done')

    assert systemtools.TestManager.compare(
        format(editor.target),
        r'''
        specifiers.InstrumentSpecifier(
            instrument=instrumenttools.UntunedPercussion(
                instrument_name='rattle',
                short_instrument_name='rattle'
                ),
            name='foo'
            )
        '''
        )
