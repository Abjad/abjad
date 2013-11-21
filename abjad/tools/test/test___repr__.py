# -*- encoding: utf-8 -*-
import pytest
from abjad.tools import documentationtools


@pytest.mark.parametrize('klass', documentationtools.list_all_abjad_classes())
def test___repr___01(klass):
    assert '__repr__' in dir(klass)
