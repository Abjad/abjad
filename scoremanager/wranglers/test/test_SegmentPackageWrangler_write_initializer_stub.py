# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_write_initializer_stub_01():

    input_ = 'red~example~score g ins q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    assert 'Wrote initializer stub.' in contents