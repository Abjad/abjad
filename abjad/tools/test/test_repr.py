from abjad import *
import pytest


@pytest.mark.parametrize('klass', documentationtools.list_all_abjad_classes())
def test_repr_01(klass): 
    assert '__repr__' in dir(klass)
