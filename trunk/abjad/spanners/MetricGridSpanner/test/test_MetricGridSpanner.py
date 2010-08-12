from abjad import *


def test_MetricGridSpanner_01( ):
   t = Staff(Note(0, (1, 8)) * 8)
   m = MetricGridSpanner(t.leaves, [(2, 8)])

   assert t.format == "\\new Staff {\n\t\\time 2/8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''
   \new Staff {
           \time 2/8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
   }
   '''
   

def test_MetricGridSpanner_02( ):
   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGridSpanner(t.leaves, [(3, 16)])

   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''
   \new Staff {
           \time 3/16
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
   }
   '''
   

def test_MetricGridSpanner_03( ):
   '''MetricGrid cycles throught given meters to cover spanner's duration.''' 

   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGridSpanner(t.leaves, [(1, 8), (1, 4)])

   assert t.format == "\\new Staff {\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n}"

   r'''
   \new Staff {
           \time 1/8
           c'8
           \time 1/4
           c'8
           c'8
           \time 1/8
           c'8
           \time 1/4
           c'8
           c'8
           \time 1/8
           c'8
           \time 1/4
           c'8
   }
   '''


def test_MetricGridSpanner_04( ):
   '''MetricGrid knows how to draw itself in the middle of a note. '''

   t = Staff(notetools.make_repeated_notes(8))
   m = MetricGridSpanner(t.leaves, [(3, 16), (2, 8)])

   r'''
   \new Staff {
      \time 3/16
      c'8
      <<
      {
         \time 2/8
         s1 * 1/16
      }
      c'8
      >>
      c'8
      <<
      {
         \time 3/16
         s1 * 1/16
      }
      c'8
      >>
      c'8
      \time 2/8
      c'8
      c'8
      \time 3/16
      c'8
   }
   '''

   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\t<<\n\t{\n\t\t\\time 2/8\n\t\ts1 * 1/16\n\t}\n\tc'8\n\t>>\n\tc'8\n\t<<\n\t{\n\t\t\\time 3/16\n\t\ts1 * 1/16\n\t}\n\tc'8\n\t>>\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"


def test_MetricGridSpanner_05( ):
   '''MetricGrid knows how to draw itself in the middle of a note. '''

   t = Staff(Note(0, (1,2)) * 2)
   m = MetricGridSpanner(t.leaves, [(1, 8), (1, 4)])

   r'''
   \new Staff {
      \time 1/8
      <<
      {
         \time 1/4
         s1 * 1/8
      }
      {
         \time 1/8
         s1 * 3/8
      }
      c'2
      >>
      \time 1/4
      <<
      {
         \time 1/8
         s1 * 1/4
      }
      {
         \time 1/4
         s1 * 3/8
      }
      c'2
      >>
   }
   '''


   assert t.format == "\\new Staff {\n\t\\time 1/8\n\t<<\n\t{\n\t\t\\time 1/4\n\t\ts1 * 1/8\n\t}\n\t{\n\t\t\\time 1/8\n\t\ts1 * 3/8\n\t}\n\tc'2\n\t>>\n\t\\time 1/4\n\t<<\n\t{\n\t\t\\time 1/8\n\t\ts1 * 1/4\n\t}\n\t{\n\t\t\\time 1/4\n\t\ts1 * 3/8\n\t}\n\tc'2\n\t>>\n}"


def test_MetricGridSpanner_06( ):
   '''MetricGrid splits notes on bar lines.'''

   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGridSpanner(t.leaves, [(3, 16)])
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


def test_MetricGridSpanner_07( ):
   '''MetricGrid splits notes on bar lines.'''

   t = Staff(Note(0, (1,8))*8)
   m = MetricGridSpanner(t.leaves, [(3, 16), (2, 8)])
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


def test_MetricGridSpanner_08( ):
   '''MetricGrid split works with tuplets.'''

   t = Voice([FixedMultiplierTuplet((2,3), Note(0, (1,8)) * 6)])
   m = MetricGridSpanner(t.leaves, [(1, 8)])
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


def test_MetricGridSpanner_09( ):
   '''MetricGrid split works with nested tuplets.'''

   t = Voice([FixedMultiplierTuplet((2,3), [Note(0, (1,8)), 
         FixedMultiplierTuplet((3,2), Note(0, (1,8)) *4)])])
   m = MetricGridSpanner(t.leaves, [(1, 8)])
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


def test_MetricGridSpanner_10( ):
   '''MetricGrid split fuses correctly tied leaves in last measure.'''

   v = Voice(Note(1, (1, 4))*3)
   v.extend(resttools.make_rests((5, 4), tied=True))
   m = MetricGridSpanner(v.leaves, [(4, 4)])
   m.split_on_bar( )

   assert isinstance(v[-1], Rest)
   assert v[-1].duration.prolated == Rational(4, 4)
   assert isinstance(v[-2], Rest)
   assert v[-2].duration.prolated == Rational(1, 4)
   assert v[-2].tie.spanner == v[-1].tie.spanner

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


def test_MetricGridSpanner_11( ):
   '''MetricGrid can split conditionally.'''

   v = Voice([Note(1, (1, 4)), Rest((1, 4)), Note(1, (1, 4))])
   def cond(leaf):
      if not isinstance(leaf, Rest): return True
      else: return False
   m = MetricGridSpanner(v.leaves, [(1, 8)])
   m.splitting_condition = cond
   m.split_on_bar( )

   assert componenttools.is_well_formed_component(v)
   assert len(v) == 5
   assert v[0].duration.written == v[1].duration.written == Rational(1, 8)
   assert v[3].duration.written == v[3].duration.written == Rational(1, 8)
   assert v[2].duration.written == Rational(1, 4)
   ties = len([p for p in v.spanners.contained if isinstance(p, TieSpanner)]) == 2
