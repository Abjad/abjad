# -*- encoding: utf-8 -*-
from experimental import *


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.core.ScoreManager()
    wrangler = score_manager.material_package_maker_wrangler

    assert wrangler._breadcrumb == 'material package makers'
    assert wrangler._current_storehouse_packagesystem_path == \
        'scoremanagertools.materialpackagemakers'

    assert wrangler.score_package_asset_storehouse_path_infix_parts is None

    assert wrangler._temporary_asset_package_path == \
        'scoremanagertools.materialpackagemakers.__temporary_package'
