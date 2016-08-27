# -*- coding: utf-8 -*-
import inspect
import pytest
from abjad.tools import abjadbooktools
from abjad.tools import documentationtools
from abjad.tools import systemtools


ignored_classes = (
    abjadbooktools.CodeBlock,
    abjadbooktools.CodeOutputProxy,
    abjadbooktools.GraphvizOutputProxy,
    abjadbooktools.LilyPondOutputProxy,
    systemtools.StorageFormatAgent,
    systemtools.FormatSpecification,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___slots___01(class_):
    r'''All concrete classes defining __slots__ do not have a dict.
    '''
    if inspect.isabstract(class_):
        return
    attrs = inspect.classify_class_attrs(class_)
    attrs = dict((attr.name, attr) for attr in attrs)
    if '__slots__' not in attrs:
        return
    elif attrs['__slots__'].defining_class is not class_:
        return
    instance_one = class_()
    assert not hasattr(instance_one, '__dict__')
