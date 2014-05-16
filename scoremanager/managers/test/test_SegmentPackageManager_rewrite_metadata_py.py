# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_rewrite_metadata_py_01():

    input_ = 'red~example~score g A mdpyrw default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'Rewrote __metadata.py__.' in contents