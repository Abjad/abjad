from abjad import *


def test_fuse_contents_by_count_01( ):
   '''Glom voice.'''

   t = Voice(construct.run(5, Rational(1, 16)))
   Slur(t[:])
   fuse.contents_by_count(t, [1, 2, 2])

   r'''\new Voice {
      c'16 (
      c'8
      c'8 )
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'16 (\n\tc'8\n\tc'8 )\n}"


def test_fuse_contents_by_count_02( ):
   '''Glom voice and render big-endian tied values.'''

   t = Voice(construct.run(5))
   Slur(t[:])
   fuse.contents_by_count(t, [5], direction = 'big-endian')

   r'''\new Voice {
      c'2 ( ~
      c'8 )
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'2 ( ~\n\tc'8 )\n}"


def test_fuse_contents_by_count_03( ):
   '''Glom voice and render big-endian tied values.'''

   t = Voice(construct.run(5))
   Slur(t)
   fuse.contents_by_count(t, [5], direction = 'little-endian')

   r'''\new Voice {
      c'8 ( ~
      c'2 )
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 ( ~\n\tc'2 )\n}"


def test_fuse_contents_by_count_04( ):
   '''Glom voice into rests.'''

   t = Voice(construct.run(5))
   fuse.contents_by_count(t, [1, 2, 2], Rest((1, 4)))

   r'''\new Voice {
      r8
      r4
      r4
   }'''

   assert check.wf(t)
   assert t.format == '\\new Voice {\n\tr8\n\tr4\n\tr4\n}'
