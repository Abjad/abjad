from experimental import *


def test_Menu_allow_ascii_access_to_unicode_key_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager.run(user_input='Étude q')
    assert score_manager.transcript_signature == (4,)

    score_manager.run(user_input='étude q')
    assert score_manager.transcript_signature == (4,)

    score_manager.run(user_input='Etude q')
    assert score_manager.transcript_signature == (4,)

    score_manager.run(user_input='etude q')
    assert score_manager.transcript_signature == (4,)
