# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_agenttools_InspectionAgent_get_timespan_01():

    voice = Voice("c'8 d'8 e'8 f'8")
    for i, x in enumerate(voice):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_02():

    staff = Staff("c'8 d'8 e'8 f'8")
    for i, x in enumerate(staff):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_03():

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[-1] = Rest((1, 8))
    for i, x in enumerate(staff):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_04():

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[10:10] = [Rest((1, 8))]
    for i, x in enumerate(staff):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_05():

    staff = Staff("c'8 d'8 e'8 f'8")
    staff[10:12] = [Rest((1, 8))]
    for i, x in enumerate(staff):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_06():
    r'''Offset works with voices.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    voice_1.name = voice_2.name = 'voice'
    container = Container([voice_1, voice_2])
    leaves = select(container).by_leaf()
    for i, x in enumerate(leaves):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_07():

    tuplet = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    for i, x in enumerate(tuplet):
        assert inspect_(x).get_timespan().start_offset == i * Offset(1, 12)


def test_agenttools_InspectionAgent_get_timespan_08():

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    voice = Voice([Note(0, (1, 8)), tuplet_1, Note(0, (1, 8))])
    offset = 0
    durations = [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]
    leaves = select(voice).by_leaf()
    for leaf, duration in zip(leaves, durations):
        assert inspect_(leaf).get_timespan().start_offset == offset
        offset += Offset(*duration)


def test_agenttools_InspectionAgent_get_timespan_09():
    r'''Offset works on nested tuplets.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    tuplet = scoretools.FixedDurationTuplet(
        Duration(2, 4), [Note("c'4"), tuplet_1, Note("c'4")])
    offset = 0
    durations = [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]
    leaves = select(tuplet).by_leaf()
    for leaf, duration in zip(leaves, durations):
        assert inspect_(leaf).get_timespan().start_offset == offset
        offset += Offset(*duration)


def test_agenttools_InspectionAgent_get_timespan_10():
    r'''Offset works with simultaneous structures.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    for i, leaf in enumerate(voice_1):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_11():
    r'''Offset on leaves works in nested contexts.
    '''

    voice = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([Note(0, (1, 8)), voice, Note(0, (1, 8))])
    leaves = select(staff).by_leaf()
    for i, leaf in enumerate(leaves):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8)
    leaves = select(voice).by_leaf()
    for i, leaf in enumerate(leaves):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8) + Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_12():
    r'''Offset on leaves works in sequential contexts.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([voice_1, voice_2])
    for i, leaf in enumerate(voice_1):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8) + Offset(1, 2)


def test_agenttools_InspectionAgent_get_timespan_13():
    r'''Offset on leaves works in nested simultaneous contexts.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    for i, leaf in enumerate(voice_1):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_14():
    r'''Offset on leaves works in nested simultaneous and sequential contexts.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    voice_3 = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([Container([voice_1, voice_2]), voice_3])
    staff[0].is_simultaneous = True
    for i, leaf in enumerate(voice_3):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8) + Offset(1, 2)


def test_agenttools_InspectionAgent_get_timespan_15():
    r'''Offset on leaves works in nested simultaneous and sequential contexts.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    voice_3 = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([voice_3, Container([voice_1, voice_2])])
    staff[1].is_simultaneous = True
    for i, leaf in enumerate(voice_1):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8) + Offset(1, 2)
    for i, leaf in enumerate(voice_2):
        start_offset = inspect_(leaf).get_timespan().start_offset
        assert start_offset == i * Offset(1, 8) + Offset(1, 2)


def test_agenttools_InspectionAgent_get_timespan_16():
    r'''Offsets works on sequential voices.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("c'8 d'8 e'8 f'8")])
    staff[0].name = staff[1].name = 'voice'
    for i, voice in enumerate(staff):
        start_offset = inspect_(voice).get_timespan().start_offset
        assert start_offset == i * Offset(4, 8)


def test_agenttools_InspectionAgent_get_timespan_17():
    r'''Prolated offset does NOT go across sequential staves.
    '''

    container = Container([Staff("c'8 d'8 e'8 f'8"), Staff("c'8 d'8 e'8 f'8")])
    container[0].name = container[1].name = 'staff'
    start_offset = inspect_(container[0]).get_timespan().start_offset
    assert start_offset == Offset(0)
    start_offset = inspect_(container[1]).get_timespan().start_offset
    assert start_offset == Offset(1, 2)


