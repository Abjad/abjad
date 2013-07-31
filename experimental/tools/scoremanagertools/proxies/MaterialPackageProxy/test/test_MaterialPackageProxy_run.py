# -*- encoding: utf-8 -*-
import py
from experimental import *


def test_MaterialPackageProxy_run_01():
    r'''Global materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='m sargasso q')
    assert score_manager.session.io_transcript.signature == (6,)

    score_manager._run(pending_user_input='m sargasso b q')
    assert score_manager.session.io_transcript.signature == (8, (2, 6))

    score_manager._run(pending_user_input='m sargasso home q')
    assert score_manager.session.io_transcript.signature == (8, (0, 6))

    # TODO: make this work by causing score backtracking to be ignored
    #score_manager._run(pending_user_input='m sargasso score q')
    #assert score_manager.session.io_transcript.signature == (8, (4, 6))

    score_manager._run(pending_user_input='m sargasso foo q')
    assert score_manager.session.io_transcript.signature == (8, (4, 6))


def test_MaterialPackageProxy_run_02():
    r'''Global materials: breadcrumbs work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='m sargasso q')
    assert score_manager.session.io_transcript[-2][1][0] == 'Score manager - materials - sargasso multipliers'


def test_MaterialPackageProxy_run_03():
    r'''Score materials: quit, back, home, score & junk all work.
    '''
    py.test.skip('TODO: add Red Example Score time signatures.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='all red_example_score m 2 q')
    assert score_manager.session.io_transcript.signature == (10,)

    score_manager._run(pending_user_input='all red_example_score m 2 b q')
    assert score_manager.session.io_transcript.signature == (12, (6, 10))

    score_manager._run(pending_user_input='all red_example_score m 2 home q')
    assert score_manager.session.io_transcript.signature == (12, (2, 10))

    score_manager._run(pending_user_input='all red_example_score m 2 score q')
    assert score_manager.session.io_transcript.signature == (12, (4, 10))

    score_manager._run(pending_user_input='all red_example_score m 2 foo q')
    assert score_manager.session.io_transcript.signature == (12, (8, 10))


def test_MaterialPackageProxy_run_04():
    r'''Score materials: breadcrumbs work.
    '''
    py.test.skip('TODO: add Red Example Score time signatures.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input='all red_example_score m time_signatures q')
    assert score_manager.session.io_transcript[-2][1][0] == 'Red Example Score - materials - time signatures'
