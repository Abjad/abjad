from abjad.note.note import Note
from abjad.tools import clone


def insert_transposed_pc_subruns(notes, subrun_indicators, history = False):
   '''Insert transposed subruns according to ``subrun_indicators``.

   *  *pitches* must be a list of zero or more Abjad \
      :class:`~abjad.note.note.Note` instances.
   *  *subrun_indicators* must be a list of zero or more \
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
      abjad> new_notes = 
         pitchtools.insert_transposed_pc_subruns(notes, subrun_indicators)
      abjad> [new_note.pitch.number for new_note in new_notes]
      [0, 5, 7, 2, 4, 0, 6, 11, 7, 9, 5, 10, 6, 8, 11, 7, 4]

   Newly created transposed inserts are shown in the innermost pairs of
   brackets below::

      [0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]

   .. todo:: Implement a *flattened* keyword to return output as above.'''

   assert all([isinstance(x, Note) for x in notes])
   assert isinstance(subrun_indicators, list)

   cloned_notes = clone.unspan(notes)
   len_notes = len(cloned_notes)
   instructions = [ ]

   #print [x.pitch.number for x in cloned_notes]

   # for (0, [2, 4])
   for (anchor_index, subrun_lengths) in subrun_indicators:
      #print anchor_index, subrun_lengths
      # pairs are [(0, 2), (1, 4)]
      pairs = [ ]
      num_subruns = len(subrun_lengths)
      for i in range(num_subruns):
         starting_note_index = anchor_index + i
         length_of_following_subrun = subrun_lengths[i]
         pair = (starting_note_index, length_of_following_subrun)
         pairs.append(pair)
      #print pairs
      for starting_note_index, length_of_following_subrun in pairs:
         #print starting_note_index, length_of_following_subrun
         real_starting_note = notes[starting_note_index % len_notes]
         cloned_starting_note = cloned_notes[starting_note_index % len_notes]
         #print real_starting_note, cloned_starting_note
         tag = real_starting_note.history.get('tag', None)
         cloned_starting_note.history['tag'] = tag
         new_notes = [ ]
         start = starting_note_index + 1
         stop = start + length_of_following_subrun
         #print start, stop
         cloned_starting_note_pc = cloned_starting_note.pitch.pc
         written_duration = cloned_starting_note.duration.written
         local_start_note_pc = cloned_notes[start].pitch.pc
         for index in range(start, stop):
            start_note = cloned_notes[index % len_notes]
            stop_note = cloned_notes[(index + 1) % len_notes]
            interval = stop_note.pitch.pc - local_start_note_pc
            #print stop_note, start_note, interval
            new_pc = (interval + cloned_starting_note_pc) % 12
            new_note = Note(new_pc, written_duration)
            if isinstance(history, str):
               starting_note_tag = cloned_starting_note.history['tag']
               if starting_note_tag is not None:
                  new_note.history['tag'] = starting_note_tag + history
               else:
                  new_note.history['tag'] = history
            new_notes.append(new_note)
         instruction = (starting_note_index + 1, new_notes)
         instructions.append(instruction)

   for index, new_notes in reversed(sorted(instructions)):
      cloned_notes[index:index] = new_notes

   return cloned_notes