def test_agenttools_InspectionAgent_get_timespan_18():
    r'''Offsets works with nested voices.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("c'8 d'8 e'8 f'8")])
    for i, voice in enumerate(staff):
        start_offset = inspect_(voice).get_timespan().start_offset
        assert start_offset == i * Offset(4, 8)


def test_agenttools_InspectionAgent_get_timespan_19():
    r'''Offsets works on sequential tuplets.
    '''

    voice = Voice(3 * Tuplet(Multiplier(2, 3), "c'8 d'8 e'8"))
    assert inspect_(voice[0]).get_timespan().start_offset == 0 * Offset(1, 4)
    assert inspect_(voice[1]).get_timespan().start_offset == 1 * Offset(1, 4)
    assert inspect_(voice[2]).get_timespan().start_offset == 2 * Offset(1, 4)


def test_agenttools_InspectionAgent_get_timespan_20():
    r'''Offsets work on tuplets between notes.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    voice = Voice([Note(0, (1, 8)), tuplet_1, Note(0, (1, 8))])
    assert inspect_(voice[0]).get_timespan().start_offset == 0 * Offset(1, 8)
    assert inspect_(voice[1]).get_timespan().start_offset == 1 * Offset(1, 8)
    assert inspect_(voice[2]).get_timespan().start_offset == 3 * Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_21():
    r'''Offsets work on nested tuplets.
    '''

    tuplet_1 = scoretools.FixedDurationTuplet(Duration(1, 4), "c'8 d'8 e'8 f'8")
    contents = [Note("c'4"), tuplet_1, Note("c'4")]
    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), contents)
    assert inspect_(tuplet[0]).get_timespan().start_offset == 0 * Offset(1, 6)
    assert inspect_(tuplet[1]).get_timespan().start_offset == 1 * Offset(1, 6)
    assert inspect_(tuplet[2]).get_timespan().start_offset == 2 * Offset(1, 6)


def test_agenttools_InspectionAgent_get_timespan_22():
    r'''Offsets work on nested contexts.
    '''

    inner_voice = Voice("c'8 d'8 e'8 f'8")
    outer_voice = Voice([Note(0, (1, 8)), inner_voice])
    inner_voice.name = outer_voice.name = 'voice'
    staff = Staff([Note(1, (1, 8)), outer_voice])
    assert inspect_(inner_voice).get_timespan().start_offset == Offset(2, 8)
    assert inspect_(outer_voice).get_timespan().start_offset == Offset(1, 8)


def test_agenttools_InspectionAgent_get_timespan_23():
    r'''Offsets work on nested simultaneous contexts.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    assert inspect_(staff[0]).get_timespan().start_offset == 0
    assert inspect_(staff[1]).get_timespan().start_offset == 0


def test_agenttools_InspectionAgent_get_timespan_24():
    r'''Offsets works in nested simultaneous and sequential contexts.
    '''

    voice_1 = Voice("c'8 d'8 e'8 f'8")
    voice_2 = Voice("c'8 d'8 e'8 f'8")
    voice_1b = Voice("c'8 d'8 e'8 f'8")
    voice_2b = Voice("c'8 d'8 e'8 f'8")
    voice_1.name = voice_1b.name = 'voiceOne'
    staff_1 = Staff([voice_1, voice_1b])
    staff_2 = Staff([voice_2, voice_2b])
    gs = StaffGroup([staff_1, staff_2])
    assert inspect_(voice_1).get_timespan().start_offset == 0
    assert inspect_(voice_2).get_timespan().start_offset == 0
    assert inspect_(voice_1b).get_timespan().start_offset == Offset(4, 8)
    assert inspect_(voice_2b).get_timespan().start_offset == Offset(4, 8)


def test_agenttools_InspectionAgent_get_timespan_25():
    r'''Offset seconds can not calculate without excplit tempo indication.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    statement = 'inspect_(staff[0]).get_timespan(in_seconds=True).start_offset'
    assert pytest.raises(Exception, statement)


def test_agenttools_InspectionAgent_get_timespan_26():
    r'''Offset seconds work with explicit tempo indication.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = Tempo(Duration(1, 8), 48)
    attach(tempo, staff, scope=Staff)

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            \tempo 8=48
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )

    start_offset = inspect_(staff[0]).get_timespan(in_seconds=True).start_offset
    assert start_offset == Offset(0)
    start_offset = inspect_(staff[1]).get_timespan(in_seconds=True).start_offset
    assert start_offset == Offset(5, 4)
