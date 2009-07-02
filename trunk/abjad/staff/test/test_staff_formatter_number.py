from abjad import *
import py.test

py.test.skip('measure redo')


def test_staff_formatter_number_01( ):
   '''Staff formatter number interface can contribute
      LilyPond comments to many measures at once.'''

   t = Staff(measuretools.make([(2, 16), (3, 16), (3, 16)]))
   measuretools.populate(t, Rational(1, 16))
   t.formatter.number.measures = 'comment'

   r'''\new Staff {
           % start measure 1
                   \time 2/16
                   c'16
                   c'16
           % stop measure 1
           % start measure 2
                   \time 3/16
                   c'16
                   c'16
                   c'16
           % stop measure 2
           % start measure 3
                   \time 3/16
                   c'16
                   c'16
                   c'16
           % stop measure 3
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t% start measure 1\n\t\t\\time 2/16\n\t\tc'16\n\t\tc'16\n\t% stop measure 1\n\t% start measure 2\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t% stop measure 2\n\t% start measure 3\n\t\t\\time 3/16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t% stop measure 3\n}"


def test_staff_formatter_number_02( ):
   '''Staff formatter number interface can contribute
      markup to many leaves at once.'''

   t = Staff(measuretools.make([(2, 16), (3, 16), (3, 16)]))
   measuretools.populate(t, Rational(1, 16))
   t.formatter.number.leaves = 'markup'

   r'''\new Staff {
                   \time 2/16
                   c'16 ^ \markup { 0 }
                   c'16 ^ \markup { 1 }
                   \time 3/16
                   c'16 ^ \markup { 2 }
                   c'16 ^ \markup { 3 }
                   c'16 ^ \markup { 4 }
                   \time 3/16
                   c'16 ^ \markup { 5 }
                   c'16 ^ \markup { 6 }
                   c'16 ^ \markup { 7 }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/16\n\t\tc'16 ^ \\markup { 0 }\n\t\tc'16 ^ \\markup { 1 }\n\t\t\\time 3/16\n\t\tc'16 ^ \\markup { 2 }\n\t\tc'16 ^ \\markup { 3 }\n\t\tc'16 ^ \\markup { 4 }\n\t\t\\time 3/16\n\t\tc'16 ^ \\markup { 5 }\n\t\tc'16 ^ \\markup { 6 }\n\t\tc'16 ^ \\markup { 7 }\n}"


def test_staff_formatter_number_03( ):
   '''Staff formatter number interface can contribute
      both measure comments and leaf markup at format-time.'''

   t = Staff(measuretools.make([(2, 16), (3, 16), (3, 16)]))
   measuretools.populate(t, Rational(1, 16))
   t.formatter.number.measures = 'comment'
   t.formatter.number.leaves = 'markup'

   r'''\new Staff {
           % start measure 1
                   \time 2/16
                   c'16 ^ \markup { 0 }
                   c'16 ^ \markup { 1 }
           % stop measure 1
           % start measure 2
                   \time 3/16
                   c'16 ^ \markup { 2 }
                   c'16 ^ \markup { 3 }
                   c'16 ^ \markup { 4 }
           % stop measure 2
           % start measure 3
                   \time 3/16
                   c'16 ^ \markup { 5 }
                   c'16 ^ \markup { 6 }
                   c'16 ^ \markup { 7 }
           % stop measure 3
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t% start measure 1\n\t\t\\time 2/16\n\t\tc'16 ^ \\markup { 0 }\n\t\tc'16 ^ \\markup { 1 }\n\t% stop measure 1\n\t% start measure 2\n\t\t\\time 3/16\n\t\tc'16 ^ \\markup { 2 }\n\t\tc'16 ^ \\markup { 3 }\n\t\tc'16 ^ \\markup { 4 }\n\t% stop measure 2\n\t% start measure 3\n\t\t\\time 3/16\n\t\tc'16 ^ \\markup { 5 }\n\t\tc'16 ^ \\markup { 6 }\n\t\tc'16 ^ \\markup { 7 }\n\t% stop measure 3\n}"
