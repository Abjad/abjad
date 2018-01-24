import abjad
import inspect
import pytest
import types
from abjad.tools import documentationtools


ignored_classes = (
    abjad.Duration,
    abjad.Enumeration,
    abjad.Multiplier,
    abjad.Offset,
    abjad.Path,
    abjad.Tags,
    )

ignored_package_names = (
    'abjadbooktools',
    'commandlinetools',
    'graphtools',
    'systemtools',
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )

# TODO: port inspect.getargspec() to getfullargspect() for annotations
#@pytest.mark.parametrize('class_', classes)
#def test_abjad_duration_01(class_):
#    r'''Every method with duration input must accept an (n, d) implicit pair.
#    '''
#    if inspect.isabstract(class_):
#        return
#    for ignored_package_name in ignored_package_names:
#        if ignored_package_name in class_.__module__:
#            return
#    object_ = class_()
#    for name in dir(object_):
#        try:
#            value = getattr(object_, name)
#        except:
#            continue
#        if not isinstance(value, types.MethodType):
#            continue
#        method = value
#        argument_specification = inspect.getargspec(method)
#        for argument_name in argument_specification.args:
#            if argument_name != 'duration':
#                continue
#            # if it works to pass in an explicit duration ...
#            try:
#                method(duration=abjad.Duration(1, 4))
#            except:
#                continue
#            # it should work to pass in a pair ...
#            method(duration=(1, 4))
