import py
from experimental import *


def test_MaterialPackageProxy_run_01():
    '''Global materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='m sargasso q')
    assert score_manager.ts == (6,)

    score_manager.run(user_input='m sargasso b q')
    assert score_manager.ts == (8, (2, 6))

    score_manager.run(user_input='m sargasso home q')
    assert score_manager.ts == (8, (0, 6))

    # TODO: make this work by causing score backtracking to be ignored
    #score_manager.run(user_input='m sargasso score q')
    #assert score_manager.ts == (8, (4, 6))

    score_manager.run(user_input='m sargasso foo q')
    assert score_manager.ts == (8, (4, 6))


def test_MaterialPackageProxy_run_02():
    '''Global materials: breadcrumbs work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='m sargasso q')
    assert score_manager.transcript[-2][0] == 'Scores - materials - sargasso multipliers'


def test_MaterialPackageProxy_run_03():
    '''Score materials: quit, back, home, score & junk all work.
    '''
    py.test.skip('TODO: add Example Score I time signatures.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='all example_score_1 m 2 q')
    assert score_manager.ts == (10,)

    score_manager.run(user_input='all example_score_1 m 2 b q')
    assert score_manager.ts == (12, (6, 10))

    score_manager.run(user_input='all example_score_1 m 2 home q')
    assert score_manager.ts == (12, (2, 10))

    score_manager.run(user_input='all example_score_1 m 2 score q')
    assert score_manager.ts == (12, (4, 10))

    score_manager.run(user_input='all example_score_1 m 2 foo q')
    assert score_manager.ts == (12, (8, 10))


def test_MaterialPackageProxy_run_04():
    '''Score materials: breadcrumbs work.
    '''
    py.test.skip('TODO: add Example Score I time signatures.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='all example_score_1 m time_signatures q')
    assert score_manager.transcript[-2][0] == 'Example Score I - materials - time signatures'
