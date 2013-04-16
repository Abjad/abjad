import os
from experimental import *


def test_StylesheetFileWrangler_read_only_attributes_01():

    studio = scoremanagementtools.studio.Studio()
    wrangler = studio.stylesheet_file_wrangler

    assert os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'clean_letter_14.ly') in \
        wrangler.list_score_external_asset_path_names()
