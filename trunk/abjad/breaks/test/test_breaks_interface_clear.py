from abjad import *


def test_breaks_interface_clear_01( ):
   '''Set line, page, x and y to None.'''

   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True
   t.breaks.x = 20
   t.breaks.y = 40

   r'''\overrideProperty #"Score.NonMusicalPaperColumn"
   #'line-break-system-details
   #'((X-offset . 20) (Y-offset . 40))
   c'4
   \break
   \pageBreak'''

   t.breaks.clear( )

   "c'4"

   assert check.wf(t)
   assert t.format == "c'4"
