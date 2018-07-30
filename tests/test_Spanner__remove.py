import abjad
import pytest


def test_Spanner__remove_01():
    """
    Remove interior component from spanner.
    Remove spanner from component's aggregator.
    Spanner is left discontiguous and score no longer checks.
    Not composer-safe.
    Follow immediately with operation to remove component from score.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
        )

    beam._remove(beam[1])
    assert not abjad.inspect(voice).is_wellformed()


def test_Spanner__remove_02():
    """
    Remove last component from spanner.
    Remove spanner from component's aggregator.
    Here an end element removes from spanner.
    So spanner is not left discontiguous and score checks.
    Still not composer-safe.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 } { g'8 a'8 }")
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
            }
            {
                g'8
                a'8
                ]
            }
        }
        """
        )

    result = beam._remove(beam[-1])
    result = beam._remove(beam[-1])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                [
                d'8
            }
            {
                e'8
                f'8
                ]
            }
            {
                g'8
                a'8
            }
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_Spanner__remove_03():
    """
    Remove works only on references and not on equality.
    """

    note = abjad.Note("c'4")
    spanner = abjad.Spanner()
    abjad.attach(spanner, abjad.select(abjad.Note("c'4")))

    assert pytest.raises(Exception, 'spanner._remove(note)')
