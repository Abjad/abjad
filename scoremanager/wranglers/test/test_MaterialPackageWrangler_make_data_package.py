# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testnumbers'
    assert not wrangler._configuration.package_exists(string)
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnumbers',
        )

    try:
        wrangler.make_data_package(pending_user_input='testnumbers q')
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialManager(path)
        assert manager._list() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)
