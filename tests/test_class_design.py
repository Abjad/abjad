import copy
import inspect
import pickle

import pytest
from default_values import class_to_default_values

import abjad

classes = abjad.list_all_classes()


@pytest.mark.parametrize("class_", classes)
def test_abjad___copy___01(class_):
    """
    All concrete classes can copy.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    instance_2 = copy.copy(instance_1)
    assert instance_2 is not None
    # TODO: eventually this should pass:
    # assert instance_1 == instance_2


@pytest.mark.parametrize("class_", classes)
def test_abjad___deepcopy___01(class_):
    """
    All concrete classes can deepcopy.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    instance_2 = copy.deepcopy(instance_1)
    assert instance_2 is not None
    # TODO: eventually this should pass:
    # assert instance_1 == instance_2


@pytest.mark.parametrize("class_", classes)
def test_abjad___hash___01(class_):
    """
    All concrete classes with __hash__ can hash.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if getattr(class_, "__hash__", None) is None:
        return
    default_values = class_to_default_values.get(class_, ())
    instance = class_(*default_values)
    value = hash(instance)
    assert isinstance(value, int)


@pytest.mark.parametrize("class_", classes)
def test_abjad___radd___01(class_):
    """
    Classes with __add__ also implement __radd__.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if issubclass(class_, str):
        return
    if hasattr(class_, "__add__"):
        assert hasattr(class_, "__radd__")


@pytest.mark.parametrize("class_", classes)
def test_abjad___repr___01(class_):
    """
    All concrete classes have a repr and a string.
    """
    _allowed_to_be_empty_string = (
        abjad.Accidental,
        abjad.Line,
        abjad.Tag,
    )
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    default_values = class_to_default_values.get(class_, ())
    instance = class_(*default_values)
    string = repr(instance)
    assert string is not None
    assert string != ""
    if issubclass(class_, Exception):
        return
    string = str(instance)
    assert string is not None
    if class_ not in _allowed_to_be_empty_string:
        assert string != ""


@pytest.mark.parametrize("class_", classes)
def test_abjad___rmul___01(class_):
    """
    All classes with __mul__ also implement __rmul__.
    """
    if inspect.isabstract(class_):
        return
    if hasattr(class_, "__mul__"):
        assert hasattr(class_, "__rmul__")


@pytest.mark.parametrize("class_", classes)
def test_abjad___slots___01(class_):
    """
    All classes with __slots__ implement __slots__ correctly.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    attrs = inspect.classify_class_attrs(class_)
    attrs = dict((attr.name, attr) for attr in attrs)
    if "__slots__" not in attrs:
        return
    elif attrs["__slots__"].defining_class is not class_:
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    assert not hasattr(instance_1, "__dict__")


ignored_classes = (
    abjad.io.AbjadGrapher,
    abjad.io.Illustrator,
    abjad.io.Player,
    abjad.io.LilyPondIO,
    abjad.Configuration,
    abjad.Descendants,
    abjad.LeafMaker,
    abjad.LilyPondFormatBundle,
    abjad.LilyPondOverride,
    abjad.LilyPondSetting,
    abjad.Lineage,
    abjad.Meter,  # TODO: should abjad.Meter pickle?
    abjad.NoteMaker,
    abjad.SlotContributions,
)
classes = abjad.list_all_classes(ignored_classes=ignored_classes)


@pytest.mark.parametrize("class_", classes)
def test_abjad_pickle_01(class_):
    """
    All concrete classes are pickable.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if "parser" in repr(class_):
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    pickle_string = pickle.dumps(instance_1)
    instance_2 = pickle.loads(pickle_string)
    repr_1 = repr(instance_1)
    repr_2 = repr(instance_2)
    assert repr_1 == repr_2
