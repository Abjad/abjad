from abjad import *
from experimental import quantizationtools


def test_quantizationtools_tempo_scaled_leaves_to_q_events_01():

    staff = Staff([])

    staff.append(Note(0, (1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Rest((1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(3, (1, 8)))
    staff.append(skiptools.Skip((1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Note(3, (1, 8)))
    staff.append(Chord([0, 1, 4], (1, 4)))

    tietools.TieSpanner(staff[3:5])
    tietools.TieSpanner(staff[5:7])
    tietools.TieSpanner(staff[7:11])

    tempo = contexttools.TempoMark((1, 4), 55)

    q_events = quantizationtools.tempo_scaled_leaves_to_q_events(staff.leaves, tempo)

    assert q_events == [
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (pitchtools.NamedChromaticPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(12000, 11)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(30000, 11),
            (pitchtools.NamedChromaticPitch("cs'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(42000, 11),
            (pitchtools.NamedChromaticPitch("d'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(54000, 11),
            (pitchtools.NamedChromaticPitch("ef'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(60000, 11)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(84000, 11),
            (pitchtools.NamedChromaticPitch("ef'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(90000, 11),
            (
                pitchtools.NamedChromaticPitch("c'"),
                pitchtools.NamedChromaticPitch("cs'"),
                pitchtools.NamedChromaticPitch("e'"),
            )
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(102000, 11)
            )
    ]


def test_quantizationtools_tempo_scaled_leaves_to_q_events_02():

    staff = Staff([])

    staff.append(Note(0, (1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Rest((1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(3, (1, 8)))
    staff.append(skiptools.Skip((1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Note(3, (1, 8)))
    staff.append(Chord([0, 1, 4], (1, 4)))

    tietools.TieSpanner(staff[3:5])
    tietools.TieSpanner(staff[5:7])
    tietools.TieSpanner(staff[7:11])

    contexttools.TempoMark((1, 4), 58, target_context=Staff)(staff[0])
    contexttools.TempoMark((1, 4), 77, target_context=Staff)(staff[9])

    q_events = quantizationtools.tempo_scaled_leaves_to_q_events(staff.leaves)

    assert q_events == [
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (pitchtools.NamedChromaticPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(30000, 29)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(75000, 29),
            (pitchtools.NamedChromaticPitch("cs'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(105000, 29),
            (pitchtools.NamedChromaticPitch("d'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(135000, 29),
            (pitchtools.NamedChromaticPitch("ef'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(150000, 29)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(15600000, 2233),
            (pitchtools.NamedChromaticPitch("ef'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(16470000, 2233),
            (
                pitchtools.NamedChromaticPitch("c'"),
                pitchtools.NamedChromaticPitch("cs'"),
                pitchtools.NamedChromaticPitch("e'"),
            )
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(18210000, 2233)
            )
    ]
