from abjad import *


def test_fuse_contents_by_counts_01( ):
   '''Glom voice.'''

   t = Voice(leaftools.make_repeated_notes(5, Rational(1, 16)))
   Slur(t[:])
   fuse.contents_by_counts(t, [1, 2, 2])

   r'''
   \new Voice {
      c'16 (
      c'8
      c'8 )
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'16 (\n\tc'8\n\tc'8 )\n}"


def test_fuse_contents_by_counts_02( ):
   '''Glom voice and render big-endian tied values.'''

   t = Voice(leaftools.make_repeated_notes(5))
   Slur(t[:])
   fuse.contents_by_counts(t, [5], direction = 'big-endian')

   r'''
   \new Voice {
      c'2 ( ~
      c'8 )
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'2 ( ~\n\tc'8 )\n}"


def test_fuse_contents_by_counts_03( ):
   '''Glom voice and render big-endian tied values.'''

   t = Voice(leaftools.make_repeated_notes(5))
   Slur(t)
   fuse.contents_by_counts(t, [5], direction = 'little-endian')

   r'''
   \new Voice {
      c'8 ( ~
      c'2 )
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 ( ~\n\tc'2 )\n}"


def test_fuse_contents_by_counts_04( ):
   '''Glom voice into rests.'''

   t = Voice(leaftools.make_repeated_notes(5))
   fuse.contents_by_counts(t, [1, 2, 2], Rest)

   r'''
   \new Voice {
      r8
      r4
      r4
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\new Voice {\n\tr8\n\tr4\n\tr4\n}'
