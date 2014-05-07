# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_open_initializer_01():
    r'''Works when initializer doesn't exist.
    '''

    input_ = 'red~example~score g segment~01 ino q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string = 'Can not find' in contents