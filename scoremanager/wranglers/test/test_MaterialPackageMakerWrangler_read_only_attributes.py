# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager.material_package_maker_wrangler

    assert wrangler._breadcrumb == 'material package makers'
    string = 'scoremanager.materialpackagemakers'
    assert wrangler._current_storehouse_packagesystem_path == string

    assert wrangler.score_package_asset_storehouse_path_infix_parts is None

    string = 'scoremanager.materialpackagemakers.__temporary_package'
    assert wrangler._temporary_asset_package_path == string
