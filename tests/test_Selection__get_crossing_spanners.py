import abjad
import pytest


def test_Selection__get_crossing_spanners_01():
    """
    Returns unordered set of spanners crossing
    over the begin- or end-bounds of logical-voice-contiguous
    components.
    """

    voice = abjad.Voice("{ c'8 d'8 } { e'8 f'8 }")
    leaves = abjad.select(voice).leaves()
    slur = abjad.Slur()
    abjad.attach(slur, voice[1][:])
    trill = abjad.TrillSpanner()
    abjad.attach(trill, leaves)

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {
                c'8
                \startTrillSpan
                d'8
            }
            {
                e'8
                (
                f'8
                )
                \stopTrillSpan
            }
        }
        """
        )

    spanners = abjad.select(voice)._get_crossing_spanners()
    assert spanners == []

    spanners = abjad.select(leaves)._get_crossing_spanners()
    assert spanners == []

    spanners = voice[:1]._get_crossing_spanners()
    assert len(spanners) == 1
    assert trill in spanners

    spanners = abjad.select(leaves[:-1])._get_crossing_spanners()
    assert len(spanners) == 2
    assert slur in spanners
    assert trill in spanners


def test_Selection__get_crossing_spanners_02():
    """
    Helper gets spanners that cross in from above.
    """

    staff = abjad.Staff("abj: | 2/8 c'8 d'8 || 2/8 e'8 f'8 || 2/8 g'8 a'8 |")
    leaves = abjad.select(staff).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves[2:5])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                e'8
                [
                f'8
            }
            {
                \time 2/8
                g'8
                ]
                a'8
            }
        }
        """
        ), print(format(staff))

    spanners = abjad.select(leaves)._get_crossing_spanners()

    assert len(spanners) == 0
