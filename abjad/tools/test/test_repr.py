from abjad import *
import pytest


class_crawler = documentationtools.ClassCrawler(
    abjad_configuration.abjad_directory_path,
    root_package_name='abjad',
    )
all_classes = class_crawler()

@pytest.mark.parametrize('klass', all_classes)
def test_repr_01(klass): 
    assert '__repr__' in dir(klass)
