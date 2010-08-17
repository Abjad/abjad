from abjad import *
from abjad.tools.spannertools._withdraw_from_crossing import _withdraw_from_crossing
import py.test


def test_spannertools_withdraw_from_crossing_01( ):
   '''Withdraw thread-contiguous components from crossing spanners.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   beam = spannertools.BeamSpanner(t[0][:])
   slur = spannertools.SlurSpanner(t[1][:])
   trill = spannertools.TrillSpanner(t.leaves)

   r'''
   \new Voice {
           {
                   c'8 [ \startTrillSpan
                   d'8 ]
           }
           {
                   e'8 (
                   f'8 ) \stopTrillSpan
           }
   }
   '''

   spanners = spannertools.get_spanners_contained_by_components([t])
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   _withdraw_from_crossing([t])
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners


def test_spannertools_withdraw_from_crossing_02( ):
   '''Withdraw thread-contiguous components from crossing spanners.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   beam = spannertools.BeamSpanner(t[0][:])
   slur = spannertools.SlurSpanner(t[1][:])
   trill = spannertools.TrillSpanner(t.leaves)

   r'''
   \new Voice {
           {
                   c'8 [ \startTrillSpan
                   d'8 ]
           }
           {
                   e'8 (
                   f'8 ) \stopTrillSpan
           }
   }
   '''

   spanners = spannertools.get_spanners_contained_by_components(t[0:1])
   assert len(spanners) == 2
   assert beam in spanners
   assert trill in spanners

   _withdraw_from_crossing(t[0:1])

   r'''
   \new Voice {
           {
                   c'8 [
                   d'8 ]
           }
           {
                   e'8 ( \startTrillSpan
                   f'8 ) \stopTrillSpan
           }
   }
   '''

   spanners = spannertools.get_spanners_contained_by_components(t[0:1])
   assert len(spanners) == 1
   assert beam in spanners

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 ( \\startTrillSpan\n\t\tf'8 ) \\stopTrillSpan\n\t}\n}"


def test_spannertools_withdraw_from_crossing_03( ):
   '''Withdraw thread-contiguous components from crossing spanners.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
   macros.diatonicize(t)
   beam = spannertools.BeamSpanner(t[0][:])
   slur = spannertools.SlurSpanner(t[1][:])
   trill = spannertools.TrillSpanner(t.leaves)

   r'''
   \new Voice {
           {
                   c'8 [ \startTrillSpan
                   d'8 ]
           }
           {
                   e'8 (
                   f'8 ) \stopTrillSpan
           }
   }
   '''

   spanners = spannertools.get_spanners_contained_by_components(t.leaves[2:3])
   assert len(spanners) == 2
   assert slur in spanners
   assert trill in spanners

   _withdraw_from_crossing(t.leaves[2:3])

   spanners = spannertools.get_spanners_contained_by_components(t.leaves[2:3])
   assert spanners == set([ ])

   "Operation leaves score tree in weird state."
   "Both slur and trill are now discontiguous."

   assert not componenttools.is_well_formed_component(t)
