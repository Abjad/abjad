from experimental import *


def test_ScoreManager_manage_svn_01():
    '''Ignore score backtracking.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='svn sco q')
    assert score_manager.transcript_signature == (6, (2, 4))
