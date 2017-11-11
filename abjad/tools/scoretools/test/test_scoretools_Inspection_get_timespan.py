import abjad
import pytest


def test_scoretools_Inspection_get_timespan_01():

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    for i, x in enumerate(voice):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_02():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    for i, x in enumerate(staff):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_03():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[-1] = abjad.Rest((1, 8))
    for i, x in enumerate(staff):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_04():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[10:10] = [abjad.Rest((1, 8))]
    for i, x in enumerate(staff):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_05():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    staff[10:12] = [abjad.Rest((1, 8))]
    for i, x in enumerate(staff):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_06():
    r'''Offset works with voices.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.name = voice_2.name = 'voice'
    container = abjad.Container([voice_1, voice_2])
    leaves = abjad.select(container).leaves()
    for i, x in enumerate(leaves):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_07():

    tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    for i, x in enumerate(tuplet):
        assert abjad.inspect(x).get_timespan().start_offset == i * abjad.Offset(1, 12)


def test_scoretools_Inspection_get_timespan_08():

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    voice = abjad.Voice([abjad.Note(0, (1, 8)), tuplet_1, abjad.Note(0, (1, 8))])
    offset = 0
    durations = [(1, 8), (1, 12), (1, 12), (1, 12), (1, 8)]
    leaves = abjad.select(voice).leaves()
    for leaf, duration in zip(leaves, durations):
        assert abjad.inspect(leaf).get_timespan().start_offset == offset
        offset += abjad.Offset(*duration)


def test_scoretools_Inspection_get_timespan_09():
    r'''Offset works on nested tuplets.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    tuplet = abjad.Tuplet((2, 3), [abjad.Note("c'4"), tuplet_1, abjad.Note("c'4")])
    offset = 0
    durations = [(1, 6), (1, 18), (1, 18), (1, 18), (1, 6)]
    leaves = abjad.select(tuplet).leaves()
    for leaf, duration in zip(leaves, durations):
        assert abjad.inspect(leaf).get_timespan().start_offset == offset
        offset += abjad.Offset(*duration)


def test_scoretools_Inspection_get_timespan_10():
    r'''Offset works with simultaneous structures.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_11():
    r'''Offset on leaves works in nested contexts.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([abjad.Note(0, (1, 8)), voice, abjad.Note(0, (1, 8))])
    leaves = abjad.select(staff).leaves()
    for i, leaf in enumerate(leaves):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8)
    leaves = abjad.select(voice).leaves()
    for i, leaf in enumerate(leaves):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8) + abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_12():
    r'''Offset on leaves works in sequential contexts.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8) + abjad.Offset(1, 2)


def test_scoretools_Inspection_get_timespan_13():
    r'''Offset on leaves works in nested simultaneous contexts.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_14():
    r'''Offset on leaves works in nested simultaneous and sequential contexts.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_3 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([abjad.Container([voice_1, voice_2]), voice_3])
    staff[0].is_simultaneous = True
    for i, leaf in enumerate(voice_3):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8) + abjad.Offset(1, 2)


def test_scoretools_Inspection_get_timespan_15():
    r'''Offset on leaves works in nested simultaneous and sequential contexts.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_3 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_3, abjad.Container([voice_1, voice_2])])
    staff[1].is_simultaneous = True
    for i, leaf in enumerate(voice_1):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8) + abjad.Offset(1, 2)
    for i, leaf in enumerate(voice_2):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(1, 8) + abjad.Offset(1, 2)


def test_scoretools_Inspection_get_timespan_16():
    r'''Offsets works on sequential voices.
    '''

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("c'8 d'8 e'8 f'8")])
    staff[0].name = staff[1].name = 'voice'
    for i, voice in enumerate(staff):
        start_offset = abjad.inspect(voice).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(4, 8)


def test_scoretools_Inspection_get_timespan_17():
    r'''Prolated offset does NOT go across sequential staves.
    '''

    container = abjad.Container([abjad.Staff("c'8 d'8 e'8 f'8"), abjad.Staff("c'8 d'8 e'8 f'8")])
    container[0].name = container[1].name = 'staff'
    start_offset = abjad.inspect(container[0]).get_timespan().start_offset
    assert start_offset == abjad.Offset(0)
    start_offset = abjad.inspect(container[1]).get_timespan().start_offset
    assert start_offset == abjad.Offset(1, 2)


def test_scoretools_Inspection_get_timespan_18():
    r'''Offsets works with nested voices.
    '''

    staff = abjad.Staff([abjad.Voice("c'8 d'8 e'8 f'8"), abjad.Voice("c'8 d'8 e'8 f'8")])
    for i, voice in enumerate(staff):
        start_offset = abjad.inspect(voice).get_timespan().start_offset
        assert start_offset == i * abjad.Offset(4, 8)


