import abjad
import pytest


def test_Container___getitem___01():
    """
    Get one container component with positive index.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    voice = abjad.Voice(notes)

    assert voice[0] is notes[0]
    assert voice[1] is notes[1]
    assert voice[2] is notes[2]
    assert voice[3] is notes[3]


def test_Container___getitem___02():
    """
    Get one container component with negative index.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    voice = abjad.Voice(notes)

    assert voice[-1] is notes[3]
    assert voice[-2] is notes[2]
    assert voice[-3] is notes[1]
    assert voice[-4] is notes[0]


def test_Container___getitem___03():
    """
    Get slice from container.
    """

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"),
        abjad.Note("e'8"),
        abjad.Note("f'8"),
    ]
    voice = abjad.Voice(notes)

    assert voice[:1] == notes[:1]
    assert voice[:2] == notes[:2]
    assert voice[:3] == notes[:3]
    assert voice[:4] == notes[:4]


def test_Container___getitem___04():
    """
    Bad index raises IndexError.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    with pytest.raises(IndexError):
        voice[99]


def test_Container___getitem___05():
    """
    Get one named component in subtree rooted at container.
    """

    template = abjad.StringQuartetScoreTemplate()
    score = template()

    assert score["First_Violin_Staff"].name == "First_Violin_Staff"
    assert score["First_Violin_Voice"].name == "First_Violin_Voice"


def test_Container___getitem___06():
    """
    Bad name raises exception.
    """

    template = abjad.StringQuartetScoreTemplate()
    score = template()

    with pytest.raises(Exception):
        score["Foo"]


def test_Container___getitem___07():
    """
    Duplicate named contexts raise exception.
    """

    template = abjad.StringQuartetScoreTemplate()
    score = template()

    assert score["First_Violin_Voice"].name == "First_Violin_Voice"

    score["Cello_Staff"].append(abjad.Voice(name="First_Violin_Voice"))

    with pytest.raises(Exception):
        score["First_Violin_Voice"]

    extra_first_violin_voice = score["Cello_Staff"].pop()

    assert score["First_Violin_Voice"].name == "First_Violin_Voice"
    assert score["First_Violin_Voice"] is not extra_first_violin_voice
