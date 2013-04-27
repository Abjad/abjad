import os
from experimental import *

score_manager_object = scoremanagertools.core.ScoreManagerObject()


def test_ScoreManagementObject_package_path_to_directory_path_01():

    assert score_manager_object.package_path_to_directory_path('materials') == \
        score_manager_object.configuration.SCORE_MANAGER_MATERIALS_DIRECTORY_PATH
    assert score_manager_object.package_path_to_directory_path('sketches') == \
        score_manager_object.configuration.SCORE_MANAGER_SKETCHES_DIRECTORY_PATH
    assert score_manager_object.package_path_to_directory_path('specifiers') == \
        score_manager_object.configuration.SCORE_MANAGER_SPECIFIERS_DIRECTORY_PATH
