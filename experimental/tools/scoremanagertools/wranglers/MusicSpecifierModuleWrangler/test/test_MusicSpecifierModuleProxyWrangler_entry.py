from experimental import *


def test_MusicSpecifierModuleProxyWrangler_entry_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(user_input='f q')

    assert score_manager._session.transcript[-2][1][0] == 'Scores - music specifiers'
    assert score_manager._session.transcript[-2][1][-4:] == \
        ['     new music specifier (new)',
         '     rename music specifier (ren)',
         '     remove music specifiers (rm)',
         '']
