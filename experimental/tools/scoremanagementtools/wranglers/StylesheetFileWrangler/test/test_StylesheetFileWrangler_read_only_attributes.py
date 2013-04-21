import os
from experimental import *


def test_StylesheetFileWrangler_read_only_attributes_01():

    score_manager = scoremanagementtools.scoremanager.ScoreManager()
    wrangler = score_manager.stylesheet_file_wrangler

    assert os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'stylesheets', 'clean_letter_14.ly') in \
        wrangler.list_score_external_asset_path_names()
