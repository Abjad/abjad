# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_edit_score_stylesheet_01():

    input_ = 'red~example~score d sse q'
    score_manager._run(pending_input=input_)

    assert score_manager._session._attempted_to_open_file