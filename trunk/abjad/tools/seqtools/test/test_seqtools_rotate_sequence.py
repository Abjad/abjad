from abjad import *


def test_seqtools_rotate_sequence_01( ):

   sequence = range(10)
   new = seqtools.rotate_sequence(sequence, -3)
   assert new == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

   new = seqtools.rotate_sequence(sequence, 4)
   assert new == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

   new = seqtools.rotate_sequence(sequence, 0)
   assert new == sequence
   assert new is not sequence


def test_seqtools_rotate_sequence_02( ):
   '''Return sequence type.
   '''

   sequence = range(10)
   new = seqtools.rotate_sequence(sequence, -1)
   assert isinstance(new, type(sequence))

   sequence = tuple(range(10))
   new = seqtools.rotate_sequence(sequence, -1)
   assert isinstance(new, type(sequence))


def test_seqtools_rotate_sequence_03( ):
   '''Rotate Abjad container.
   '''

   container_1 = Container("c'8 d'8 e'8 f'8")
   container_2 = seqtools.rotate_sequence(container_1, -1)

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


def test_seqtools_rotate_sequence_04( ):
   '''Rotate notes.
   '''

   notes_1 = iotools.parse_lilypond_input_string("c'8 d'8 e'8 f'8")
   notes_2 = seqtools.rotate_sequence(notes_1, -1)

   for note in notes_2:
      assert note not in notes_1


def test_seqtools_rotate_sequence_05( ):
   '''Rotate named chromatic pitch segment.
   '''

   named_chromatic_pitch_segment_1 = pitchtools.NamedChromaticPitchSegment("c'' d'' e'' f''")
   named_chromatic_pitch_segment_2 = seqtools.rotate_sequence(named_chromatic_pitch_segment_1, -1)
   named_chromatic_pitch_segment_3 = pitchtools.NamedChromaticPitchSegment("d'' e'' f'' c''")

   assert named_chromatic_pitch_segment_2 == named_chromatic_pitch_segment_3
   assert isinstance(named_chromatic_pitch_segment_1, pitchtools.NamedChromaticPitchSegment)
   assert isinstance(named_chromatic_pitch_segment_2, pitchtools.NamedChromaticPitchSegment)
   assert isinstance(named_chromatic_pitch_segment_3, pitchtools.NamedChromaticPitchSegment)
