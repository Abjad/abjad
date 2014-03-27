# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler__find_up_to_date_manager_01():
    r'''Works with Git.
    '''

    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='git',
        system=True,
        )

    assert isinstance(manager, scoremanager.managers.MaterialManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(os.path.dirname(manager._path)) == 'materials'
    assert not os.path.dirname(manager._path) == 'materials'


def test_MaterialPackageWrangler__find_up_to_date_manager_02():
    r'''Works with Subversion.
    '''

    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_up_to_date_manager(
        repository='svn',
        system=False,
        )

    if not manager:
        return

    assert isinstance(manager, scoremanager.managers.MaterialManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.basename(os.path.dirname(manager._path)) == 'materials'
    assert not os.path.dirname(manager._path) == 'materials'