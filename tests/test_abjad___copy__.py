import abjad
import copy
import inspect
import pytest


ignored_classes = (abjad.StorageFormatManager, abjad.FormatSpecification)

classes = pytest.helpers.list_all_abjad_classes(
    ignored_classes=ignored_classes
)


@pytest.mark.parametrize("class_", classes)
def test_abjad___copy___01(class_):
    """
    All concrete classes with a storage format can copy.
    """
    if "_get_storage_format_specification" not in dir(
        class_
    ) or "_get_format_specification" not in dir(class_):
        return
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    instance_one = class_()
    instance_two = copy.copy(instance_one)
    instance_one_format = format(instance_one, "storage")
    instance_two_format = format(instance_two, "storage")
    if not issubclass(class_, abjad.Container):
        assert instance_one_format == instance_two_format
    # TODO: eventually this second asset should also pass
    # assert instance_one == instance_two
