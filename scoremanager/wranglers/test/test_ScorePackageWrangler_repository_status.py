# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_repository_status_01():
    r'''Works with all scores.
    '''

    input_ = 'rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents