# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_commit_01():
    r'''Flow control reaches Git-managed segment package.
    '''

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_git_manager()

    manager._session._is_repository_test = True
    manager.commit()
    assert manager._session._attempted_to_commit


def test_SegmentPackageManager_commit_02():
    r'''Flow control reaches Subversion-managed segment package.
    '''

    wrangler = ide._segment_package_wrangler
    manager = wrangler._find_svn_manager()

    if not manager:
        return

    manager._session._is_repository_test = True
    manager.commit()
    assert manager._session._attempted_to_commit


def test_SegmentPackageManager_commit_03():
    r'''Back works in commit message getter.
    '''

    input_ = 'red~example~score rci b q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert not 'Commit message will be' in contents