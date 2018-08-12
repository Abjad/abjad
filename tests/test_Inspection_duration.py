import abjad
import pytest


def test_Inspection_duration_01():
    """
    Spanner duration in seconds equals sum of duration of all leaves in
    spanner, in seconds.
    """

    voice = abjad.Voice([
        abjad.Measure((2, 12), "c'8 d'8", implicit_scaling=True),
        abjad.Measure((2, 8), "c'8 d'8")]
        )
    leaves = abjad.select(voice).leaves()
    mark = abjad.MetronomeMark(abjad.Duration(1, 8), 42)
    abjad.attach(mark, leaves[0], context='Voice')
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, voice[0][:])
    decrescendo = abjad.Hairpin('>')
    abjad.attach(decrescendo, voice[1][:])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                #(ly:expect-warning "strange time signature found")
                \time 2/12
                \scaleDurations #'(2 . 3) {
                    \tempo 8=42
                    c'8
                    [
                    \<
                    d'8
                    \!
                }
            }   % measure
            {   % measure
                \time 2/8
                c'8
                \>
                d'8
                ]
                \!
            }   % measure
        }
        """
        )

    assert abjad.inspect(beam).duration(in_seconds=True) == abjad.Duration(100, 21)
    assert abjad.inspect(crescendo).duration(in_seconds=True) == abjad.Duration(40, 21)
    assert abjad.inspect(decrescendo).duration(in_seconds=True) == \
        abjad.Duration(20, 7)


def test_Inspection_duration_02():

    voice = abjad.Voice(
        [abjad.Measure((2, 12), "c'8 d'8", implicit_scaling=True),
        abjad.Measure((2, 8), "c'8 d'8")]
        )
    leaves = abjad.select(voice).leaves()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)
    crescendo = abjad.Hairpin('<')
    abjad.attach(crescendo, voice[0][:])
    decrescendo = abjad.Hairpin('>')
    abjad.attach(decrescendo, voice[1][:])

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            {   % measure
                #(ly:expect-warning "strange time signature found")
                \time 2/12
                \scaleDurations #'(2 . 3) {
                    c'8
                    [
                    \<
                    d'8
                    \!
                }
            }   % measure
            {   % measure
                \time 2/8
                c'8
                \>
                d'8
                ]
                \!
            }   % measure
        }
        """
        )

    assert abjad.inspect(beam).duration() == abjad.Duration(5, 12)
    assert abjad.inspect(crescendo).duration() == abjad.Duration(2, 12)
    assert abjad.inspect(decrescendo).duration() == abjad.Duration(2, 8)


def test_Inspection_duration_03():
    """
    Container duration in seconds equals sum of leaf durations in seconds.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 38)
    abjad.attach(mark, staff[0])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 42)
    abjad.attach(mark, staff[2])
    score = abjad.Score([staff])

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                \tempo 4=38
                c'8
                d'8
                \tempo 4=42
                e'8
                f'8
            }
        >>
        """
        )

    assert abjad.inspect(score).duration(in_seconds=True) == abjad.Duration(400, 133)


def test_Inspection_duration_04():
    """
    Container can not calculate duration in seconds without metronome mark.
    """

    container = abjad.Container("c'8 d'8 e'8 f'8")
    statement = 'inspect(container).duration(in_seconds=True)'
    assert pytest.raises(Exception, statement)


def test_Inspection_duration_05():
    """
    Clock duration equals duration divide by effective tempo.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 38)
    abjad.attach(mark, staff[0])
    mark = abjad.MetronomeMark(abjad.Duration(1, 4), 42)
    abjad.attach(mark, staff[2])
    abjad.Score([staff])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            \tempo 4=38
            c'8
            d'8
            \tempo 4=42
            e'8
            f'8
        }
        """
        )

    assert abjad.inspect(staff[0]).duration(in_seconds=True) == abjad.Duration(15, 19)
    assert abjad.inspect(staff[1]).duration(in_seconds=True) == abjad.Duration(15, 19)
    assert abjad.inspect(staff[2]).duration(in_seconds=True) == abjad.Duration(5, 7)
    assert abjad.inspect(staff[3]).duration(in_seconds=True) == abjad.Duration(5, 7)


def test_Inspection_duration_06():
    """
    Clock duration can not calculate without metronome mark.
    """

    note = abjad.Note("c'4")
    statement = 'inspect(note).duration(in_seconds=True)'
    assert pytest.raises(Exception, statement)
