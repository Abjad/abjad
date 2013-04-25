import os
from experimental import *


def test_RhythmMakerPackageSelector_list_current_material_package_path_names_01():

    selector = scoremanagertools.selectors.RhythmMakerPackageSelector()
    selector.session._current_score_package_short_name = 'example_score_1'
    assert selector.list_current_material_package_paths() == []