def test_scoretools_Inspection_get_timespan_19():
    r'''Offsets works on sequential tuplets.
    '''

    voice = abjad.Voice(3 * abjad.Tuplet(abjad.Multiplier(2, 3), "c'8 d'8 e'8"))
    assert abjad.inspect(voice[0]).get_timespan().start_offset == 0 * abjad.Offset(1, 4)
    assert abjad.inspect(voice[1]).get_timespan().start_offset == 1 * abjad.Offset(1, 4)
    assert abjad.inspect(voice[2]).get_timespan().start_offset == 2 * abjad.Offset(1, 4)


def test_scoretools_Inspection_get_timespan_20():
    r'''Offsets work on tuplets between notes.
    '''

    tuplet_1 = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    voice = abjad.Voice([abjad.Note(0, (1, 8)), tuplet_1, abjad.Note(0, (1, 8))])
    assert abjad.inspect(voice[0]).get_timespan().start_offset == 0 * abjad.Offset(1, 8)
    assert abjad.inspect(voice[1]).get_timespan().start_offset == 1 * abjad.Offset(1, 8)
    assert abjad.inspect(voice[2]).get_timespan().start_offset == 3 * abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_21():
    r'''Offsets work on nested tuplets.
    '''

    tuplet_1 = abjad.Tuplet((1, 2), "c'8 d'8 e'8 f'8")
    contents = [abjad.Note("c'4"), tuplet_1, abjad.Note("c'4")]
    tuplet = abjad.Tuplet((2, 3), contents)
    assert abjad.inspect(tuplet[0]).get_timespan().start_offset == 0 * abjad.Offset(1, 6)
    assert abjad.inspect(tuplet[1]).get_timespan().start_offset == 1 * abjad.Offset(1, 6)
    assert abjad.inspect(tuplet[2]).get_timespan().start_offset == 2 * abjad.Offset(1, 6)


def test_scoretools_Inspection_get_timespan_22():
    r'''Offsets work on nested contexts.
    '''

    inner_voice = abjad.Voice("c'8 d'8 e'8 f'8")
    outer_voice = abjad.Voice([abjad.Note(0, (1, 8)), inner_voice])
    inner_voice.name = outer_voice.name = 'voice'
    staff = abjad.Staff([abjad.Note(1, (1, 8)), outer_voice])
    assert abjad.inspect(inner_voice).get_timespan().start_offset == abjad.Offset(2, 8)
    assert abjad.inspect(outer_voice).get_timespan().start_offset == abjad.Offset(1, 8)


def test_scoretools_Inspection_get_timespan_23():
    r'''Offsets work on nested simultaneous contexts.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    staff = abjad.Staff([voice_1, voice_2])
    staff.is_simultaneous = True
    assert abjad.inspect(staff[0]).get_timespan().start_offset == 0
    assert abjad.inspect(staff[1]).get_timespan().start_offset == 0


def test_scoretools_Inspection_get_timespan_24():
    r'''Offsets works in nested simultaneous and sequential contexts.
    '''

    voice_1 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2 = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1b = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_2b = abjad.Voice("c'8 d'8 e'8 f'8")
    voice_1.name = voice_1b.name = 'voiceOne'
    staff_1 = abjad.Staff([voice_1, voice_1b])
    staff_2 = abjad.Staff([voice_2, voice_2b])
    gs = abjad.StaffGroup([staff_1, staff_2])
    assert abjad.inspect(voice_1).get_timespan().start_offset == 0
    assert abjad.inspect(voice_2).get_timespan().start_offset == 0
    assert abjad.inspect(voice_1b).get_timespan().start_offset == abjad.Offset(4, 8)
    assert abjad.inspect(voice_2b).get_timespan().start_offset == abjad.Offset(4, 8)


def test_scoretools_Inspection_get_timespan_25():
    r'''Offset seconds can not calculate without excplit metronome mark.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    statement = 'inspect(staff[0]).get_timespan(in_seconds=True).start_offset'
    assert pytest.raises(Exception, statement)


def test_scoretools_Inspection_get_timespan_26():
    r'''Offset seconds work with explicit metronome mark.
    '''

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    mark = abjad.MetronomeMark(abjad.Duration(1, 8), 48)
    abjad.attach(mark, staff[0], context='Staff')

    assert format(staff) == abjad.String.normalize(
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

    start_offset = abjad.inspect(staff[0]).get_timespan(in_seconds=True).start_offset
    assert start_offset == abjad.Offset(0)
    start_offset = abjad.inspect(staff[1]).get_timespan(in_seconds=True).start_offset
    assert start_offset == abjad.Offset(5, 4)
