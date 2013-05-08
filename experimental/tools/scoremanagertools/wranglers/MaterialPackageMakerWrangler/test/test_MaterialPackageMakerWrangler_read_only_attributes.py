from experimental import *


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.material_package_maker_wrangler

    assert wrangler.breadcrumb == 'material package makers'
    assert wrangler.current_asset_container_package_path == 'scoremanagertools.materialpackagemakers'
    assert all([
        x.startswith('scoremanagertools.materialpackagemakers.') for x in wrangler.list_score_external_asset_package_paths()])

    assert wrangler.list_system_asset_container_package_paths() == \
        ['scoremanagertools.materialpackagemakers']
    assert wrangler.score_internal_asset_container_package_path_infix is None

    assert wrangler.temporary_asset_package_path == 'scoremanagertools.materialpackagemakers.__temporary_package'

    assert wrangler.list_asset_container_package_paths() == ['scoremanagertools.materialpackagemakers']
