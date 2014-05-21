# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_go_to_stylesheets_01():
    r'''From materials directory to build directory.
    '''

    input_ = 'y q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - scores',
        'Score manager - stylesheets',
        ]
    assert score_manager._transcript.titles == titles