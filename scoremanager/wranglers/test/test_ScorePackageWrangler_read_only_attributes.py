# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager

score_manager = scoremanager.core.ScoreManager()
wrangler = score_manager._score_package_wrangler


def test_ScorePackageWrangler_read_only_attributes_01():
    r'''Breadcrumb.
    '''

    assert wrangler._breadcrumb == 'scores'


def test_ScorePackageWrangler_read_only_attributes_02():
    r'''Current storehouse.
    '''

    assert wrangler._current_storehouse_package_path == ''
    assert wrangler._current_storehouse_directory_path == \
        wrangler.configuration.user_score_packages_directory_path


def test_ScorePackageWrangler_read_only_attributes_03():
    r'''Temporary asset.
    '''

    assert wrangler._temporary_asset_package_path == '__temporary_package'
