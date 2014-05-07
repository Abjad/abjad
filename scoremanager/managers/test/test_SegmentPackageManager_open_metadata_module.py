# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_open_metadata_module_01():

    input_ = 'red~example~score g segment~01 mdmo q'
    score_manager._run(pending_input=input_)

    assert score_manager._session._attempted_to_open_file