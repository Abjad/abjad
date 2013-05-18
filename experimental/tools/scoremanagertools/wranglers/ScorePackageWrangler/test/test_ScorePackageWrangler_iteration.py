from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.score_package_wrangler


def test_ScorePackageWrangler_iteration_01():

    assert 'experimental.tools.scoremanagertools.built_in_scores.red_example_score' in \
        wrangler.list_score_asset_packagesystem_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.examle_score_1' not in \
        wrangler.list_score_asset_packagesystem_paths(
            head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler.list_score_asset_packagesystem_paths(head='asdf') == []


def test_ScorePackageWrangler_iteration_02():

    assert 'experimental.tools.scoremanagertools.built_in_scores.red_example_score' in \
        wrangler._list_score_storehouse_package_paths()
    assert 'experimental.tools.scoremanagertools.built_in_scores.red_example_score' not in \
        wrangler._list_score_storehouse_package_paths(
        head='experimental.tools.scoremanagertools.built_in_scores.green_example_score')
    assert wrangler._list_score_storehouse_package_paths(head='asdf') == []
