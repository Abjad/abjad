# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        wrangler.make_data_package(pending_user_input='testnumbers q')
        assert wrangler.configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        manager._remove()
        assert not wrangler.configuration.package_exists(string)
