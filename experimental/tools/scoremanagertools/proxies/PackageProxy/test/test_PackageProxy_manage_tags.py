from experimental import *


def test_PackageProxy_manage_tags_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='example~score~i tags q')
    assert score_manager.ts == (6,)

    score_manager.run(user_input='example~score~i tags b q')
    assert score_manager.ts == (8, (2, 6))

    score_manager.run(user_input='example~score~i tags home q')
    assert score_manager.ts == (8, (0, 6))

    score_manager.run(user_input='example~score~i tags score q')
    assert score_manager.ts == (8, (2, 6))

    score_manager.run(user_input='example~score~i tags foo q')
    assert score_manager.ts == (8, (4, 6))
