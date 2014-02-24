# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageManager__run_01():
    r'''Global materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm red~sargasso~measures q')
    assert score_manager._transcript.signature == (6,)

    score_manager._run(pending_user_input='lmm red~sargasso~measures b q')
    assert score_manager._transcript.signature == (8, (2, 6))

    score_manager._run(pending_user_input='lmm red~sargasso~measures h q')
    assert score_manager._transcript.signature == (8, (0, 6))

    score_manager._run(pending_user_input='lmm red~sargasso~measures s q')
    assert score_manager._transcript.signature == (8, (4, 6))

    score_manager._run(pending_user_input='lmm red~sargasso~measures foo q')
    assert score_manager._transcript.signature == (8, (4, 6))


def test_MaterialPackageManager__run_02():
    r'''Global materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm red~sargasso~measures q')
    string = 'Score manager - material library - red sargasso measures'
    assert score_manager._transcript.last_menu_title == string


def test_MaterialPackageManager__run_03():
    r'''Score materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (8,)

    string = 'red~example~score m tempo~inventory b q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (10, (4, 8))

    string = 'red~example~score m tempo~inventory h q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (10, (0, 8))

    string = 'red~example~score m tempo~inventory s q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (10, (2, 8))

    string = 'red~example~score m tempo~inventory foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager._transcript.signature == (10, (6, 8))


def test_MaterialPackageManager__run_04():
    r'''Score materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)
    string = 'Red Example Score (2013) - materials - tempo inventory'
    assert score_manager._transcript.last_menu_title == string


def test_MaterialPackageManager__run_05():
    r'''Segment navigation works.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m g q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles
