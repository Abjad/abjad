import os
from experimental import *

score_manager_object = scoremanagertools.core.ScoreManagerObject()


def test_ScoreManagerObject_package_importable_name_to_path_01():

    assert score_manager_object.package_importable_name_to_path('materials') == os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY')
    assert score_manager_object.package_importable_name_to_path('sketches') == os.environ.get('SCORE_MANAGER_CHUNKS_DIRECTORY')
    assert score_manager_object.package_importable_name_to_path('specifiers') == os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY')
