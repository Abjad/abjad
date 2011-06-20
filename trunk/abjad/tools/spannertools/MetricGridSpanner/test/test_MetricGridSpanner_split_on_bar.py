from abjad import *
import py.test


def test_MetricGridSpanner_split_on_bar_01( ):
   '''MetricGrid splits notes on bar lines.'''
   py.test.skip('something weird with grace notes in _fuse_tied_leaves_within_measures.')

   t = Staff(Note(0, (1,8)) * 8)
   m = spannertools.MetricGridSpanner(t.leaves, [(3, 16)])
   m.split_on_bar( )

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n}"

   r'''
   \new Staff {
           \time 3/16
           c'8
           c'16 ~
           c'16
           c'8
           c'8
           c'16 ~
           c'16
           c'8
           c'8
           c'16 ~
           c'16
   }
   '''


def test_MetricGridSpanner_split_on_bar_02( ):
   '''MetricGrid splits notes on bar lines.'''
   py.test.skip('something weird with grace notes.')
   
   t = Staff(Note(0, (1,8))*8)
   m = spannertools.MetricGridSpanner(t.leaves, [(3, 16), (2, 8)])
   m.split_on_bar( )

   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\t\\time 2/8\n\tc'16\n\tc'8\n\tc'16 ~\n\t\\time 3/16\n\tc'16\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"

   r'''
   \new Staff {
           \time 3/16
           c'8
           c'16 ~
           \time 2/8
           c'16
           c'8
           c'16 ~
           \time 3/16
           c'16
           c'8
           \time 2/8
           c'8
           c'8
           \time 3/16
           c'8
   }
   '''


def test_MetricGridSpanner_split_on_bar_03( ):
   '''MetricGrid split works with tuplets.'''
   py.test.skip('something weird with grace notes.')

   t = Voice([Tuplet(Fraction(2,3), Note(0, (1,8)) * 6)])
   m = spannertools.MetricGridSpanner(t.leaves, [(1, 8)])
   m.split_on_bar( )

   '''MetricGrid split_on_bar works in Tuplets.'''   
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t}\n}"

   r'''
   \new Voice {
           \times 2/3 {
                   \time 1/8
                   c'8
                   c'16 ~
                   c'16
                   c'8
                   c'8
                   c'16 ~
                   c'16
                   c'8
           }
   }
   '''


def test_MetricGridSpanner_split_on_bar_04( ):
   '''MetricGrid split works with nested tuplets.'''
   py.test.skip('something weird with grace notes.')

   t = Voice([Tuplet(Fraction(2,3), [Note(0, (1,8)), 
         Tuplet(Fraction(3,2), Note(0, (1,8)) *4)])])
   m = spannertools.MetricGridSpanner(t.leaves, [(1, 8)])
   m.split_on_bar( )

   assert t.format =="\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\t\\fraction \\times 3/2 {\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t}\n\t}\n}"

   r'''
   \new Voice {
           \times 2/3 {
                   \time 1/8
                   c'8
                   \fraction \times 3/2 {
                           \times 2/3 {
                                   c'16 ~
                           }
                           \times 2/3 {
                                   c'8
                           }
                           \times 2/3 {
                                   c'16 ~
                           }
                           \times 2/3 {
                                   c'8
                           }
                           \times 2/3 {
                                   c'16 ~
                           }
                           \times 2/3 {
                                   c'8
                           }
                           \times 2/3 {
                                   c'16 ~
                           }
                           \times 2/3 {
                                   c'8
                           }
                   }
           }
   }
   '''


def test_MetricGridSpanner_split_on_bar_05( ):
   '''MetricGrid split fuses correctly tied leaves in last measure.'''
   py.test.skip('something weird with grace notes.')

   v = Voice(Note(1, (1, 4))*3)
   v.extend(resttools.make_rests((5, 4), tied=True))
   m = spannertools.MetricGridSpanner(v.leaves, [(4, 4)])
   m.split_on_bar( )

   assert isinstance(v[-1], Rest)
   assert v[-1].duration.prolated == Duration(4, 4)
   assert isinstance(v[-2], Rest)
   assert v[-2].duration.prolated == Duration(1, 4)
   #assert v[-2].tie.spanner == v[-1].tie.spanner
   assert spannertools.get_the_only_spanner_attached_to_component(
      v[-2], tietools.TieSpanner) == \
      spannertools.get_the_only_spanner_attached_to_component(
      v[-1], tietools.TieSpanner)

   r'''
   \new Voice {
           \time 4/4
           cs'4
           cs'4
           cs'4
           r4 ~
           r1
   }
   '''


def test_MetricGridSpanner_split_on_bar_06( ):
   '''MetricGrid can split conditionally.'''
   py.test.skip('something weird with grace notes.')

   v = Voice([Note(1, (1, 4)), Rest((1, 4)), Note(1, (1, 4))])
   def cond(leaf):
      if not isinstance(leaf, Rest): return True
      else: return False
   m = spannertools.MetricGridSpanner(v.leaves, [(1, 8)])
   m.splitting_condition = cond
   m.split_on_bar( )

   assert componenttools.is_well_formed_component(v)
   assert len(v) == 5
   assert v[0].duration.written == v[1].duration.written == Duration(1, 8)
   assert v[3].duration.written == v[3].duration.written == Duration(1, 8)
   assert v[2].duration.written == Duration(1, 4)
   #ties = len([p for p in v.spanners.contained if isinstance(p, tietools.TieSpanner)]) == 2
   ties = spannertools.get_spanners_attached_to_any_improper_child_of_component(
      v, tietools.TieSpanner)
   assert len(ties) == 2
