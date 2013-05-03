import os
from experimental import *

configuration = scoremanagertools.core.ScoreManagerConfiguration()
scores_directory_path = configuration.scores_directory_path


def test_directory_path_to_package_path_01():

    assert packagepathtools.directory_path_to_package_path(
        configuration.score_manager_materials_directory_path) == 'materials'
    assert packagepathtools.directory_path_to_package_path(
        configuration.score_manager_specifiers_directory_path) == 'specifiers'
    assert packagepathtools.directory_path_to_package_path(
        configuration.score_manager_sketches_directory_path) == 'sketches'


def test_directory_path_to_package_path_02():

    directory_path = os.path.join(scores_directory_path, 'example_score_1')
    assert packagepathtools.directory_path_to_package_path(directory_path) == 'example_score_1'

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'mus')
    assert packagepathtools.directory_path_to_package_path(directory_path) == 'example_score_1.mus'

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'mus', 'materials')
    assert packagepathtools.directory_path_to_package_path(directory_path) == \
        'example_score_1.mus.materials'


def test_directory_path_to_package_path_03():

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'foo')
    assert packagepathtools.directory_path_to_package_path(directory_path) == 'example_score_1.foo'

    file_path = os.path.join(scores_directory_path, 'example_score_1', 'foo.py')
    assert packagepathtools.directory_path_to_package_path(file_path) == 'example_score_1.foo'
