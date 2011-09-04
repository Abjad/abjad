from abjad import *
from abjad.tools import sequencetools
from abjad.tools import iotools


def test_sequencetools_rotate_sequence_01():
    '''Rotate sequence by distance less than or equal to sequence length.
    '''

    assert sequencetools.rotate_sequence(range(10), -3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert sequencetools.rotate_sequence(range(10), 4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert sequencetools.rotate_sequence(range(10), 0) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_sequencetools_rotate_sequence_02():
    '''Rotate sequence by distance greatern than sequence length.
    '''

    assert sequencetools.rotate_sequence(range(10), -23) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert sequencetools.rotate_sequence(range(10), 24) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]


def test_sequencetools_rotate_sequence_03():
    '''Return sequence type.
    '''

    sequence = range(10)
    new = sequencetools.rotate_sequence(sequence, -1)
    assert isinstance(new, type(sequence))

    sequence = tuple(range(10))
    new = sequencetools.rotate_sequence(sequence, -1)
    assert isinstance(new, type(sequence))


def test_sequencetools_rotate_sequence_04():
    '''Rotate Abjad container.
    '''

    container_1 = Container("c'8 d'8 e'8 f'8")
    container_2 = sequencetools.rotate_sequence(container_1, -1)

    r'''
    {
        d'8
        e'8
        f'8
        c'8
    }
    '''

    assert componenttools.is_well_formed_component(container_1)
    assert componenttools.is_well_formed_component(container_2)
    assert container_2.format == "{\n\td'8\n\te'8\n\tf'8\n\tc'8\n}"
    assert container_2 is not container_1
    assert container_1[0] is not container_2[-1]


def test_sequencetools_rotate_sequence_05():
    '''Rotate notes.
    '''

    notes_1 = iotools.parse_lilypond_input_string("c'8 d'8 e'8 f'8")
    notes_2 = sequencetools.rotate_sequence(notes_1, -1)

    for note in notes_2:
        assert note not in notes_1


def test_sequencetools_rotate_sequence_06():
    '''Rotate named chromatic pitch segment.
    '''

    named_chromatic_pitch_segment_1 = pitchtools.NamedChromaticPitchSegment("c'' d'' e'' f''")
    named_chromatic_pitch_segment_2 = sequencetools.rotate_sequence(named_chromatic_pitch_segment_1, -1)
    named_chromatic_pitch_segment_3 = pitchtools.NamedChromaticPitchSegment("d'' e'' f'' c''")

    assert named_chromatic_pitch_segment_2 == named_chromatic_pitch_segment_3
    assert isinstance(named_chromatic_pitch_segment_1, pitchtools.NamedChromaticPitchSegment)
    assert isinstance(named_chromatic_pitch_segment_2, pitchtools.NamedChromaticPitchSegment)
    assert isinstance(named_chromatic_pitch_segment_3, pitchtools.NamedChromaticPitchSegment)
