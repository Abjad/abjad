import os
from experimental import *


def test_package_path_to_directory_path_01():

    configuration = scoremanagertools.core.ScoreManagerConfiguration()

    assert packagepathtools.package_path_to_directory_path('system_materials') == \
        configuration.system_materials_directory_path
    assert packagepathtools.package_path_to_directory_path('sketches') == \
        configuration.user_sketches_directory_path
    assert packagepathtools.package_path_to_directory_path('system_specifiers') == \
        configuration.system_specifiers_directory_path

