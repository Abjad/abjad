import pytest

import abjad


def test_dynamic_01():
    """
    Duplicate dynamics raise exception on attach.
    """

    voice = abjad.Voice("c'4")
    dynamic_1 = abjad.Dynamic("p")
    abjad.attach(dynamic_1, voice[0])
    dynamic_2 = abjad.Dynamic("p")
    with pytest.raises(Exception) as exception:
        abjad.attach(dynamic_2, voice[0])
    assert "attempting to attach conflicting indicator" in str(exception)
