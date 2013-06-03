import os
from experimental import *


def test_StylesheetFileWrangler_interactively_select_asset_filesystem_path_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.stylesheet_file_wrangler
    wrangler._session.user_input = 'clean'
    filesystem_path = wrangler.interactively_select_asset_filesystem_path()

    assert filesystem_path == os.path.join(
        score_manager.configuration.built_in_stylesheets_directory_path,
        'clean-letter-14.ly')
