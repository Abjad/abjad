# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_write_stub_initializer_01():

    input_ = 'red~example~score g inws y q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    assert 'Will write stub to' in contents
    assert 'Wrote stub to' in contents