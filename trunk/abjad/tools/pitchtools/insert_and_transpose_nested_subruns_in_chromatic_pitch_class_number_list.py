from abjad.components.Note import Note
from abjad.tools import componenttools
from abjad.tools import listtools
from abjad.tools.pitchtools.get_named_chromatic_pitch_from_pitch_carrier import \
   get_named_chromatic_pitch_from_pitch_carrier


def insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list(
   notes, subrun_indicators):
   '''Insert transposed subruns according to ``subrun_indicators``.

   *  *pitches* must be a list of zero or more Abjad
      :class:`~abjad.components.Note.note.Note` instances.
   *  *subrun_indicators* must be a list of zero or more
      ``(index, length_list)`` pairs.

   For each ``(index, length_list)`` pair in *subrun_indicators* 
   the function will read *index* mod ``len(notes)`` and insert
   a subrun of length ``length_list[0]`` immediately after ``notes[index]``,
   a subrun of length ``length_list[1]`` immediately after ``notes[index+1]``,
   and, in general, a subrun of ``length_list[i]`` immediately after
   ``notes[index+i]``, for ``i < length(length_list)``.   
   This is easiest to see with an example.

   ::

      abjad> notes = [Note(p, (1, 4)) for p in [0, 2, 7, 9, 5, 11, 4]]
      abjad> subrun_indicators = [(0, [2, 4]), (4, [3, 1])]
      abjad> pitchtools.insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list(notes, subrun_indicators)

      abjad> for x in notes:
         try:
            t.append(x.pitch.pitch_number)
         except AttributeError:
            t.append([y.pitch.pitch_number for y in x])

      abjad> t
      [0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]

   .. note:: New subruns are wrapped with lists.
      These wrapper lists are designed 
      to allow inspection of the structural changes to *notes*
      immediately after the function returns.
      For this reason most calls to this function will be followed
      by ``notes = listtools.flatten_iterable(notes)``.

   ::

      abjad> notes = listtools.flatten_iterable(notes)
      abjad> notes
      [0, 5, 7, 2, 4, 0, 6, 11, 7, 9, 5, 10, 6, 8, 11, 7, 4]

   .. note:: This function is designed to work on a built-in Python list
      of notes. This function is **not** designed to work on Abjad
      voices, staves or other containers because the function currently
      implements no spanner-handling.
      Specifically, this function is designed to be used during
      precomposition when other, similar abstract pitch transforms
      may be common.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.insert_transposed_pc_subruns( )`` to
      ``pitchtools.insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list( )``.

   .. versionchanged:: 1.1.2
      renamed ``pitchtools.insert_and_transpose_nested_subruns_in_lpitch_class_number_list( )`` to
      ``pitchtools.insert_and_transpose_nested_subruns_in_chromatic_pitch_class_number_list( )``.
   '''

   assert isinstance(notes, list)
   assert all([isinstance(x, Note) for x in notes])
   assert isinstance(subrun_indicators, list)

   len_notes = len(notes)
   instructions = [ ]

   for subrun_indicator in subrun_indicators:
      pairs = _make_index_length_pairs(subrun_indicator)
      for anchor_index, subrun_length in pairs:
         anchor_note = notes[anchor_index % len_notes]
         anchor_pitch = get_named_chromatic_pitch_from_pitch_carrier(anchor_note)
         anchor_written_duration = anchor_note.duration.written
         source_start_index = anchor_index + 1
         source_stop_index = source_start_index + subrun_length + 1
         subrun_source = listtools.get_cyclic(
            notes, source_start_index, source_stop_index)
         subrun_intervals = _get_intervals_in_subrun(subrun_source)
         new_notes = _make_new_notes(
            anchor_pitch, anchor_written_duration, subrun_intervals)
         instruction = (anchor_index, new_notes)
         instructions.append(instruction)

   for anchor_index, new_notes in reversed(sorted(instructions)):
      notes.insert(anchor_index + 1, new_notes)


def _get_intervals_in_subrun(subrun_source):
   subrun_source = list(subrun_source)
   result = [0]
   for first, second in listtools.pairwise(subrun_source):
      first_pitch = get_named_chromatic_pitch_from_pitch_carrier(first)
      second_pitch = get_named_chromatic_pitch_from_pitch_carrier(second)
      interval = abs(second_pitch.numbered_chromatic_pitch) - \
         abs(first_pitch.numbered_chromatic_pitch)
      result.append(interval + result[-1])
   result.pop(0)
   return result


def _make_index_length_pairs(subrun_indicator):
   anchor_index, subrun_lengths = subrun_indicator
   num_subruns = len(subrun_lengths)
   pairs = [ ]
   for i in range(num_subruns):
      start_index = anchor_index + i
      subrun_length = subrun_lengths[i]
      pair = (start_index, subrun_length)
      pairs.append(pair)
   return pairs


def _make_new_notes(anchor_pitch, anchor_written_duration, subrun_intervals):
   new_notes = [ ]
   for subrun_interval in subrun_intervals:
      new_pc = (abs(anchor_pitch.numbered_chromatic_pitch) + subrun_interval) % 12
      new_note = Note(new_pc, anchor_written_duration)
      new_notes.append(new_note)
   return new_notes
