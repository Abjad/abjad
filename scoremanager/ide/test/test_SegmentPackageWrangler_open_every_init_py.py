# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_open_every_init_py_01():

    input_ = 'red~example~score g no* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string = 'Will open ...'
    assert string in contents
    assert score_manager._session._attempted_to_open_file