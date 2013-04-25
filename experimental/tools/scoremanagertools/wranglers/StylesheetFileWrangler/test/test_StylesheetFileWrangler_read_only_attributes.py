import os
from experimental import *


def test_StylesheetFileWrangler_read_only_attributes_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    wrangler = score_manager.stylesheet_file_wrangler

    path = os.path.join(
        score_manager.configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 
        'stylesheets', 'clean_letter_14.ly')
    assert path in wrangler.list_score_external_asset_path_names()
