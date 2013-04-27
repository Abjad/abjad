import os
from experimental import *


def test_ScoreManagementObject_public_methods_01():

    score_manager_object = scoremanagertools.core.ScoreManagerObject()

    path = os.path.join(
        score_manager_object.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH, 
        'scoremanager', 'ScoreManager', 'ScoreManager.py')
    assert score_manager_object.module_path_to_file_path(
        'scoremanagertools.scoremanager.ScoreManager.ScoreManager') == path

    path = score_manager_object.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH
    assert score_manager_object.package_importable_name_to_directory_path('scoremanagertools') == path
