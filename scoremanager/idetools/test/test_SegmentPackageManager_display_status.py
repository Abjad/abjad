# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_display_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score g A rst q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_SegmentPackageManager_display_status_02():
    r'''Works with Subversion.
    '''

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_svn_manager()
    if not manager:
        return
    manager.display_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents