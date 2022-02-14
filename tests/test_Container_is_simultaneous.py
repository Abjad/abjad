import pytest

import abjad


def test_Container_is_simultaneous_01():
    """
    Is true when container encloses contents in LilyPond << >> brackets,
    otherwise False.
    """

    assert not abjad.Container().simultaneous
    assert not abjad.Tuplet().simultaneous
    assert abjad.Score().simultaneous
    assert not abjad.Container().simultaneous
    assert not abjad.Staff().simultaneous
    assert abjad.StaffGroup().simultaneous
    assert not abjad.Voice().simultaneous


def test_Container_is_simultaneous_02():
    """
    Is true when container encloses contents in LilyPond << >> brackets,
    otherwise False.
    """

    container = abjad.Container([])
    container.simultaneous = True
    assert container.simultaneous


def test_Container_is_simultaneous_03():
    """
    Container 'simultaneous' is settable.
    """

    container = abjad.Container([])
    assert not container.simultaneous

    container.simultaneous = True
    assert container.simultaneous


def test_Container_is_simultaneous_04():
    """
    A simultaneous container can hold Contexts.
    """

    container = abjad.Container([abjad.Voice("c'8 cs'8"), abjad.Voice("d'8 ef'8")])
    container.simultaneous = True

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        <<
            \new Voice
            {
                c'8
                cs'8
            }
            \new Voice
            {
                d'8
                ef'8
            }
        >>
        """
    )


def test_Container_is_simultaneous_05():
    """
    Simultaneous containers must contain only other containers.
    """

    # allowed
    container = abjad.Container(
        [abjad.Container("c'8 c'8 c'8 c'8"), abjad.Container("c'8 c'8 c'8 c'8")]
    )

    # not allowed
    container = abjad.Container("c'8 c'8 c'8 c'8")
    with pytest.raises(Exception):
        container.simultaneous = True
