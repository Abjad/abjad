from experimental import *


def test_PackageProxy_manage_tags_01():
    '''Quit, back, home, score & junk all work.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='red~example~score tags q')
    assert score_manager._session.transcript.signature == (6,)

    score_manager._run(user_input='red~example~score tags b q')
    assert score_manager._session.transcript.signature == (8, (2, 6))

    score_manager._run(user_input='red~example~score tags home q')
    assert score_manager._session.transcript.signature == (8, (0, 6))

    score_manager._run(user_input='red~example~score tags score q')
    assert score_manager._session.transcript.signature == (8, (2, 6))

    score_manager._run(user_input='red~example~score tags foo q')
    assert score_manager._session.transcript.signature == (8, (4, 6))
