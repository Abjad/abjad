# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_list_versions_directory_01():
    r'''Score manager displays informative string when no versions
    directory exists and raises no exceptions.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score g 1 vdls default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string = 'definition_0001.py output_0001.ly output_0001.pdf'
    assert string in contents