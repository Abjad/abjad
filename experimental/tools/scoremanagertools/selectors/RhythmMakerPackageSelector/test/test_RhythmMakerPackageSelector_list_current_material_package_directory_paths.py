import os
from experimental import *


def test_RhythmMakerPackageSelector_list_current_material_package_directory_paths_01():

    selector = scoremanagertools.selectors.RhythmMakerPackageSelector()
    selector._session._underscore_delimited_current_score_name = 'example_score_1'
    assert selector.list_current_material_directory_paths() == []
