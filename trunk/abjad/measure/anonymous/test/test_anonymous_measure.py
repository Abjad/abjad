from abjad import *


def test_anonymous_measure_01( ):
   '''
   Anonymous measures dynamically adjust to the size of contents.
   Anonymous measures print no meter.
   '''

   t = AnonymousMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   
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

   assert t.meter.change == False
   assert t.meter.effective == Meter(1, 2)
   assert t.meter.forced is None

   assert t.format == "{\n\t\\override Staff.TimeSignature #'stencil = ##f\n\t\\time 1/2\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\revert Staff.TimeSignature #'stencil\n}"


def test_anonymous_measure_02( ):
   '''
   Anonymous measures dynamically adjust to contents size.
   Anonymous measures print no meter.
   '''

   t = AnonymousMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   
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

   assert t.meter.change == False
   assert t.meter.effective == Meter(3, 8)
   assert t.meter.forced is None
