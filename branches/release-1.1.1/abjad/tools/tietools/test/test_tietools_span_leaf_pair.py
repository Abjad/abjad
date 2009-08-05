from abjad import *


def test_tietools_span_leaf_pair_01( ):
   '''Span left leaf with spanner and right leaf without spanner.'''
   
   t = Voice(construct.run(4))
   Tie(t[:2])

   r'''\new Voice {
      c'8 ~
      c'8
      c'8
      c'8
   }'''

   tietools.span_leaf_pair(t[1], t[2])

   r'''\new Voice {
      c'8 ~
      c'8 ~
      c'8
      c'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'8 ~\n\tc'8\n\tc'8\n}"


def test_tietools_span_leaf_pair_02( ):
   '''Span left leaf with spanner and right leaf with spanner.'''
   
   t = Voice(construct.run(4))
   Tie(t[:2])
   Tie(t[2:])

   r'''\new Voice {
      c'8 ~
      c'8
      c'8 ~
      c'8
   }'''

   tietools.span_leaf_pair(t[1], t[2])

   r'''\new Voice {
      c'8 ~
      c'8 ~
      c'8 ~
      c'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 ~\n\tc'8 ~\n\tc'8 ~\n\tc'8\n}"


def test_tietools_span_leaf_pair_03( ):
   '''Span left leaves with no spanner.'''
   
   t = Voice(construct.run(4))

   r'''\new Voice {
      c'8 
      c'8
      c'8 
      c'8
   }'''

   tietools.span_leaf_pair(t[1], t[2])

   r'''\new Voice {
      c'8
      c'8 ~
      c'8
      c'8
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8\n\tc'8 ~\n\tc'8\n\tc'8\n}"
