# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageManager_list_versions_directory_01():
    r'''Score manager displays informative string when no versions
    directory exists and raises no exceptions.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score g 1 vrl default q'
    score_manager._run(pending_user_input=string)

    string = 'No versions found.'
    assert score_manager._transcript[-5].title == string
