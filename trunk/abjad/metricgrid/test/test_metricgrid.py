from abjad import *
from abjad.tools import construct


def test_metricgrid_01( ):
   t = Staff(Note(0, (1, 8)) * 8)
   m = MetricGrid(t.leaves, [(2, 8)])

   assert t.format == "\\new Staff {\n\t\\time 2/8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''\new Staff {
           \time 2/8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
   }'''
   

def test_metricgrid_02( ):
   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t.leaves, [(3, 16)])

   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''\new Staff {
           \time 3/16
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
           c'8
   }'''
   

def test_metricgrid_03( ):
   '''MetricGrid cycles throught given meters to cover spanner's duration.''' 

   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t.leaves, [(1, 8), (1, 4)])

   assert t.format == "\\new Staff {\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n}"

   r'''\new Staff {
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
   }'''


def test_metricgrid_04( ):
   '''MetricGrid knows how to draw itself in the middle of a note. '''

   t = Staff(construct.run(8))
   m = MetricGrid(t.leaves, [(3, 16), (2, 8)])

   r'''\new Staff {
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
   }'''

   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\t<<\n\t{\n\t\t\\time 2/8\n\t\ts1 * 1/16\n\t}\n\tc'8\n\t>>\n\tc'8\n\t<<\n\t{\n\t\t\\time 3/16\n\t\ts1 * 1/16\n\t}\n\tc'8\n\t>>\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"


def test_metricgrid_05( ):
   '''MetricGrid knows how to draw itself in the middle of a note. '''

   t = Staff(Note(0, (1,2)) * 2)
   m = MetricGrid(t.leaves, [(1, 8), (1, 4)])

   r'''\new Staff {
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
   }'''


   assert t.format == "\\new Staff {\n\t\\time 1/8\n\t<<\n\t{\n\t\t\\time 1/4\n\t\ts1 * 1/8\n\t}\n\t{\n\t\t\\time 1/8\n\t\ts1 * 3/8\n\t}\n\tc'2\n\t>>\n\t\\time 1/4\n\t<<\n\t{\n\t\t\\time 1/8\n\t\ts1 * 1/4\n\t}\n\t{\n\t\t\\time 1/4\n\t\ts1 * 3/8\n\t}\n\tc'2\n\t>>\n}"


def test_metricgrid_splitting_01( ):
   '''MetricGrid splits notes on bar lines.'''

   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t.leaves, [(3, 16)])
   m.splitOnBar( )

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n}"

   r'''\new Staff {
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
   }'''


def test_metricgrid_splitting_02( ):
   '''MetricGrid splits notes on bar lines.'''

   t = Staff(Note(0, (1,8))*8)
   m = MetricGrid(t.leaves, [(3, 16), (2, 8)])
   m.splitOnBar( )

   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\t\\time 2/8\n\tc'16\n\tc'8\n\tc'16 ~\n\t\\time 3/16\n\tc'16\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"

   r'''\new Staff {
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
   }'''


def test_metricgrid_splitting_03( ):
   '''MetricGrid split works with tuplets.'''

   t = Voice([FixedMultiplierTuplet((2,3), Note(0, (1,8)) * 6)])
   m = MetricGrid(t.leaves, [(1, 8)])
   m.splitOnBar( )

   '''MetricGrid splitOnBar works in Tuplets.'''   
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t}\n}"

   r'''\new Voice {
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
   }'''


def test_metricgrid_splitting_04( ):
   '''MetricGrid split works with nested tuplets.'''

   t = Voice([FixedMultiplierTuplet((2,3), [Note(0, (1,8)), 
         FixedMultiplierTuplet((3,2), Note(0, (1,8)) *4)])])
   m = MetricGrid(t.leaves, [(1, 8)])
   m.splitOnBar( )

   assert t.format =="\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\t\\fraction \\times 3/2 {\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t}\n\t}\n}"

   r'''\new Voice {
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
   }'''


def test_metricgrid_splitting_05( ):
   '''MetricGrid split fuses correctly tied leaves in last measure.'''

   v = Voice(Note(1, (1, 4))*3)
   v.extend(construct.rests((5, 4), tied=True))
   m = MetricGrid(v.leaves, [(4, 4)])
   m.splitOnBar( )

   assert isinstance(v[-1], Rest)
   assert v[-1].duration.prolated == Rational(4, 4)
   assert isinstance(v[-2], Rest)
   assert v[-2].duration.prolated == Rational(1, 4)
   assert v[-2].tie.spanner == v[-1].tie.spanner

   r'''\new Voice {
           \time 4/4
           cs'4
           cs'4
           cs'4
           r4 ~
           r1
   }'''


def test_metricgrid_splitting_06( ):
   '''MetricGrid can split conditionally.'''

   v = Voice([Note(1, (1, 4)), Rest((1, 4)), Note(1, (1, 4))])
   def cond(leaf):
      if not isinstance(leaf, Rest): return True
      else: return False
   m = MetricGrid(v.leaves, [(1, 8)])
   m.splittingCondition = cond
   m.splitOnBar( )

   assert check.wf(v)
   assert len(v) == 5
   assert v[0].duration.written == v[1].duration.written == Rational(1, 8)
   assert v[3].duration.written == v[3].duration.written == Rational(1, 8)
   assert v[2].duration.written == Rational(1, 4)
   ties = len([p for p in v.spanners.contained if isinstance(p, Tie)]) == 2
