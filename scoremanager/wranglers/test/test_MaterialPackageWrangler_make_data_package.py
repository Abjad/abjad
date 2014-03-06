# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnumbers',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]

    try:
        wrangler.make_data_package(pending_user_input='testnumbers q')
        assert os.path.exists(path)
        manager = scoremanager.managers.MaterialManager(path)
        assert manager._list() == directory_entries
    finally:
        manager._remove()
        assert not os.path.exists(path)
