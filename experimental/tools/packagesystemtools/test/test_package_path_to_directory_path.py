import os
from experimental import *


def test_packagesystem_path_to_filesystem_path_01():

    configuration = scoremanagertools.core.ScoreManagerConfiguration()

    assert packagesystemtools.packagesystem_path_to_filesystem_path('built_in_materials') == \
        configuration.built_in_materials_directory_path
    assert packagesystemtools.packagesystem_path_to_filesystem_path('sketches') == \
        configuration.user_sketches_directory_path
    assert packagesystemtools.packagesystem_path_to_filesystem_path('built_in_specifiers') == \
        configuration.built_in_specifiers_directory_path

