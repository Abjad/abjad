# -*- encoding: utf-8 -*-
from abjad.tools import sequencetools


# TODO: remove from public API altogether
def insert_and_transpose_nested_subruns_in_pitch_class_number_list(
    notes, 
    subrun_tokens,
    ):
    '''Insert and transpose nested subruns in `pitch_class_number_list`
    according to `subrun_tokens`:

    ::

        >>> notes = [Note(p, (1, 4)) for p in [0, 2, 7, 9, 5, 11, 4]]
        >>> subrun_tokens = [(0, [2, 4]), (4, [3, 1])]
        >>> pitchtools.insert_and_transpose_nested_subruns_in_pitch_class_number_list(
        ... notes, subrun_tokens)

        >>> t = []
        >>> for x in notes:
        ...   try:
        ...        t.append(x.written_pitch.pitch_number)
        ...   except AttributeError:
        ...        t.append([y.written_pitch.pitch_number for y in x])

        >>> t
        [0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]

    Set `subrun_tokens` to a list of zero or more ``(index, length_list)`` pairs.

    For each ``(index, length_list)`` pair in *subrun_tokens*
    the function will read *index* mod ``len(notes)`` and insert
    a subrun of length ``length_list[0]`` immediately after ``notes[index]``,
    a subrun of length ``length_list[1]`` immediately after ``notes[index+1]``,
    and, in general, a subrun of ``length_list[i]`` immediately after
    ``notes[index+i]``, for ``i < length(length_list)``.

    New subruns are wrapped with lists.
    These wrapper lists are designed
    to allow inspection of the structural changes to *notes*
    immediately after the function returns.
    For this reason most calls to this function will be followed
    by ``notes = sequencetools.flatten_sequence(notes)``:

    ::

        >>> for note in notes: note
        ...
        Note("c'4")
        [Note("f'4"), Note("g'4")]
        Note("d'4")
        [Note("e'4"), Note("c'4"), Note("fs'4"), Note("b'4")]
        Note("g'4")
        Note("a'4")
        Note("f'4")
        [Note("bf'4"), Note("fs'4"), Note("af'4")]
        Note("b'4")
        [Note("g'4")]
        Note("e'4")

    This function is designed to work on a built-in Python list
    of notes. This function is **not** designed to work on Abjad
    voices, staves or other containers because the function currently
    implements no spanner-handling.
    That is, this function is designed to be used during
    precomposition when other, similar abstract pitch transforms
    may be common.

    Returns list of integers and / or floats.
    '''
    from abjad.tools import scoretools
    from abjad.tools import pitchtools

    assert isinstance(notes, list)
    assert all(isinstance(x, scoretools.Note) for x in notes)
    assert isinstance(subrun_tokens, list)

    len_notes = len(notes)
    instructions = []

    for subrun_token in subrun_tokens:
        pairs = _make_index_length_pairs(subrun_token)
        for anchor_index, subrun_length in pairs:
            anchor_note = notes[anchor_index % len_notes]
            anchor_pitch = pitchtools.get_named_pitch_from_pitch_carrier(anchor_note)
            anchor_written_duration = anchor_note.written_duration
            source_start_index = anchor_index + 1
            source_stop_index = source_start_index + subrun_length + 1
            subrun_source = sequencetools.iterate_sequence_cyclically_from_start_to_stop(
                notes, source_start_index, source_stop_index)
            subrun_intervals = _get_intervals_in_subrun(subrun_source)
            new_notes = _make_new_notes(
                anchor_pitch, anchor_written_duration, subrun_intervals)
            instruction = (anchor_index, new_notes)
            instructions.append(instruction)

    for anchor_index, new_notes in reversed(sorted(instructions)):
        notes.insert(anchor_index + 1, new_notes)


def _get_intervals_in_subrun(subrun_source):
    from abjad.tools import pitchtools

    subrun_source = list(subrun_source)
    result = [0]
    for first, second in sequencetools.iterate_sequence_pairwise_strict(
        subrun_source):
        first_pitch = pitchtools.get_named_pitch_from_pitch_carrier(first)
        second_pitch = pitchtools.get_named_pitch_from_pitch_carrier(second)
        interval = pitchtools.NumberedPitch(second_pitch).pitch_number - \
            pitchtools.NumberedPitch(first_pitch).pitch_number
        result.append(interval + result[-1])
    result.pop(0)
    return result


def _make_index_length_pairs(subrun_token):
    anchor_index, subrun_lengths = subrun_token
    num_subruns = len(subrun_lengths)
    pairs = []
    for i in range(num_subruns):
        start_index = anchor_index + i
        subrun_length = subrun_lengths[i]
        pair = (start_index, subrun_length)
        pairs.append(pair)
    return pairs


def _make_new_notes(anchor_pitch, anchor_written_duration, subrun_intervals):
    from abjad.tools import pitchtools
    from abjad.tools import scoretools
    new_notes = []
    for subrun_interval in subrun_intervals:
        new_pc = (pitchtools.NumberedPitch(anchor_pitch).pitch_number +
            subrun_interval) % 12
        new_note = scoretools.Note(new_pc, anchor_written_duration)
        new_notes.append(new_note)
    return new_notes
