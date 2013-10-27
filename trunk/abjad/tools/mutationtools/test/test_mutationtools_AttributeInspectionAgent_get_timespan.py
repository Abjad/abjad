# -*- encoding: utf-8 -*-
import py
from abjad import *


def test_mutationtools_AttributeInspectionAgent_get_timespan_01():

    voice = Voice(notetools.make_repeated_notes(16))
    for i, x in enumerate(voice):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_02():

    staff = Staff(notetools.make_repeated_notes(16))
    for i, x in enumerate(staff):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_03():

    staff = Staff(notetools.make_repeated_notes(16))
    staff[10] = Rest((1, 8))
    for i, x in enumerate(staff):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_04():

    staff = Staff(notetools.make_repeated_notes(16))
    staff[10:10] = [Rest((1, 8))]
    for i, x in enumerate(staff):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_05():

    staff = Staff(notetools.make_repeated_notes(16))
    staff[10:12] = [Rest((1, 8))]
    for i, x in enumerate(staff):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_06():
    r'''Offset works with voices.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(16))
    voice_2 = Voice(notetools.make_repeated_notes(16))
    voice_1.name = voice_2.name = 'voice'
    container = Container([voice_1, voice_2])
    for i, x in enumerate(container.select_leaves()):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_07():

    tuplet = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    for i, x in enumerate(tuplet):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 12)


def test_mutationtools_AttributeInspectionAgent_get_timespan_08():

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    voice = Voice([Note(0, (1, 8)), tuplet_1, Note(0, (1, 8))])
    offset = 0
    durations = [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]
    for x, d in zip(voice.select_leaves(), durations):
        assert inspect(x).get_timespan().start_offset == offset
        offset += Duration(*d)


def test_mutationtools_AttributeInspectionAgent_get_timespan_09():
    r'''Offset works on nested tuplets.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(1, 4), "c'8 c'8 c'8")
    tuplet = tuplettools.FixedDurationTuplet(
        Duration(2, 4), [Note("c'4"), tuplet_1, Note("c'4")])
    offset = 0
    durations = [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]
    for x, d in zip(tuplet.select_leaves(), durations):
        assert inspect(x).get_timespan().start_offset == offset
        offset += Duration(*d)


def test_mutationtools_AttributeInspectionAgent_get_timespan_10():
    r'''Offset works with simultaneous structures.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(16))
    voice_2 = Voice(notetools.make_repeated_notes(16))
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    for i, x in enumerate(voice_1):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(voice_2):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_11():
    r'''Offset on leaves works in nested contexts.
    '''

    voice = Voice(notetools.make_repeated_notes(4))
    staff = Staff([Note(0, (1, 8)), voice, Note(0, (1, 8))])
    for i, x in enumerate(staff.select_leaves(allow_discontiguous_leaves=True)):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(voice.select_leaves()):
        assert inspect(x).get_timespan().start_offset == \
            i * Duration(1, 8) + Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_12():
    r'''Offset on leaves works in sequential contexts.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(4))
    voice_2 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([voice_1, voice_2])
    for i, x in enumerate(voice_1.select_leaves()):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(voice_2.select_leaves()):
        assert inspect(x).get_timespan().start_offset == \
            i * Duration(1, 8) + Duration(1, 2)


def test_mutationtools_AttributeInspectionAgent_get_timespan_13():
    r'''Offset on leaves works in nested simultaneous contexts.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(4))
    voice_2 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    for i, x in enumerate(voice_1.select_leaves()):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)
    for i, x in enumerate(voice_2.select_leaves()):
        assert inspect(x).get_timespan().start_offset == i * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_14():
    r'''Offset on leaves works in nested simultaneous and sequential contexts.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(4))
    voice_2 = Voice(notetools.make_repeated_notes(4))
    v3 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([Container([voice_1, voice_2]), v3])
    staff[0].is_simultaneous = True
    for i, x in enumerate(v3.select_leaves()):
        assert inspect(x).get_timespan().start_offset == \
            i * Duration(1, 8) + Duration(1, 2)


