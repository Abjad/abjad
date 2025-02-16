import copy
import inspect
import pickle

import pytest

import abjad

classes = abjad.list_all_classes()


class_to_default_values = {
    abjad.io.AbjadGrapher: (abjad.Note("c'4"),),
    abjad.io.Illustrator: (abjad.Note("c'4"),),
    abjad.io.LilyPondIO: (abjad.Note("c'4"),),
    abjad.io.Player: (abjad.Note("c'4"),),
    abjad.parsers.parser.MarkupCommand: (r"\hcenter-in",),
    abjad.Articulation: ("staccato",),
    abjad.Bundle: (abjad.Articulation("."),),
    abjad.ColorFingering: (0,),
    abjad.InstrumentName: ("Piano",),
    abjad.Markup: (r"\markup Allegro",),
    abjad.Meter: (abjad.meter.make_best_guess_rtc((4, 4)),),
    abjad.MetricModulation: (abjad.Note("c'4"), abjad.Note("c'4.")),
    abjad.MetronomeMark: (abjad.Duration(1, 4), 90),
    abjad.TextMark: (r'\textMark \markup \italic "V.S."',),
    abjad.ShortInstrumentName: (r"\markup Vc.",),
    abjad.StaffChange: ("RH_Staff",),
    abjad.TimeSignature: ((4, 4),),
    abjad.Tweak: (r"\tweak color #red",),
}


@pytest.mark.parametrize("class_", classes)
def test_abjad___copy___(class_):
    """
    All concrete classes can copy.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if issubclass(class_, Exception):
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    instance_2 = copy.copy(instance_1)
    assert instance_2 is not None
    assert instance_1 == instance_2


@pytest.mark.parametrize("class_", classes)
def test_abjad___deepcopy___(class_):
    """
    All concrete classes can deepcopy.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if issubclass(class_, Exception):
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    instance_2 = copy.deepcopy(instance_1)
    assert instance_2 is not None
    assert instance_1 == instance_2


@pytest.mark.parametrize("class_", classes)
def test_abjad___hash___(class_):
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
def test_abjad___repr___(class_):
    """
    All concrete classes have a repr and a string.
    """
    _allowed_to_be_empty_string = (
        abjad.Accidental,
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
def test_abjad___rmul___(class_):
    """
    All classes with __mul__ also implement __rmul__.
    """
    if inspect.isabstract(class_):
        return
    if hasattr(class_, "__mul__"):
        assert hasattr(class_, "__rmul__")


@pytest.mark.parametrize("class_", classes)
def test_abjad___slots___(class_):
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


@pytest.mark.parametrize("class_", classes)
def test_abjad_contexted_persistence(class_):
    """
    All classes with "persistent" property also have "context" property.
    """
    if inspect.isabstract(class_):
        return
    if hasattr(class_, "persistent"):
        assert hasattr(class_, "context")


@pytest.mark.parametrize("class_", classes)
def test_abjad_format_site_defaults(class_):
    """
    All classes with "site" property default to "before" or "after".
    """
    if inspect.isabstract(class_):
        return
    if hasattr(class_, "site"):
        default_values = class_to_default_values.get(class_, ())
        instance = class_(*default_values)
        assert instance.site in ("before", "after"), repr(class_.site)


@pytest.mark.parametrize("class_", classes)
def test_abjad_pickle(class_):
    """
    All concrete classes are pickable.
    """
    if inspect.isabstract(class_):
        return
    if getattr(class_, "_is_abstract", None) is True:
        return
    if issubclass(class_, Exception):
        return
    default_values = class_to_default_values.get(class_, ())
    instance_1 = class_(*default_values)
    pickle_string = pickle.dumps(instance_1)
    instance_2 = pickle.loads(pickle_string)
    assert instance_1 == instance_2
