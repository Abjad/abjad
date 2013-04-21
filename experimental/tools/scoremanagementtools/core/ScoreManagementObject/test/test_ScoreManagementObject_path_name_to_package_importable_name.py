import os
from experimental import *

scf_object = scoremanagementtools.core.ScoreManagementObject()


def test_ScoreManagementObject_path_name_to_package_importable_name_01():

    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFMATERIALSPATH')) == 'materials'
    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFSPECIFIERSPATH')) == 'specifiers'
    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFCHUNKSPATH')) == 'sketches'


def test_ScoreManagementObject_path_name_to_package_importable_name_02():

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1')
    assert scf_object.path_name_to_package_importable_name(path) == 'example_score_1'

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus')
    assert scf_object.path_name_to_package_importable_name(path) == 'example_score_1.mus'

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus', 'materials')
    assert scf_object.path_name_to_package_importable_name(path) == 'example_score_1.mus.materials'


def test_ScoreManagementObject_path_name_to_package_importable_name_03():

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'foo')
    assert scf_object.path_name_to_package_importable_name(path) == 'example_score_1.foo'

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'foo.py')
    assert scf_object.path_name_to_package_importable_name(path) == 'example_score_1.foo'
