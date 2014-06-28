# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_write_cache_01():
    r'''Not necessary to keep cache path with FilesystemState.
    AbjadIDE._run() always preserves cache during tests.
    '''

    input_ = 'cw q'
    ide._run(input_=input_)
    contents = ide._transcript.contents
    assert 'Wrote' in contents