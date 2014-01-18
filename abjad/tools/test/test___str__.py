# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools
#pytest.skip('working on these now.')


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('class_', classes)
def test___repr___01(class_):
    r'''All concrete classes have a string representation.

    (But note that exceptions do not have a string representation.)
    '''

    if not inspect.isabstract(class_):
        if not issubclass(class_, Exception):
            instance = class_()
            string = str(instance)
            assert string is not None
            #assert string != ''
