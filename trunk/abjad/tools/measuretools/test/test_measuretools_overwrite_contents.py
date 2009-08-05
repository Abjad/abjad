from abjad import *
import py.test


def test_measuretools_overwrite_contents_01( ):
   '''Contents duration less than sum of duration of measures.
   Note spacer skip at end of second measure.
   '''

   t = Staff(measuretools.make([(1, 8), (3, 16)]))

   r'''
   \new Staff {
           {
                   \time 1/8
                   s1 * 1/8
           }
           {
                   \time 3/16
                   s1 * 3/16
           }
   }
   '''

   notes = construct.scale(4, Rational(1, 16)) 
   measuretools.overwrite_contents(t, notes)

   r'''
   \new Staff {
           {
                   \time 1/8
                   c'16
                   d'16
           }
           {
                   \time 3/16
                   e'16
                   f'16
                   s1 * 1/16
           }
   }
   '''
   
   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'16\n\t\td'16\n\t}\n\t{\n\t\t\\time 3/16\n\t\te'16\n\t\tf'16\n\t\ts1 * 1/16\n\t}\n}"


def test_measuretools_overwrite_contents_02( ):
   '''Some contents too big for some measures.
   Small measures skipped.
   '''

   t = Staff(measuretools.make([(1, 16), (3, 16), (1, 16), (3, 16)]))

   r'''
   \new Staff {
           {
                   \time 1/16
                   s1 * 1/16
           }
           {
                   \time 3/16
                   s1 * 3/16
           }
           {
                   \time 1/16
                   s1 * 1/16
           }
           {
                   \time 3/16
                   s1 * 3/16
           }
   }
   '''

   notes = construct.scale(2)
   measuretools.overwrite_contents(t, notes)   

   r'''
   \new Staff {
           {
                   \time 1/16
                   s1 * 1/16
           }
           {
                   \time 3/16
                   c'8
                   s1 * 1/16
           }
           {
                   \time 1/16
                   s1 * 1/16
           }
           {
                   \time 3/16
                   d'8
                   s1 * 1/16
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/16\n\t\ts1 * 1/16\n\t}\n\t{\n\t\t\\time 3/16\n\t\tc'8\n\t\ts1 * 1/16\n\t}\n\t{\n\t\t\\time 1/16\n\t\ts1 * 1/16\n\t}\n\t{\n\t\t\\time 3/16\n\t\td'8\n\t\ts1 * 1/16\n\t}\n}"


def test_measuretools_overwrite_contents_03( ):
   '''Raise MissingMeasureError when input expression 
   contains no measures.'''

   t = Note(0, (1, 4))
   notes = construct.scale(2)

   assert py.test.raises(MissingMeasureError, 
      'measuretools.overwrite_contents(t, notes)')


def test_measuretools_overwrite_contents_04( ):
   '''Raise StopIteration when not enough measures.'''

   t = Staff(measuretools.make([(1, 8), (1, 8)]))
   notes = construct.scale(6, Rational(1, 16))

   assert py.test.raises(StopIteration, 
      'measuretools.overwrite_contents(t, notes)')


def test_measuretools_overwrite_contents_05( ):
   '''Populate measures even when not enough total measures.'''

   t = Staff(measuretools.make([(1, 8), (1, 8)]))
   notes = construct.scale(6, Rational(1, 16))

   try:
      measuretools.overwrite_contents(t, notes)
   except StopIteration:
      pass

   r'''
   \new Staff {
           {
                   \time 1/8
                   c'16
                   d'16
           }
           {
                   \time 1/8
                   e'16
                   f'16
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 1/8\n\t\tc'16\n\t\td'16\n\t}\n\t{\n\t\t\\time 1/8\n\t\te'16\n\t\tf'16\n\t}\n}" 
