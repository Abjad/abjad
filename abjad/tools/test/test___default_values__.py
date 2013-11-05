import inspect
import pytest
from abjad.tools import documentationtools


pytest.skip()


@pytest.mark.parametrize('klass', documentationtools.list_all_abjad_classes())
def test___default_values___01(klass):
    if '_storage_format' in dir(klass) and not inspect.isabstract(klass):
        instance = klass()
