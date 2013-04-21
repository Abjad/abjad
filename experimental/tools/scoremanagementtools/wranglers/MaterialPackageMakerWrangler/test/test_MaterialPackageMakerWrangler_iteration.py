from experimental import *

score_manager = scoremanagementtools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_maker_wrangler


def test_MaterialPackageMakerWrangler_iteration_01():

    assert wrangler.list_score_internal_asset_importable_names() == []


def test_MaterialPackageMakerWrangler_iteration_02():

    assert wrangler.list_score_internal_asset_container_importable_names() == []


def test_MaterialPackageMakerWrangler_iteration_03():

    assert 'scoremanagementtools.makers.PitchRangeInventoryMaterialPackageMaker' in \
        wrangler.list_asset_importable_names()


def test_MaterialPackageMakerWrangler_iteration_04():

    assert ('scoremanagementtools.makers.PitchRangeInventoryMaterialPackageMaker',
        'pitch range inventory material package maker') in wrangler.make_visible_asset_menu_tokens()


def test_MaterialPackageMakerWrangler_iteration_05():

    assert 'pitch range inventory material package maker' in wrangler.list_asset_human_readable_names()
