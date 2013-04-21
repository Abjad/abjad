import os
from experimental import *


def test_ScoreManagementObject_public_methods_01():

    score_management_object = scoremanagementtools.core.ScoreManagementObject()

    path = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'scoremanager', 'ScoreManager', 'ScoreManager.py')
    assert score_management_object.module_importable_name_to_path_name(
        'scoremanagementtools.scoremanager.ScoreManager.ScoreManager') == path

    path = os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH')
    assert score_management_object.package_importable_name_to_path_name('scoremanagementtools') == path
