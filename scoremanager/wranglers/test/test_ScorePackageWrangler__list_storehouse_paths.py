# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_ScorePackageWrangler__list_storehouse_paths_01():
    r'''Abjad score packages directory.
    '''
    
    wrangler = scoremanager.wranglers.ScorePackageWrangler()
    
    paths = [
        wrangler._configuration.abjad_score_packages_directory_path,
        ]

    # TODO: should be possible to set abjad_library=False
    result = wrangler._list_storehouse_paths(
        abjad_library=True,
        abjad_score_packages=True,
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
