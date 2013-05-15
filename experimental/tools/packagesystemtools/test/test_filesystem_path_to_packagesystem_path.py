import os
from experimental import *

configuration = scoremanagertools.core.ScoreManagerConfiguration()
user_scores_directory_path = configuration.user_scores_directory_path


def test_filesystem_path_to_packagesystem_path_01():

    assert packagesystemtools.filesystem_path_to_packagesystem_path(
        configuration.built_in_materials_directory_path) == 'built_in_materials'
    assert packagesystemtools.filesystem_path_to_packagesystem_path(
        configuration.built_in_specifiers_directory_path) == 'built_in_specifiers'
    assert packagesystemtools.filesystem_path_to_packagesystem_path(
        configuration.user_sketches_directory_path) == 'sketches'


def test_filesystem_path_to_packagesystem_path_02():

    directory_path = os.path.join(user_scores_directory_path, 'red_example_score')
    assert packagesystemtools.filesystem_path_to_packagesystem_path(directory_path) == 'red_example_score'

    directory_path = os.path.join(user_scores_directory_path, 'red_example_score', 'music')
    assert packagesystemtools.filesystem_path_to_packagesystem_path(directory_path) == 'red_example_score.music'

    directory_path = os.path.join(user_scores_directory_path, 'red_example_score', 'music', 'materials')
    assert packagesystemtools.filesystem_path_to_packagesystem_path(directory_path) == \
        'red_example_score.music.materials'


def test_filesystem_path_to_packagesystem_path_03():

    directory_path = os.path.join(user_scores_directory_path, 'red_example_score', 'foo')
    assert packagesystemtools.filesystem_path_to_packagesystem_path(directory_path) == 'red_example_score.foo'

    file_path = os.path.join(user_scores_directory_path, 'red_example_score', 'foo.py')
    assert packagesystemtools.filesystem_path_to_packagesystem_path(file_path) == 'red_example_score.foo'
