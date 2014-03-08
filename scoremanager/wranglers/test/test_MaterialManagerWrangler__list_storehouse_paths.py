# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManagerWrangler__list_storehouse_paths_01():
    
    wrangler = scoremanager.wranglers.MaterialManagerWrangler()
    
    paths = [
        wrangler._configuration.abjad_material_managers_directory_path,
        ]

    result = wrangler._list_storehouse_paths(
        user_library=False,
        user_score_packages=False,
        )

    assert result == paths
