# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_display_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score m tempo~inventory rst q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageManager_display_status_02():
    r'''Works with Subversion.
    '''

    wrangler = ide._material_package_wrangler
    manager = wrangler._find_svn_manager()
    if not manager:
        return
    manager.display_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents