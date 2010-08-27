from abjad import *
import py.test


def test_AnonymousMeasure_01( ):
   '''Anonymous measures dynamically adjust to the size of contents.
   Anonymous measures print no meter.
   '''
   py.test.skip('simplify update produres to fix dynamic measure effective meter.')

   t = measuretools.AnonymousMeasure(macros.scale(4))
   
   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 1/2
           c'8
           d'8
           e'8
           f'8
           \revert Staff.TimeSignature #'stencil
   }
   '''

   #assert t.meter.change == False
   #assert t.meter.effective == metertools.Meter(1, 2)
   assert t.meter.effective == marktools.TimeSignatureMark(1, 2)
   #assert t.meter.forced is None

   assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/2\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_AnonymousMeasure_02( ):
   '''
   Anonymous measures dynamically adjust to contents size.
   Anonymous measures print no meter.
   '''

   t = measuretools.AnonymousMeasure(macros.scale(3))
   
   r'''
   {
           \override Staff.TimeSignature #'stencil = ##f
           \time 3/8
           c'8
           d'8
           e'8
           \revert Staff.TimeSignature #'stencil
   }
   '''

   assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 3/8\n\tc'8\n\td'8\n\te'8\n\t\\revert Staff.TimeSignature #'stencil\n}"

   #assert t.meter.change == False
   #assert t.meter.effective == metertools.Meter(3, 8)
   assert t.meter.effective == marktools.TimeSignatureMark(3, 8)
   #assert t.meter.forced is None
