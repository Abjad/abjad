from abjad import *


def test_suppress_01( ):
   '''Suppress binary meter at format-time.'''

   t = Measure((7, 8), scale(7))
   t.meter.effective.suppress = True

   r'''
        c'8
        d'8
        e'8
        f'8
        g'8
        a'8
        b'8
   '''

   assert t.format == "\tc'8\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8"


def test_suppress_02( ):
   '''Suppress nonbinary meter at format-time.'''

   t = Measure((8, 9), scale(8))
   t.meter.effective.suppress = True

   r'''
        \scaleDurations #'(8 . 9) {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
        }
   '''

   assert t.format == "\t\\scaleDurations #'(8 . 9) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t\tf'8\n\t\tg'8\n\t\ta'8\n\t\tb'8\n\t\tc''8\n\t}"
