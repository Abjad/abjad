# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialManager__run_01():
    r'''Global materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'lmm example~sargasso~measures q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (6,)

    input_ = 'lmm example~sargasso~measures b q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (8, (2, 6))

    input_ = 'lmm example~sargasso~measures h q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (8, (0, 6))

    input_ = 'lmm example~sargasso~measures s q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (8, (4, 6))

    input_ = 'lmm example~sargasso~measures foo q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (8, (4, 6))


def test_MaterialManager__run_02():
    r'''Global materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'lmm example~sargasso~measures q'
    score_manager._run(pending_user_input=input_, is_test=True)
    string = 'Score manager - material library - example sargasso measures'
    assert score_manager._transcript.last_title == string


def test_MaterialManager__run_03():
    r'''Score materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (8,)

    input_ = 'red~example~score m tempo~inventory b q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (10, (4, 8))

    input_ = 'red~example~score m tempo~inventory h q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (10, (0, 8))

    input_ = 'red~example~score m tempo~inventory s q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (10, (2, 8))

    input_ = 'red~example~score m tempo~inventory foo q'
    score_manager._run(pending_user_input=input_, is_test=True)
    assert score_manager._transcript.signature == (10, (6, 8))


def test_MaterialManager__run_04():
    r'''Score materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=input_, is_test=True)
    string = 'Red Example Score (2013) - materials - tempo inventory'
    assert score_manager._transcript.last_title == string


def test_MaterialManager__run_05():
    r'''Segment navigation works.
    '''

    score_manager = scoremanager.core.ScoreManager()
    input_ = 'red~example~score m g q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles
