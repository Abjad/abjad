import os
from experimental import *


def test_package_path_to_directory_path_01():

    configuration = scoremanagertools.core.ScoreManagerConfiguration()

    assert packagepathtools.package_path_to_directory_path('materials') == \
        configuration.system_materials_directory_path
    assert packagepathtools.package_path_to_directory_path('sketches') == \
        configuration.score_manager_sketches_directory_path
    assert packagepathtools.package_path_to_directory_path('specifiers') == \
        configuration.score_manager_specifiers_directory_path

