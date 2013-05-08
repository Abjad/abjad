import os
from experimental import *

configuration = scoremanagertools.core.ScoreManagerConfiguration()
scores_directory_path = configuration.scores_directory_path


def test_filesystem_path_to_package_path_01():

    assert packagepathtools.filesystem_path_to_package_path(
        configuration.system_materials_directory_path) == 'system_materials'
    assert packagepathtools.filesystem_path_to_package_path(
        configuration.system_specifiers_directory_path) == 'specifiers'
    assert packagepathtools.filesystem_path_to_package_path(
        configuration.user_sketches_directory_path) == 'sketches'


def test_filesystem_path_to_package_path_02():

    directory_path = os.path.join(scores_directory_path, 'example_score_1')
    assert packagepathtools.filesystem_path_to_package_path(directory_path) == 'example_score_1'

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'music')
    assert packagepathtools.filesystem_path_to_package_path(directory_path) == 'example_score_1.music'

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'music', 'materials')
    assert packagepathtools.filesystem_path_to_package_path(directory_path) == \
        'example_score_1.music.materials'


def test_filesystem_path_to_package_path_03():

    directory_path = os.path.join(scores_directory_path, 'example_score_1', 'foo')
    assert packagepathtools.filesystem_path_to_package_path(directory_path) == 'example_score_1.foo'

    file_path = os.path.join(scores_directory_path, 'example_score_1', 'foo.py')
    assert packagepathtools.filesystem_path_to_package_path(file_path) == 'example_score_1.foo'
