# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_repository_status_01():
    r'''Work with Git outside of score.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    input_ = 'm rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_repository_status_02():
    r'''Work with Git inside score.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    input_ = 'red~example~score m rst q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_repository_status_03():
    r'''Work with Subversion outside of score.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=False)
    if not manager:
        return
    manager.repository_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents


def test_MaterialPackageWrangler_repository_status_04():
    r'''Work with Subversion inside score.
    '''

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=True)
    if not manager:
        return
    manager.repository_status()
    contents = manager._transcript.contents

    assert 'Repository status for' in contents
    assert '... OK' in contents