from experimental import *


def test_PackageWrangler_read_only_attributes_01():

    wrangler = scoremanagertools.wranglers.PackageWrangler()

    assert wrangler.list_score_external_asset_container_package_paths() == []
    assert wrangler.score_internal_asset_container_package_path_infix is None
    assert 'example_score_1' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert wrangler.list_score_external_asset_package_paths() == []
    assert 'example_score_1' in wrangler.list_score_internal_asset_package_paths()
