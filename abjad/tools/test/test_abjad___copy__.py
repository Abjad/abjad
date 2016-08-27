# -*- coding: utf-8 -*-
import copy
import inspect
import pytest
from abjad.tools import abjadbooktools
from abjad.tools import documentationtools
from abjad.tools import scoretools
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
def test_abjad___copy___01(class_):
    r'''All concrete classes with a storage format can copy.
    '''
    if (
        '_storage_format_specification' not in dir(class_) or
        '_get_format_specification' not in dir(class_)
        ): 
        return
    if inspect.isabstract(class_):
        return
    instance_one = class_()
    instance_two = copy.copy(instance_one)
    instance_one_format = format(instance_one, 'storage')
    instance_two_format = format(instance_two, 'storage')
    if not issubclass(class_, scoretools.Container):
        assert instance_one_format == instance_two_format
    # TODO: eventually this second asset should also pass
    #assert instance_one == instance_two
