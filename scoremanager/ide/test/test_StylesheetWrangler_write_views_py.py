# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_StylesheetWrangler_write_views_py_01():

    input_ = 'red~example~score y vw y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Will write ...' in contents
    assert 'Rewrote' in contents