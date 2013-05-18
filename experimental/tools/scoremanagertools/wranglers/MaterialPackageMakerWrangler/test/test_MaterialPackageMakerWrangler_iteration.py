from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.material_package_maker_wrangler


def test_MaterialPackageMakerWrangler_iteration_01():

    assert wrangler.list_score_asset_packagesystem_paths() == []


def test_MaterialPackageMakerWrangler_iteration_02():

    assert wrangler._list_score_storehouse_package_paths() == []


def test_MaterialPackageMakerWrangler_iteration_03():

    assert 'scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker' in \
        wrangler.list_asset_packagesystem_paths()


def test_MaterialPackageMakerWrangler_iteration_04():

    assert ('scoremanagertools.materialpackagemakers.PitchRangeInventoryMaterialPackageMaker',
        'pitch range inventory material package maker') in wrangler._make_visible_asset_menu_tokens()
