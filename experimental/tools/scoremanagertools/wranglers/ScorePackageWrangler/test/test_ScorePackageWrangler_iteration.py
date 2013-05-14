from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.score_package_wrangler


def test_ScorePackageWrangler_iteration_01():

    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1' in \
        wrangler.list_score_internal_asset_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.examle_score_1' not in \
        wrangler.list_score_internal_asset_package_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler.list_score_internal_asset_package_paths(head='asdf') == []


def test_ScorePackageWrangler_iteration_02():

    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1' in \
        wrangler.list_score_internal_asset_container_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.example_score_1' not in \
        wrangler.list_score_internal_asset_container_package_paths(
        head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler.list_score_internal_asset_container_package_paths(head='asdf') == []
