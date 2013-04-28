import os
from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.score_package_wrangler


def test_ScorePackageWrangler_read_only_attributes_01():
    '''Breadcrumb.
    '''

    assert wrangler.breadcrumb == 'scores'


def test_ScorePackageWrangler_read_only_attributes_02():
    '''Asset containers (all).
    '''

    assert 'example_score_1' in wrangler.list_asset_container_package_paths()
    directory_path = os.path.join(wrangler.configuration.scores_directory_path, 'example_score_1')
    assert directory_path in wrangler.list_asset_container_paths()


def test_ScorePackageWrangler_read_only_attributes_03():
    '''Current asset container.
    '''

    assert wrangler.current_asset_container_package_path is None
    assert wrangler.current_asset_container_path == wrangler.configuration.scores_directory_path


def test_ScorePackageWrangler_read_only_attributes_04():
    '''Score-external asset container.
    '''

    assert wrangler.list_score_external_asset_container_package_paths() == []


def test_ScorePackageWrangler_read_only_attributes_05():
    '''Score-external assets.
    '''

    assert wrangler.list_score_external_asset_package_paths() == []


def test_ScorePackageWrangler_read_only_attributes_06():
    '''Infix.
    '''

    assert wrangler.score_internal_asset_container_package_path_infix is None


def test_ScorePackageWrangler_read_only_attributes_07():
    '''Temporary asset.
    '''

    assert wrangler.temporary_asset_package_path == '__temporary_package'


def test_ScorePackageWrangler_read_only_attributes_08():
    '''Other read-only attributes.
    '''

    assert 'Example Score I (2013)' in wrangler.visible_score_titles_with_years
