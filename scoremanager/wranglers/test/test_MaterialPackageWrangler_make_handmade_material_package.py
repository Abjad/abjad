# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testnotes'
    assert not wrangler._configuration.package_exists(string)
    filesystem_path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnotes',
        )

    try:
        wrangler.make_handmade_material_package(
            pending_user_input='testnotes q')
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialManager(filesystem_path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)
