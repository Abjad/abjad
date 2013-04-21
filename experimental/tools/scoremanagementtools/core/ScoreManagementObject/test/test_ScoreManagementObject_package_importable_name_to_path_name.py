import os
from experimental import *

scf_object = scoremanagementtools.core.ScoreManagementObject()


def test_ScoreManagementObject_package_importable_name_to_path_name_01():

    assert scf_object.package_importable_name_to_path_name('materials') == os.environ.get('SCFMATERIALSPATH')
    assert scf_object.package_importable_name_to_path_name('sketches') == os.environ.get('SCFCHUNKSPATH')
    assert scf_object.package_importable_name_to_path_name('specifiers') == os.environ.get('SCFSPECIFIERSPATH')
