# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_repository_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score g rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_SegmentPackageManager_repository_status_02():
    r'''Works with Subversion.
    '''

    wrangler = score_manager._segment_package_wrangler
    manager = wrangler._find_svn_manager()
    if not manager:
        return
    manager.repository_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents