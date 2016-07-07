# -*- coding: utf-8 -*-
from abjad import *


def test_quantizationtools_QEventSequence_from_tempo_scaled_leaves_01():

    staff = Staff([])

    staff.append(Note(0, (1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Rest((1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(3, (1, 8)))
    staff.append(scoretools.Skip((1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Note(3, (1, 8)))
    staff.append(Chord([0, 1, 4], (1, 4)))

    tie = spannertools.Tie()
    attach(tie, staff[3:5])
    tie = spannertools.Tie()
    attach(tie, staff[5:7])

    tempo = Tempo((1, 4), 55)

    leaves = select(staff).by_leaf()
    q_events = quantizationtools.QEventSequence.from_tempo_scaled_leaves(
        leaves, tempo)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(12000, 11)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(30000, 11),
            (NamedPitch("cs'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(42000, 11),
            (NamedPitch("d'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(54000, 11),
            (NamedPitch("ef'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(60000, 11)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(84000, 11),
            (NamedPitch("ef'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(90000, 11),
            (
                NamedPitch("c'"),
                NamedPitch("cs'"),
                NamedPitch("e'"),
            )
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(102000, 11)
            )
    ))


def test_quantizationtools_QEventSequence_from_tempo_scaled_leaves_02():

    staff = Staff([])

    staff.append(Note(0, (1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Rest((1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(1, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(2, (1, 8)))
    staff.append(Note(3, (1, 8)))
    staff.append(scoretools.Skip((1, 4)))
    staff.append(Rest((1, 4)))
    staff.append(Note(3, (1, 8)))
    staff.append(Chord([0, 1, 4], (1, 4)))

    tie = spannertools.Tie()
    attach(tie, staff[3:5])
    tie = spannertools.Tie()
    attach(tie, staff[5:7])

    tempo = Tempo((1, 4), 58)
    attach(tempo, staff[0], scope=Staff)
    tempo = Tempo((1, 4), 77)
    attach(tempo, staff[9], scope=Staff)

    leaves = select(staff).by_leaf()
    q_events = quantizationtools.QEventSequence.from_tempo_scaled_leaves(
        leaves)

    assert q_events == quantizationtools.QEventSequence((
        quantizationtools.PitchedQEvent(
            durationtools.Offset(0, 1),
            (NamedPitch("c'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(30000, 29)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(75000, 29),
            (NamedPitch("cs'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(105000, 29),
            (NamedPitch("d'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(135000, 29),
            (NamedPitch("ef'"),)
            ),
        quantizationtools.SilentQEvent(
            durationtools.Offset(150000, 29)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(15600000, 2233),
            (NamedPitch("ef'"),)
            ),
        quantizationtools.PitchedQEvent(
            durationtools.Offset(16470000, 2233),
            (
                NamedPitch("c'"),
                NamedPitch("cs'"),
                NamedPitch("e'"),
            )
            ),
        quantizationtools.TerminalQEvent(
            durationtools.Offset(18210000, 2233)
            )
    ))
