# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_RhythmMakerPackageSelector_list_current_material_package_directory_paths_01():

    selector = scoremanagertools.selectors.RhythmMakerPackageSelector()
    selector.session._snake_case_current_score_name = 'red_example_score'
    assert selector.list_current_material_directory_paths() == []
