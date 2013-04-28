import os
from experimental import *

score_manager_object = scoremanagertools.core.ScoreManagerObject()


def test_ScoreManagementObject_package_path_to_directory_path_01():

    assert score_manager_object.package_path_to_directory_path('materials') == \
        score_manager_object.configuration.score_manager_materials_directory_path
    assert score_manager_object.package_path_to_directory_path('sketches') == \
        score_manager_object.configuration.score_manager_sketches_directory_path
    assert score_manager_object.package_path_to_directory_path('specifiers') == \
        score_manager_object.configuration.score_manager_specifiers_directory_path
