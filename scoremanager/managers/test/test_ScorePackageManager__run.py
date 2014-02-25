# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager__run_01():
    r'''Segment navigation works.
    '''

    score_manager = scoremanager.core.ScoreManager()

    string = 'red~example~score setup g q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score templates g q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - score_templates',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score stylesheets g q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles


def test_ScorePackageManager__run_02():
    r'''Material navigation works.
    '''

    score_manager = scoremanager.core.ScoreManager()

    string = 'red~example~score setup m q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score templates m q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - score_templates',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score stylesheets m q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_ScorePackageManager__run_03():
    r'''Build navigation works.
    '''

    score_manager = scoremanager.core.ScoreManager()

    string = 'red~example~score u u q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build manager',
        'Red Example Score (2013) - build manager',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score m u q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - build manager',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score g u q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - build manager',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score setup u q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - setup',
        'Red Example Score (2013) - build manager',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score templates u q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - score_templates',
        'Red Example Score (2013) - build manager',
        ]
    assert score_manager._transcript.titles == titles

    string = 'red~example~score y u q'
    score_manager._run(pending_user_input=string)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - build manager',
        ]
    assert score_manager._transcript.titles == titles
