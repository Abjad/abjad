from experimental import *


def test_MaterialPackageMakerWrangler_read_only_attributes_01():

    score_manager = scoremanagementtools.studio.ScoreManager()
    wrangler = score_manager.material_package_maker_wrangler

    assert wrangler.breadcrumb == 'material package makers'
    assert wrangler.current_asset_container_importable_name == 'scoremanagementtools.makers'
    assert all([
        x.startswith('scoremanagementtools.makers.') for x in wrangler.list_score_external_asset_importable_names()])

    assert wrangler.list_score_external_asset_container_importable_names() == \
        ['scoremanagementtools.makers']
    assert wrangler.score_internal_asset_container_importable_name_infix is None

    assert wrangler.temporary_asset_importable_name == 'scoremanagementtools.makers.__temporary_package'

    assert wrangler.list_asset_container_importable_names() == ['scoremanagementtools.makers']
