# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManager__run_01():
    r'''Global materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm example~sargasso~measures q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (6,)

    input_ = 'm example~sargasso~measures b q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (8, (2, 6))

    input_ = 'm example~sargasso~measures h q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (8, (0, 6))

    input_ = 'm example~sargasso~measures s q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (8, (4, 6))

    input_ = 'm example~sargasso~measures foo q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (8, (4, 6))


def test_MaterialPackageManager__run_02():
    r'''Global materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm example~sargasso~measures q'
    score_manager._run(pending_input=input_)
    string = 'Score manager - materials'
    string += ' - example sargasso measures (Abjad)'
    assert score_manager._transcript.last_title == string


def test_MaterialPackageManager__run_03():
    r'''Score materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (8,)

    input_ = 'red~example~score m tempo~inventory b q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (10, (4, 8))

    input_ = 'red~example~score m tempo~inventory h q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (10, (0, 8))

    input_ = 'red~example~score m tempo~inventory s q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (10, (2, 8))

    input_ = 'red~example~score m tempo~inventory foo q'
    score_manager._run(pending_input=input_)
    assert score_manager._transcript.signature == (10, (6, 8))


def test_MaterialPackageManager__run_04():
    r'''Score materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_input=input_)
    string = 'Red Example Score (2013) - materials - tempo inventory'
    assert score_manager._transcript.last_title == string


def test_MaterialPackageManager__run_05():
    r'''Segment navigation works.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m g q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles