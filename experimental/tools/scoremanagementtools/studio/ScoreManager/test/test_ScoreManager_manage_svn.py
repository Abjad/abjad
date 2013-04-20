from experimental import *


def test_ScoreManager_manage_svn_01():
    '''Ignore score backtracking.
    '''

    score_manager = scoremanagementtools.studio.ScoreManager()
    score_manager.run(user_input='svn sco q')
    assert score_manager.ts == (6, (2, 4))
