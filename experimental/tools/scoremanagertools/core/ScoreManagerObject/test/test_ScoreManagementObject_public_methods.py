import os
from experimental import *


def test_ScoreManagementObject_public_methods_01():

    score_manager_object = scoremanagertools.core.ScoreManagerObject()

    file_path = os.path.join(
        score_manager_object.configuration.score_manager_tools_directory_path, 
        'scoremanager', 'ScoreManager', 'ScoreManager.py')
    assert score_manager_object.module_path_to_file_path(
        'scoremanagertools.scoremanager.ScoreManager.ScoreManager') == file_path

    directory_path = score_manager_object.configuration.score_manager_tools_directory_path
    assert score_manager_object.package_path_to_directory_path('scoremanagertools') == directory_path
