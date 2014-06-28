# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_StylesheetWrangler__select_asset_path_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    wrangler = ide._stylesheet_wrangler
    input_ = 'clean'
    wrangler._session._pending_input = input_
    path = wrangler._select_asset_path()

    assert path == os.path.join(
        ide._configuration.example_stylesheets_directory,
        'clean-letter-14.ily',
        )