def test_mutationtools_AttributeInspectionAgent_get_timespan_15():
    r'''Offset on leaves works in nested simultaneous and sequential contexts.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(4))
    voice_2 = Voice(notetools.make_repeated_notes(4))
    v3 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([v3, Container([voice_1, voice_2])])
    staff[1].is_simultaneous = True
    for i, x in enumerate(voice_1.select_leaves()):
        assert inspect(x).get_timespan().start_offset == \
            i * Duration(1, 8) + Duration(1, 2)
    for i, x in enumerate(voice_2.select_leaves()):
        assert inspect(x).get_timespan().start_offset == \
            i * Duration(1, 8) + Duration(1, 2)


def test_mutationtools_AttributeInspectionAgent_get_timespan_16():
    r'''Offsets works on sequential voices.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("c'8 d'8 e'8 f'8")])
    staff[0].name = staff[1].name = 'voice'
    for i, x in enumerate(staff):
        assert inspect(x).get_timespan().start_offset == i * Duration(4, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_17():
    r'''Prolated offset does NOT go across sequential staves.
    '''

    container = Container([Staff("c'8 d'8 e'8 f'8"), Staff("c'8 d'8 e'8 f'8")])
    container[0].name = container[1].name = 'staff'
    assert inspect(container[0]).get_timespan().start_offset == Duration(0)
    assert inspect(container[1]).get_timespan().start_offset == Duration(1, 2)


def test_mutationtools_AttributeInspectionAgent_get_timespan_18():
    r'''Offsets works with nested voices.
    '''

    staff = Staff([Voice("c'8 d'8 e'8 f'8"), Voice("c'8 d'8 e'8 f'8")])
    for i, x in enumerate(staff):
        assert inspect(x).get_timespan().start_offset == i * Duration(4, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_19():
    r'''Offsets works on sequential tuplets.
    '''

    voice = Voice(3 * Tuplet(Multiplier(2, 3), "c'8 d'8 e'8"))
    assert inspect(voice[0]).get_timespan().start_offset == 0 * Duration(1, 4)
    assert inspect(voice[1]).get_timespan().start_offset == 1 * Duration(1, 4)
    assert inspect(voice[2]).get_timespan().start_offset == 2 * Duration(1, 4)


def test_mutationtools_AttributeInspectionAgent_get_timespan_20():
    r'''Offsets work on tuplets between notes.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    voice = Voice([Note(0, (1, 8)), tuplet_1, Note(0, (1, 8))])
    assert inspect(voice[0]).get_timespan().start_offset == 0 * Duration(1, 8)
    assert inspect(voice[1]).get_timespan().start_offset == 1 * Duration(1, 8)
    assert inspect(voice[2]).get_timespan().start_offset == 3 * Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_21():
    r'''Offsets work on nested tuplets.
    '''

    tuplet_1 = tuplettools.FixedDurationTuplet(Duration(1, 4), notetools.make_repeated_notes(3))
    tuplet = tuplettools.FixedDurationTuplet(Duration(2, 4), [Note("c'4"), tuplet_1, Note("c'4")])
    assert inspect(tuplet[0]).get_timespan().start_offset == 0 * Duration(1, 6)
    assert inspect(tuplet[1]).get_timespan().start_offset == 1 * Duration(1, 6)
    assert inspect(tuplet[2]).get_timespan().start_offset == 2 * Duration(1, 6)


def test_mutationtools_AttributeInspectionAgent_get_timespan_22():
    r'''Offsets work on nested contexts.
    '''

    inner_voice = Voice(notetools.make_repeated_notes(4))
    outer_voice = Voice([Note(0, (1, 8)), inner_voice])
    inner_voice.name = outer_voice.name = 'voice'
    staff = Staff([Note(1, (1, 8)), outer_voice])
    assert inspect(inner_voice).get_timespan().start_offset == Duration(2, 8)
    assert inspect(outer_voice).get_timespan().start_offset == Duration(1, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_23():
    r'''Offsets work on nested simultaneous contexts.
     '''

    voice_1 = Voice(notetools.make_repeated_notes(4))
    voice_2 = Voice(notetools.make_repeated_notes(4))
    staff = Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    assert inspect(staff[0]).get_timespan().start_offset == 0
    assert inspect(staff[1]).get_timespan().start_offset == 0


def test_mutationtools_AttributeInspectionAgent_get_timespan_24():
    r'''Offsets works in nested simultaneous and sequential contexts.
    '''

    voice_1 = Voice(notetools.make_repeated_notes(4))
    voice_2 = Voice(notetools.make_repeated_notes(4))
    voice_1b= Voice(notetools.make_repeated_notes(4))
    voice_2b= Voice(notetools.make_repeated_notes(4))
    voice_1.name = voice_1b.name = 'voiceOne'
    s1 = Staff([voice_1, voice_1b])
    s2 = Staff([voice_2, voice_2b])
    gs = scoretools.GrandStaff([s1, s2])
    assert inspect(voice_1).get_timespan().start_offset == 0
    assert inspect(voice_2).get_timespan().start_offset == 0
    assert inspect(voice_1b).get_timespan().start_offset == Duration(4, 8)
    assert inspect(voice_2b).get_timespan().start_offset == Duration(4, 8)


def test_mutationtools_AttributeInspectionAgent_get_timespan_25():
    r'''Offset seconds can not calculate without excplit tempo indication.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    statement = 'inspect(staff[0]).get_timespan(in_seconds=True).start_offset'
    assert py.test.raises(MissingTempoError, statement)


def test_mutationtools_AttributeInspectionAgent_get_timespan_26():
    r'''Offset seconds work with explicit tempo indication.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")
    tempo = contexttools.TempoMark(Duration(1, 8), 48, target_context=Staff)
    tempo.attach(staff)

    assert testtools.compare(
        staff,
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

    assert inspect(staff[0]).get_timespan(in_seconds=True).start_offset == \
        Duration(0)
    assert inspect(staff[1]).get_timespan(in_seconds=True).start_offset == \
        Duration(5, 4)
