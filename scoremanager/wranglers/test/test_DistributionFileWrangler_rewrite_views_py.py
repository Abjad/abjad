# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionFileWrangler_rewrite_views_py_01():

    input_ = 'red~example~score d vw y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Will rewrite ...' in contents
    assert 'Rewrote' in contents