# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetWrangler_make_asset_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_stylesheets_directory_path,
        'test-stylesheet.ily',
        )

    assert not os.path.exists(path)
    try:
        string = 'lmy new 1 test-stylesheet q'
        score_manager._run(pending_user_input=string)
        assert os.path.exists(path)
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)
