# -*- encoding: utf-8 -*-
import os
import pytest
pytest.skip('change user material_packages/ to materials/.')
from abjad import *
import scoremanager
session = scoremanager.core.Session()
wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)


def test_MaterialPackageWrangler__find_up_to_date_manager_01():
    r'''Works with Git.
    '''

    manager = wrangler._find_up_to_date_manager(
        system=True,
        repository='git',
        )

    assert isinstance(manager, scoremanager.managers.MaterialManager)
    assert manager._is_git_versioned()
    assert manager._is_up_to_date()
    assert os.path.dirname(manager._path) == 'materials'


def test_MaterialPackageWrangler__find_up_to_date_manager_02():
    r'''Works with Subversion.
    '''

    manager = wrangler._find_up_to_date_manager(
        system=False,
        repository='svn',
        )

    if not manager:
        return

    assert isinstance(manager, scoremanager.managers.MaterialManager)
    assert manager._is_svn_versioned()
    assert manager._is_up_to_date()
    assert os.path.dirname(manager._path) == 'materials'