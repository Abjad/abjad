from abjad import *

def test_metricgrid_01( ):
   t = Staff(Note(0, (1, 8)) * 8)
   m = MetricGrid(t, [(2, 8)])
   assert t.format == "\\new Staff {\n\t\\time 2/8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"
   '''
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
   
def test_metricgrid_02( ):
   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t, [(3, 16)])
   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n\tc'8\n}"
   '''
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

   
def test_metricgrid_03( ):
   '''MetricGrid cycles throught given meters to cover spanner's duration.''' 
   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t, [(1, 8), (1, 4)])
   assert t.format == "\\new Staff {\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n\tc'8\n\t\\time 1/8\n\tc'8\n\t\\time 1/4\n\tc'8\n}"

   '''
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

def test_metricgrid_04( ):
   '''MetricGrid knows how to draw itself in the middle of a note. '''
   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t, [(3, 16), (2, 8)])
   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\t<<\n\t{ s1 * 1/16 \\time 2/8 }\n\tc'8\n\t>>\n\tc'8\n\t<<\n\t{ s1 * 1/16 \\time 3/16 }\n\tc'8\n\t>>\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"
   '''
   \new Staff {
        \time 3/16
        c'8
        <<
        { s1 * 1/16 \time 2/8 }
        c'8
        >>
        c'8
        <<
        { s1 * 1/16 \time 3/16 }
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

def test_metricgrid_05( ):
   '''MetricGrid knows how to draw itself in the middle of a note. '''
   t = Staff(Note(0, (1,2)) * 2)
   m = MetricGrid(t, [(1, 8), (1, 4)])
   assert t.format == "\\new Staff {\n\t\\time 1/8\n\t<<\n\t{ s1 * 1/8 \\time 1/4 }\n\t{ s1 * 3/8 \\time 1/8 }\n\tc'2\n\t>>\n\t\\time 1/4\n\t<<\n\t{ s1 * 1/4 \\time 1/8 }\n\t{ s1 * 3/8 \\time 1/4 }\n\tc'2\n\t>>\n}"
   '''
   \new Staff {
           \time 1/8
           <<
           { s1 * 1/8 \time 1/4 }
           { s1 * 3/8 \time 1/8 }
           c'2
           >>
           \time 1/4
           <<
           { s1 * 1/4 \time 1/8 }
           { s1 * 3/8 \time 1/4 }
           c'2
           >>
   }
   '''


def test_metricgrid_10( ):
   '''MetricGrid splits notes on bar lines.'''
   t = Staff(Note(0, (1,8)) * 8)
   m = MetricGrid(t, [(3, 16)])
   m.splitOnBar( )
   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n\tc'8\n\tc'8\n\tc'16 ~\n\tc'16\n}"
   '''
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

def test_metricgrid_11( ):
   '''MetricGrid splits notes on bar lines.'''
   t = Staff(Note(0, (1,8))*8)
   m = MetricGrid(t, [(3, 16), (2, 8)])
   m.splitOnBar( )
   assert t.format == "\\new Staff {\n\t\\time 3/16\n\tc'8\n\tc'16 ~\n\t\\time 2/8\n\tc'16\n\tc'8\n\tc'16 ~\n\t\\time 3/16\n\tc'16\n\tc'8\n\t\\time 2/8\n\tc'8\n\tc'8\n\t\\time 3/16\n\tc'8\n}"
   '''
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

def test_metricgrid_12( ):
   '''MetricGrid split works with tuplets.'''
   t = Voice([FixedMultiplierTuplet((2,3), Note(0, (1,8)) * 6)])
   m = MetricGrid(t, [(1, 8)])
   m.splitOnBar( )
   '''MetricGrid splitOnBar works in Tuplets.'''   
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t\tc'8\n\t\tc'16 ~\n\t\tc'16\n\t\tc'8\n\t}\n}"
   '''
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

def test_metricgrid_13( ):
   '''MetricGrid split works with nested tuplets.'''
   t = Voice([FixedMultiplierTuplet((2,3), [Note(0, (1,8)), 
         FixedMultiplierTuplet((3,2), Note(0, (1,8)) *4)])])
   m = MetricGrid(t, [(1, 8)])
   m.splitOnBar( )
   assert t.format =="\\new Voice {\n\t\\times 2/3 {\n\t\t\\time 1/8\n\t\tc'8\n\t\t\\fraction \\times 3/2 {\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'16 ~\n\t\t\t}\n\t\t\t\\times 2/3 {\n\t\t\t\tc'8\n\t\t\t}\n\t\t}\n\t}\n}"
   '''
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
