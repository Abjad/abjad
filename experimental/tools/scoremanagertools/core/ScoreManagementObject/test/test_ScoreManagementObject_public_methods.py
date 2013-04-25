import os
from experimental import *


def test_ScoreManagementObject_public_methods_01():

    score_management_object = scoremanagertools.core.ScoreManagementObject()

    path = os.path.join(
        score_management_object.configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 
        'scoremanager', 'ScoreManager', 'ScoreManager.py')
    assert score_management_object.module_importable_name_to_path_name(
        'scoremanagertools.scoremanager.ScoreManager.ScoreManager') == path

    path = score_management_object.configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH
    assert score_management_object.package_importable_name_to_path_name('scoremanagertools') == path
