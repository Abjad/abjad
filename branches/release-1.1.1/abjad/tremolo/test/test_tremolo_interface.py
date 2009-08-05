from abjad import * 

### FORMATTING ###

def test_tremolo_interface_01( ):
   '''Tremolo formats correctly on Note.'''
   t = Note(1, (1, 4))
   t.tremolo.subdivision = 8
   assert t.format == "cs'4 :8"
   t.tremolo.subdivision = None
   assert t.format == "cs'4"


def test_tremolo_interface_02( ):
   '''Tremolo formats correctly on Chord.'''
   t = Chord([1, 2, 3], (1, 4))
   t.tremolo.subdivision = 8
   assert t.format == "<cs' d' ef'>4 :8"
   t.tremolo.subdivision = None
   assert t.format == "<cs' d' ef'>4"


def test_tremolo_interface_03( ):
   '''Tremolo formats correctly on Rest.'''
   t = Rest((1, 4))
   t.tremolo.subdivision = 8
   assert t.format == "r4 :8"
   t.tremolo.subdivision = None
   assert t.format == "r4"

