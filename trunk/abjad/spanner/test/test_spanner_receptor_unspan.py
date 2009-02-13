from abjad import *


def test_spanner_receptor_unspan_01( ):
   '''Unspan a spanned leaf.'''

   t = Note(0, (1, 8))
   Beam(t)
   t.beam.unspan( )

   r'''
   c'8
   '''

   assert check(t)
   assert t.format == "c'8"


def test_spanner_receptor_unspan_02( ):
   '''Unspan an already unspanned leaf.'''

   t = Note(0, (1, 8))
   t.beam.unspan( )

   r'''
   c'8
   '''

   assert check(t)
   assert t.format == "c'8"
