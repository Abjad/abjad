from experimental import *


def test_PackageWrangler_read_only_attributes_01():

    wrangler = scoremanagertools.wranglers.PackageWrangler()

    assert wrangler.list_score_external_asset_container_package_importable_names() == []
    assert wrangler.score_internal_asset_container_package_importable_name_infix is None
    assert 'example_score_1' in \
        wrangler.list_score_internal_asset_container_package_importable_names()
    assert wrangler.list_score_external_asset_package_importable_names() == []
    assert 'example_score_1' in wrangler.list_score_internal_asset_package_importable_names()
