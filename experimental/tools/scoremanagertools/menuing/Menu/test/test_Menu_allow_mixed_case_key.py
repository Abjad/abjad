from experimental import *


def test_Menu_allow_mixed_case_key_01():
    '''Allow mixed case 'home' key.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input="L'arch home q")
    assert score_manager.ts == (6, (0, 4))

    score_manager.run(user_input="L'arch HOME q")
    assert score_manager.ts == (6, (0, 4))

    score_manager.run(user_input="L'arch hOmE q")
    assert score_manager.ts == (6, (0, 4))

    score_manager.run(user_input="L'arch hOME q")
    assert score_manager.ts == (6, (0, 4))
