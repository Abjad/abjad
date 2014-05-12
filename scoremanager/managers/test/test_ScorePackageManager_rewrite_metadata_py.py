# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_rewrite_metadata_py_01():

    input_ = 'red~example~score mdmrw default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'Rewrote metadata module.' in contents