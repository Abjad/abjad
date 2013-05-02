from experimental import *
import py


def test_MaterialPackageWrangler_run_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='m q')
    assert score_manager.session.transcript.signature == (4,)

    score_manager.run(user_input='m b q')
    assert score_manager.session.transcript.signature == (6, (0, 4))

    score_manager.run(user_input='m home q')
    assert score_manager.session.transcript.signature == (6, (0, 4))

    score_manager.run(user_input='m score q')
    assert score_manager.session.transcript.signature == (6, (2, 4))

    score_manager.run(user_input='m asdf q')
    assert score_manager.session.transcript.signature == (6, (2, 4))


def test_MaterialPackageWrangler_run_02():
    '''Breadcrumbs work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='m q')
    assert score_manager.session.short_transcript[-2][0] == 'Scores - materials'
