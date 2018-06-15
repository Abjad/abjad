import abjad
import pytest
from abjad import utilities


pytest_plugins = ['helpers_namespace']


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace['abjad'] = abjad
    doctest_namespace['f'] = abjad.f
    doctest_namespace['Infinity'] = abjad.mathtools.Infinity()
    doctest_namespace['NegativeInfinity'] = abjad.mathtools.NegativeInfinity()


@pytest.helpers.register
def list_all_abjad_classes(modules=None, ignored_classes=None):
    return utilities.list_all_classes(
        modules='abjad',
        ignored_classes=ignored_classes,
        )


@pytest.helpers.register
def list_all_abjad_functions(modules=None):
    return utilities.list_all_functions(modules='abjad')
