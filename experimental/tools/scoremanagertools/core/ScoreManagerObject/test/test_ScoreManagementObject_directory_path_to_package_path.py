import os
from experimental import *

score_manager_object = scoremanagertools.core.ScoreManagerObject()
score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
scores_directory_path = score_manager_configuration.scores_directory_path


def test_ScoreManagementObject_directory_path_to_package_path_01():

    assert score_manager_object.directory_path_to_package_path(
        score_manager_configuration.score_manager_materials_directory_path) == 'materials'
    assert score_manager_object.directory_path_to_package_path(
        score_manager_configuration.score_manager_specifiers_directory_path) == 'specifiers'
    assert score_manager_object.directory_path_to_package_path(
        score_manager_configuration.score_manager_sketches_directory_path) == 'sketches'


def test_ScoreManagementObject_directory_path_to_package_path_02():

    directory_path = os.path.join(scores_directory_path, 'example_score_1')
    assert score_manager_object.directory_path_to_package_path(directory_path) == 'example_score_1'

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'mus')
    assert score_manager_object.directory_path_to_package_path(directory_path) == 'example_score_1.mus'

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'mus', 'materials')
    assert score_manager_object.directory_path_to_package_path(directory_path) == \
        'example_score_1.mus.materials'


def test_ScoreManagementObject_directory_path_to_package_path_03():

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'foo')
    assert score_manager_object.directory_path_to_package_path(directory_path) == 'example_score_1.foo'

    file_path = os.path.join(scores_directory_path, 'example_score_1', 'foo.py')
    assert score_manager_object.directory_path_to_package_path(file_path) == 'example_score_1.foo'
