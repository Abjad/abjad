# -*- encoding: utf-8 -*-

import inspect
import pickle
import pytest
from abjad.tools import documentationtools


pytest.skip()


@pytest.mark.parametrize('klass', documentationtools.list_all_abjad_classes())
def test_pickle_01(klass):
    if '_storage_format' in dir(klass) and not inspect.isabstract(klass):
        instance_one = klass()
        instance_two = pickle.loads(pickle.dumps(instance_one))
        assert instance_one == instance_two
