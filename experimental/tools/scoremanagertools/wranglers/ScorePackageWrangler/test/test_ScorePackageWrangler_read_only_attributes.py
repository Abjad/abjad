import os
from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.score_package_wrangler


def test_ScorePackageWrangler_read_only_attributes_01():
    '''Breadcrumb.
    '''

    assert wrangler._breadcrumb == 'scores'


def test_ScorePackageWrangler_read_only_attributes_02():
    '''Asset containers.
    '''

    assert 'experimental.tools.scoremanagertools.built_in_scores.red_example_score' in \
        wrangler._list_asset_container_package_paths()
    directory_path = os.path.join(wrangler.configuration.built_in_scores_directory_path, 'red_example_score')
    assert directory_path in wrangler._list_asset_container_filesystem_paths()


def test_ScorePackageWrangler_read_only_attributes_03():
    '''Current asset container.
    '''

    assert wrangler.current_asset_container_packagesystem_path == ''
    assert wrangler.current_asset_container_filesystem_path == wrangler.configuration.user_scores_directory_path


def test_ScorePackageWrangler_read_only_attributes_04():
    '''Score-external asset container.
    '''

    assert wrangler._list_built_in_score_external_asset_container_packagesystem_path() == [
        'experimental.tools.scoremanagertools.built_in_scores']


def test_ScorePackageWrangler_read_only_attributes_05():
    '''Score-external assets.
    '''

    assert wrangler.list_score_external_asset_packagesystem_paths() == []


def test_ScorePackageWrangler_read_only_attributes_06():
    '''Infix.
    '''

    assert wrangler.asset_container_path_infix_parts == ()


def test_ScorePackageWrangler_read_only_attributes_07():
    '''Temporary asset.
    '''

    assert wrangler._temporary_asset_package_path == '__temporary_package'


def test_ScorePackageWrangler_read_only_attributes_08():
    '''Other read-only attributes.
    '''

    assert 'Red Example Score (2013)' in wrangler.visible_score_titles_with_years
