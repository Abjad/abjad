import abjad
import pytest


def test_scoretools_Container_is_simultaneous_01():
    """
    Is true when container encloses contents in LilyPond << >> brackets,
    otherwise False.
    """

    assert not abjad.Container().is_simultaneous
    assert not abjad.Tuplet().is_simultaneous
    assert not abjad.Measure().is_simultaneous
    assert abjad.Score().is_simultaneous
    assert not abjad.Container().is_simultaneous
    assert not abjad.Staff().is_simultaneous
    assert abjad.StaffGroup().is_simultaneous
    assert not abjad.Voice().is_simultaneous


def test_scoretools_Container_is_simultaneous_02():
    """
    Is true when container encloses contents in LilyPond << >> brackets,
    otherwise False.
    """

    container = abjad.Container([])
    container.is_simultaneous = True
    assert container.is_simultaneous


def test_scoretools_Container_is_simultaneous_03():
    """
    Container 'simultaneous' is settable.
    """

    container = abjad.Container([])
    assert not container.is_simultaneous

    container.is_simultaneous = True
    assert container.is_simultaneous


def test_scoretools_Container_is_simultaneous_04():
    """
    A simultaneous container can hold Contexts.
    """

    container = abjad.Container([abjad.Voice("c'8 cs'8"), abjad.Voice("d'8 ef'8")])
    container.is_simultaneous = True

    assert format(container) == abjad.String.normalize(
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


def test_scoretools_Container_is_simultaneous_05():
    """
    Simultaneous containers must contain only other containers.
    """

    # allowed
    container = abjad.Container(2 * abjad.Container("c'8 c'8 c'8 c'8"))

    # not allowed
    container = abjad.Container("c'8 c'8 c'8 c'8")
    pytest.raises(Exception, 'container.is_simultaneous = True')
