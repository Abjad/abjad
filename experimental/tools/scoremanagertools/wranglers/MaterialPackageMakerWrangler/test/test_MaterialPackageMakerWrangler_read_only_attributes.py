from experimental import *


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.material_package_maker_wrangler

    assert wrangler._breadcrumb == 'material package makers'
    assert wrangler.current_asset_container_packagesystem_path == 'scoremanagertools.materialpackagemakers'

    assert wrangler._list_built_in_score_external_asset_container_packagesystem_path() == \
        ['scoremanagertools.materialpackagemakers']
    assert wrangler.asset_container_path_infix_parts == ()

    assert wrangler._temporary_asset_package_path == \
        'scoremanagertools.materialpackagemakers.__temporary_package'

    assert wrangler._list_asset_container_package_paths() == ['scoremanagertools.materialpackagemakers']
