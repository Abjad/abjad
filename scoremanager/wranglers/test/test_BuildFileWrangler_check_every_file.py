# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_BuildFileWrangler_check_every_file_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score u ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Build files (18 files): OK' in contents


def test_BuildFileWrangler_check_every_file_02():
    r'''Works in library.
    '''

    input_ = 'u ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Build files' in contents