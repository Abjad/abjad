# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MakerFileWrangler_check_every_file_01():
    r'''Works in score.
    '''

    input_ = 'red~example~score k ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Maker files (2 files): OK' in contents


def test_MakerFileWrangler_check_every_file_02():
    r'''Works in library.
    '''

    input_ = 'k ck* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Maker files' in contents