import inspect
import pytest

from abjad import abjad_configuration
from abjad.tools import documentationtools


class_crawler = documentationtools.ClassCrawler(
    abjad_configuration.abjad_directory_path,
    root_package_name='abjad',
    )
all_classes = class_crawler()

function_crawler = documentationtools.FunctionCrawler(
    abjad_configuration.abjad_directory_path,
    root_package_name='abjad',
    )
all_functions = function_crawler()

ignored_names = (
    '__init__',
    '__weakref__',
    )

pytest.skip()

@pytest.mark.parametrize('klass', all_classes)
def test_docstrings_01(klass):
    assert klass.__doc__ is not None
    for attr in inspect.classify_class_attrs(klass):
        if attr.name in ignored_names:
            continue
        elif attr.defining_class is not klass:
            continue
        if attr.name[0].isalpha() or attr.name.startswith('__'):
            assert getattr(klass, attr.name).__doc__ is not None


@pytest.mark.parametrize('obj', all_functions)
def test_docstrings_02(obj):
    assert obj.__doc__ is not None
