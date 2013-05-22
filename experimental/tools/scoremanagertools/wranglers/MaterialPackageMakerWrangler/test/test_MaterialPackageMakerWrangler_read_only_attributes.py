from experimental import *


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.material_package_maker_wrangler

    assert wrangler._breadcrumb == 'material package makers'
    assert wrangler._current_storehouse_packagesystem_path == \
        'experimental.tools.scoremanagertools.materialpackagemakers'

    assert wrangler._list_built_in_external_storehouse_packagesystem_path() == \
        ['experimental.tools.scoremanagertools.materialpackagemakers']
    assert wrangler.storehouse_path_infix_parts == ()

    assert wrangler._temporary_asset_package_path == \
        'experimental.tools.scoremanagertools.materialpackagemakers.__temporary_package'

    assert wrangler._list_storehouse_package_paths() == [
        'experimental.tools.scoremanagertools.materialpackagemakers']
