# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetFileWrangler_interactively_make_asset_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager.configuration
    filesystem_path = os.path.join(
        configuration.user_library_stylesheets_directory_path,
        'test-stylesheet.ily',
        )

    assert not os.path.exists(filesystem_path)

    try:
        string = 'lmy new 1 test-stylesheet q'
        score_manager._run(pending_user_input=string, is_test=True)
        assert os.path.exists(filesystem_path)
    finally:
        os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
