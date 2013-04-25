import os
from experimental import *

score_management_object = scoremanagertools.core.ScoreManagerObject()
score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
scores_directory_path = score_manager_configuration.SCORES_DIRECTORY_PATH


def test_ScoreManagerObject_path_name_to_package_importable_name_01():

    assert score_management_object.path_name_to_package_importable_name(os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY')) == 'materials'
    assert score_management_object.path_name_to_package_importable_name(os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY')) == 'specifiers'
    assert score_management_object.path_name_to_package_importable_name(os.environ.get('SCORE_MANAGER_CHUNKS_DIRECTORY')) == 'sketches'


def test_ScoreManagerObject_path_name_to_package_importable_name_02():

    path = os.path.join(scores_directory_path, 'example_score_1')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1'

    path = os.path.join(scores_directory_path, 'example_score_1', 'mus')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.mus'

    path = os.path.join(scores_directory_path, 'example_score_1', 'mus', 'materials')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.mus.materials'


def test_ScoreManagerObject_path_name_to_package_importable_name_03():

    path = os.path.join(scores_directory_path, 'example_score_1', 'foo')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.foo'

    path = os.path.join(scores_directory_path, 'example_score_1', 'foo.py')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.foo'
