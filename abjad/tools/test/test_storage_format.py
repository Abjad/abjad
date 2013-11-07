# -*- encoding: utf-8 -*-
import inspect
import pickle
import pytest
from abjad.tools import documentationtools
pytest.skip()


@pytest.mark.parametrize('klass', documentationtools.list_all_abjad_classes())
def test_storage_format_01(klass):
    r'''All class with storage format have evaluable storage format.
    '''

    if '_storage_format' in dir(klass) and not inspect.isabstract(klass):
        instance_one = klass()
        instance_two = eval(format(instance_one, 'storage'))
        assert instance_one == instance_two
