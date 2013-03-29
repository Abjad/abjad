import os
import scf

scf_object = scf.core.SCFObject()


def test_SCFObject_path_name_to_package_importable_name_01():

    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFMATERIALSPATH')) == 'materials'
    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFSPECIFIERSPATH')) == 'specifiers'
    assert scf_object.path_name_to_package_importable_name(os.environ.get('SCFCHUNKSPATH')) == 'sketches'


def test_SCFObject_path_name_to_package_importable_name_02():

    path = os.path.join(os.environ.get('SCORES'), 'aracilik')
    assert scf_object.path_name_to_package_importable_name(path) == 'aracilik'

    path = os.path.join(os.environ.get('SCORES'), 'aracilik', 'mus')
    assert scf_object.path_name_to_package_importable_name(path) == 'aracilik.mus'

    path = os.path.join(os.environ.get('SCORES'), 'aracilik', 'mus', 'materials')
    assert scf_object.path_name_to_package_importable_name(path) == 'aracilik.mus.materials'


def test_SCFObject_path_name_to_package_importable_name_03():

    path = os.path.join(os.environ.get('SCORES'), 'aracilik', 'foo')
    assert scf_object.path_name_to_package_importable_name(path) == 'aracilik.foo'

    path = os.path.join(os.environ.get('SCORES'), 'aracilik', 'foo.py')
    assert scf_object.path_name_to_package_importable_name(path) == 'aracilik.foo'
