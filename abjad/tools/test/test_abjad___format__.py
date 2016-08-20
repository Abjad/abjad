# -*- coding: utf-8 -*-
import importlib
import inspect
import pytest
import abjad
from abjad.tools import abjadbooktools
from abjad.tools import documentationtools
from abjad.tools import metertools
from abjad.tools import systemtools
from abjad.tools import tonalanalysistools


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
def test_abjad___format___01(class_):
    r'''All concrete classes have a storage format.
    '''
    if (
        '_storage_format_specification' not in dir(class_) or
        '_get_format_specification' not in dir(class_)
        ):
        return
    if inspect.isabstract(class_):
        return
    instance = class_()
    instance_format = format(instance, 'storage')
    assert isinstance(instance_format, str)
    assert not instance_format == ''


ignored_classes = (
    abjadbooktools.CodeBlock,
    abjadbooktools.CodeOutputProxy,
    abjadbooktools.GraphvizOutputProxy,
    abjadbooktools.LilyPondOutputProxy,
    metertools.Meter,
    tonalanalysistools.RootedChordClass,
    systemtools.StorageFormatAgent,
    systemtools.FormatSpecification,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___format___02(class_):
    r'''All storage-formattable classes have evaluable storage format.
    '''
    if '_storage_format_specification' not in dir(class_):
        return
    if inspect.isabstract(class_):
        return
    environment = abjad.__dict__.copy()
    environment.update(abjad.demos.__dict__)
    environment['abjadbooktools'] = importlib.import_module(
        'abjad.tools.abjadbooktools')
    environment['abjad'] = abjad
    instance_one = class_()
    instance_one_format = format(instance_one, 'storage')
    assert isinstance(instance_one_format, str)
    assert instance_one_format != ''
    instance_two = eval(instance_one_format, environment)
    instance_two_format = format(instance_two, 'storage')
    assert instance_one_format == instance_two_format
