from experimental import *


def test_ScoreManager_manage_svn_01():
    '''Ignore score backtracking.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='svn sco q')
    assert score_manager._session.transcript.signature == (6, (2, 4))
