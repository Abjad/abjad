from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.score_package_wrangler


def test_ScorePackageWrangler_iteration_01():

    assert 'example_score_1' in wrangler.list_score_internal_asset_package_paths()
    assert 'examle_score_1' not in wrangler.list_score_internal_asset_package_paths(
        head='example_score_2')
    assert wrangler.list_score_internal_asset_package_paths(head='asdf') == []


def test_ScorePackageWrangler_iteration_02():

    assert 'example_score_1' in wrangler.list_score_internal_asset_container_package_paths()
    assert 'example_score_1' not in wrangler.list_score_internal_asset_container_package_paths(
        head='example_score_2')
    assert wrangler.list_score_internal_asset_container_package_paths(head='asdf') == []
