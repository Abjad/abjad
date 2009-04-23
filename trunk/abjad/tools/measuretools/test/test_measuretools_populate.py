from abjad import *


def test_measuretools_populate_01( ):
   '''Populate nonbinary measure with note train.'''

   t = RigidMeasure((5, 18), [ ])
   measuretools.populate(t, Rational(1, 16))

   r'''\time 5/18
       \scaleDurations #'(8 . 9) {
         c'16
         c'16
         c'16
         c'16
         c'16
    }'''

   assert check.wf(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}"


def test_measuretools_populate_02( ):
   '''Populate nonbinary measure with big-endian tie chain.'''

   t = RigidMeasure((5, 18), [ ])
   measuretools.populate(t, 'big-endian')

   r'''\time 5/18
      \scaleDurations #'(8 . 9) {
         c'4 ~
         c'16
      }'''

   assert check.wf(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'4 ~\n\t\tc'16\n\t}"


def test_measuretools_populate_03( ):
   '''Populate nonbinary measure with little-endian tie chain.'''

   t = RigidMeasure((5, 18), [ ])
   measuretools.populate(t, 'little-endian')

   r'''\time 5/18
      \scaleDurations #'(8 . 9) {
         c'16 ~
         c'4
      }'''

   assert check.wf(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16 ~\n\t\tc'4\n\t}"


def test_measuretools_populate_04( ):
   '''Populate nonbinary measure with time-scaled skip.'''

   t = RigidMeasure((5, 18), [ ])
   measuretools.populate(t, 'skip')

   r'''\time 5/18
      \scaleDurations #'(8 . 9) {
         s1 * 5/16
      }'''
   
   assert check.wf(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\ts1 * 5/16\n\t}"


def test_measuretools_populate_05( ):
   '''Populate nonbinary measure with meter series.'''

   t = RigidMeasure((5, 18), [ ])
   measuretools.populate(t, 'meter series')

   r'''\time 5/18
      \scaleDurations #'(8 . 9) {
         c'16
         c'16
         c'16
         c'16
         c'16
      }'''

   assert check.wf(t)
   assert t.format == "\t\\time 5/18\n\t\\scaleDurations #'(8 . 9) {\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t}"


def test_measuretools_populate_06( ):
   '''Populate measures conditionally.
      Iteration control tests index of iteration.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 4)
   pitchtools.diatonicize(t)

   r'''\new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 2/8
                   e'8
                   f'8
                   \time 2/8
                   g'8
                   a'8
                   \time 2/8
                   b'8
                   c''8
   }'''

   def iterctrl(measure, i):
      return i % 2 == 1
      
   measuretools.populate(t, 'skip', iterctrl)

   r'''\new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 2/8
                   s1 * 1/4
                   \time 2/8
                   g'8
                   a'8
                   \time 2/8
                   s1 * 1/4
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t\t\\time 2/8\n\t\ts1 * 1/4\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t\t\\time 2/8\n\t\ts1 * 1/4\n}"


def test_measuretools_populate_07( ):
   '''Populate measures conditionally.
      Iteration control tests measure length.'''

   t = Staff([RigidMeasure((n, 8), construct.scale(n)) for n in (2, 3, 4)])

   r'''\new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 3/8
                   c'8
                   d'8
                   e'8
                   \time 4/8
                   c'8
                   d'8
                   e'8
                   f'8
   }'''

   measuretools.populate(t, 'skip', lambda m, i: 2 < len(m))

   r'''\new Staff {
                   \time 2/8
                   c'8
                   d'8
                   \time 3/8
                   s1 * 3/8
                   \time 4/8
                   s1 * 1/2
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t\t\\time 3/8\n\t\ts1 * 3/8\n\t\t\\time 4/8\n\t\ts1 * 1/2\n}"
