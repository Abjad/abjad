# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManagerWrangler_read_only_attributes_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager._material_manager_wrangler

    assert wrangler._breadcrumb == 'material managers'
    string = 'scoremanager.managers'
    assert wrangler._current_storehouse_package_path == string

    string = 'scoremanager.managers.__temporary_package'
    assert wrangler._temporary_asset_package_path == string
