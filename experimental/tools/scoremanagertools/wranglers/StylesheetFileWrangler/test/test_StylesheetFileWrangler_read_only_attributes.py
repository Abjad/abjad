import os
from experimental import *


def test_StylesheetFileWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.stylesheet_file_wrangler

    file_path = os.path.join(
        score_manager.configuration.score_manager_tools_directory_path, 
        'stylesheets', 'clean_letter_14.ly')
    assert file_path in wrangler.list_score_external_asset_paths()
