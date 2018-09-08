import abjad
import inspect
import pytest


ignored_classes = (
    abjad.Path,
    abjad.StorageFormatManager,
    abjad.FormatSpecification,
    )

classes = pytest.helpers.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___format___01(class_):
    """
    All concrete classes have a storage format.
    """
    if (
        '_get_storage_format_specification' not in dir(class_) or
        '_get_format_specification' not in dir(class_)
    ):
        return
    if inspect.isabstract(class_):
        return
    if getattr(class_, '_is_abstract', None) is True:
        return
    instance = class_()
    instance_format = format(instance, 'storage')
    assert isinstance(instance_format, str)
    assert not instance_format == ''


ignored_classes = (
    abjad.Path,
    abjad.Meter,
    abjad.StorageFormatManager,
    abjad.FormatSpecification,
    )

classes = pytest.helpers.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___format___02(class_):
    """
    All storage-formattable classes have evaluable storage format.
    """
    if '_get_storage_format_specification' not in dir(class_):
        return
    if inspect.isabstract(class_):
        return
    if getattr(class_, '_is_abstract', None) is True:
        return
    environment = abjad.__dict__.copy()
    environment.update(abjad.demos.__dict__)
    environment['abjad'] = abjad
    instance_one = class_()
    instance_one_format = format(instance_one, 'storage')
    assert isinstance(instance_one_format, str)
    assert instance_one_format != ''
    instance_two = eval(instance_one_format, environment)
    instance_two_format = format(instance_two, 'storage')
    assert instance_one_format == instance_two_format


ignored_classes = (
    #abjad.Parser,
    abjad.Path,
    abjad.Tags,
    abjad.parser.SyntaxNode,
    )

classes = pytest.helpers.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('class_', classes)
def test_abjad___format___03(class_):
    """
    All concrete classes bald-format.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, '_is_abstract', None) is True:
        return
    object_ = class_()
    string = f'{object_}'
    print(string)
