import os
from experimental import *


def test_package_path_to_directory_path_01():

    configuration = scoremanagertools.core.ScoreManagerConfiguration()

    assert packagesystemtools.package_path_to_directory_path('built_in_materials') == \
        configuration.built_in_materials_directory_path
    assert packagesystemtools.package_path_to_directory_path('sketches') == \
        configuration.user_sketches_directory_path
    assert packagesystemtools.package_path_to_directory_path('built_in_specifiers') == \
        configuration.built_in_specifiers_directory_path

