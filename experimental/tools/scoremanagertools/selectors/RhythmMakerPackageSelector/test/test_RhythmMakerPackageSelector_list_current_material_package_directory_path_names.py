import os
from experimental import *


def test_RhythmMakerPackageSelector_list_current_material_directory_path_names_01():

    selector = scoremanagertools.selectors.RhythmMakerPackageSelector()
    selector.session._current_score_package_name = 'example_score_1'
    assert selector.list_current_material_directory_paths() == []
