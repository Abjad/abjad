# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_write_cache_01():
    r'''Not necessary to keep cache path with FilesystemState.
    ScoreManager._run() always preserves cache during tests.
    '''

    input_ = 'cw <return> q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    assert 'Wrote' in contents