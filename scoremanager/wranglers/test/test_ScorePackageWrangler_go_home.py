# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_go_home_01():

    input_ = 'h q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Score Manager - scores',
        ]
    assert score_manager._transcript.titles == titles