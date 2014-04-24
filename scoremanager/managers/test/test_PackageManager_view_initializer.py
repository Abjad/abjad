# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_PackageManager_view_initializer_01():

    input_ = 'm example~numbers inro q'
    score_manager._run(pending_user_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - materials',
        'Score manager - materials - example numbers (Abjad)',
        'Score manager - materials - example numbers (Abjad)',
        ]
    assert score_manager._transcript.titles == titles
    assert score_manager._session._attempted_to_open_file