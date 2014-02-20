# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetFileWrangler_interactively_select_asset_filesystem_path_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager._stylesheet_file_wrangler
    wrangler.session.pending_user_input = 'clean'
    filesystem_path = wrangler.interactively_select_asset_filesystem_path()

    assert filesystem_path == os.path.join(
        score_manager.configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )
