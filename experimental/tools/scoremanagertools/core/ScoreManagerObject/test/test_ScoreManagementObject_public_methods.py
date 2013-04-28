import os
from experimental import *


def test_ScoreManagementObject_public_methods_01():

    score_manager_object = scoremanagertools.core.ScoreManagerObject()

    path = os.path.join(
        score_manager_object.configuration.score_manager_tools_directory_path, 
        'scoremanager', 'ScoreManager', 'ScoreManager.py')
    assert score_manager_object.module_path_to_file_path(
        'scoremanagertools.scoremanager.ScoreManager.ScoreManager') == path

    path = score_manager_object.configuration.score_manager_tools_directory_path
    assert score_manager_object.package_path_to_directory_path('scoremanagertools') == path
