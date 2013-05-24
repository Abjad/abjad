import os
from experimental import *

score_manager = scoremanagertools.scoremanager.ScoreManager()
wrangler = score_manager.score_package_wrangler


def test_ScorePackageWrangler_read_only_attributes_01():
    '''Breadcrumb.
    '''

    assert wrangler._breadcrumb == 'scores'


def test_ScorePackageWrangler_read_only_attributes_02():
    '''Current storehouse.
    '''

    assert wrangler._current_storehouse_packagesystem_path == ''
    assert wrangler._current_storehouse_filesystem_path == wrangler.configuration.user_scores_directory_path


def test_ScorePackageWrangler_read_only_attributes_03():
    '''Infix.
    '''

    assert wrangler.storehouse_path_infix_parts == ()


def test_ScorePackageWrangler_read_only_attributes_04():
    '''Temporary asset.
    '''

    assert wrangler._temporary_asset_package_path == '__temporary_package'
