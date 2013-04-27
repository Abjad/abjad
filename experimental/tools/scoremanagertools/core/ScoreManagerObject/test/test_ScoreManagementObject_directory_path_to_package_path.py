import os
from experimental import *

score_manager_object = scoremanagertools.core.ScoreManagerObject()
score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
scores_directory_path = score_manager_configuration.SCORES_DIRECTORY_PATH


def test_ScoreManagementObject_directory_path_to_package_path_01():

    assert score_manager_object.directory_path_to_package_path(
        score_manager_configuration.SCORE_MANAGER_MATERIALS_DIRECTORY_PATH) == 'materials'
    assert score_manager_object.directory_path_to_package_path(
        score_manager_configuration.SCORE_MANAGER_SPECIFIERS_DIRECTORY_PATH) == 'specifiers'
    assert score_manager_object.directory_path_to_package_path(
        score_manager_configuration.SCORE_MANAGER_SKETCHES_DIRECTORY_PATH) == 'sketches'


def test_ScoreManagementObject_directory_path_to_package_path_02():

    path = os.path.join(scores_directory_path, 'example_score_1')
    assert score_manager_object.directory_path_to_package_path(path) == 'example_score_1'

    path = os.path.join(scores_directory_path, 'example_score_1', 'mus')
    assert score_manager_object.directory_path_to_package_path(path) == 'example_score_1.mus'

    path = os.path.join(scores_directory_path, 'example_score_1', 'mus', 'materials')
    assert score_manager_object.directory_path_to_package_path(path) == 'example_score_1.mus.materials'


def test_ScoreManagementObject_directory_path_to_package_path_03():

    path = os.path.join(scores_directory_path, 'example_score_1', 'foo')
    assert score_manager_object.directory_path_to_package_path(path) == 'example_score_1.foo'

    path = os.path.join(scores_directory_path, 'example_score_1', 'foo.py')
    assert score_manager_object.directory_path_to_package_path(path) == 'example_score_1.foo'
