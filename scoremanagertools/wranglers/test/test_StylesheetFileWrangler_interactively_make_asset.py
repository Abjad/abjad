# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_StylesheetFileWrangler_interactively_make_asset_01():

    score_manager = scoremanagertools.core.ScoreManager()
    configuration = score_manager.configuration
    filesystem_path = os.path.join(
        configuration.user_asset_library_stylesheets_directory_path,
        'test-stylesheet.ly')

    assert not os.path.exists(filesystem_path)

    try:
        score_manager._run(
            pending_user_input='y new 1 test-stylesheet q', is_test=True)
        assert os.path.exists(filesystem_path)
    finally:
        os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
