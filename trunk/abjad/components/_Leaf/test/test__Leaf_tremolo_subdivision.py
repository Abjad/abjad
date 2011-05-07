from abjad import * 


def test__Leaf_tremolo_subdivision_01( ):
   '''Tremolo formats correctly on Note.'''

   t = Note(1, (1, 4))
   t.tremolo_subdivision = 8
   assert t.format == "cs'4 :8"
   t.tremolo_subdivision = None
   assert t.format == "cs'4"


def test__Leaf_tremolo_subdivision_02( ):
   '''Tremolo formats correctly on Chord.'''

   t = Chord([1, 2, 3], (1, 4))
   t.tremolo_subdivision = 8
   assert t.format == "<cs' d' ef'>4 :8"
   t.tremolo_subdivision = None
   assert t.format == "<cs' d' ef'>4"


def test__Leaf_tremolo_subdivision_03( ):
   '''Tremolo formats correctly on Rest.'''

   t = Rest((1, 4))
   t.tremolo_subdivision = 8
   assert t.format == "r4 :8"
   t.tremolo_subdivision = None
   assert t.format == "r4"
