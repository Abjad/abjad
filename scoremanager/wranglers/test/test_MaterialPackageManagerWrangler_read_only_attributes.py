# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageManagerWrangler_read_only_attributes_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager._material_package_manager_wrangler

    assert wrangler._breadcrumb == 'material package managers'
    string = 'scoremanager.materialpackagemanagers'
    assert wrangler._current_storehouse_packagesystem_path == string

    assert wrangler.score_package_asset_storehouse_path_infix_parts is None

    string = 'scoremanager.materialpackagemanagers.__temporary_package'
    assert wrangler._temporary_asset_package_path == string
