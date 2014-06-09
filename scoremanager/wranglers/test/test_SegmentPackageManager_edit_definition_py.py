# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_edit_definition_py_01():

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    input_ = 'red~example~score g A de q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file