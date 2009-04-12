from abjad import *


def test_bracket_defaults_01( ):
   '''Bracket defaults to solid red line with left and right nibs.'''

   t = Staff(measures_make([(2, 16), (3, 16), (5, 16)]))
   measures_populate(t, Rational(1, 16))
   Bracket(t[0])
   Bracket(t[1])
   Bracket(t[2])

   r'''
   \new Staff {
                   \time 2/16
                   \override TextSpanner #'dash-fraction = #1
                   \override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))
                   \override TextSpanner #'staff-padding = #2
                   \override TextSpanner #'color = #red
                   \override TextSpanner #'thickness = #1.5
                   \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
                   c'16 \startTextSpan
                   c'16 \stopTextSpan
                   \revert TextSpanner #'dash-fraction
                   \revert TextSpanner #'bound-details #'left #'text
                   \revert TextSpanner #'staff-padding
                   \revert TextSpanner #'color
                   \revert TextSpanner #'thickness
                   \revert TextSpanner #'bound-details #'right #'text
                   \time 3/16
                   \override TextSpanner #'dash-fraction = #1
                   \override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))
                   \override TextSpanner #'staff-padding = #2
                   \override TextSpanner #'color = #red
                   \override TextSpanner #'thickness = #1.5
                   \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
                   c'16 \startTextSpan
                   c'16
                   c'16 \stopTextSpan
                   \revert TextSpanner #'dash-fraction
                   \revert TextSpanner #'bound-details #'left #'text
                   \revert TextSpanner #'staff-padding
                   \revert TextSpanner #'color
                   \revert TextSpanner #'thickness
                   \revert TextSpanner #'bound-details #'right #'text
                   \time 5/16
                   \override TextSpanner #'dash-fraction = #1
                   \override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))
                   \override TextSpanner #'staff-padding = #2
                   \override TextSpanner #'color = #red
                   \override TextSpanner #'thickness = #1.5
                   \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
                   c'16 \startTextSpan
                   c'16
                   c'16
                   c'16
                   c'16 \stopTextSpan
                   \revert TextSpanner #'dash-fraction
                   \revert TextSpanner #'bound-details #'left #'text
                   \revert TextSpanner #'staff-padding
                   \revert TextSpanner #'color
                   \revert TextSpanner #'thickness
                   \revert TextSpanner #'bound-details #'right #'text
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\t\\time 2/16\n\t\t\\override TextSpanner #'dash-fraction = #1\n\t\t\\override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))\n\t\t\\override TextSpanner #'staff-padding = #2\n\t\t\\override TextSpanner #'color = #red\n\t\t\\override TextSpanner #'thickness = #1.5\n\t\t\\override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))\n\t\tc'16 \\startTextSpan\n\t\tc'16 \\stopTextSpan\n\t\t\\revert TextSpanner #'dash-fraction\n\t\t\\revert TextSpanner #'bound-details #'left #'text\n\t\t\\revert TextSpanner #'staff-padding\n\t\t\\revert TextSpanner #'color\n\t\t\\revert TextSpanner #'thickness\n\t\t\\revert TextSpanner #'bound-details #'right #'text\n\t\t\\time 3/16\n\t\t\\override TextSpanner #'dash-fraction = #1\n\t\t\\override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))\n\t\t\\override TextSpanner #'staff-padding = #2\n\t\t\\override TextSpanner #'color = #red\n\t\t\\override TextSpanner #'thickness = #1.5\n\t\t\\override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))\n\t\tc'16 \\startTextSpan\n\t\tc'16\n\t\tc'16 \\stopTextSpan\n\t\t\\revert TextSpanner #'dash-fraction\n\t\t\\revert TextSpanner #'bound-details #'left #'text\n\t\t\\revert TextSpanner #'staff-padding\n\t\t\\revert TextSpanner #'color\n\t\t\\revert TextSpanner #'thickness\n\t\t\\revert TextSpanner #'bound-details #'right #'text\n\t\t\\time 5/16\n\t\t\\override TextSpanner #'dash-fraction = #1\n\t\t\\override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))\n\t\t\\override TextSpanner #'staff-padding = #2\n\t\t\\override TextSpanner #'color = #red\n\t\t\\override TextSpanner #'thickness = #1.5\n\t\t\\override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))\n\t\tc'16 \\startTextSpan\n\t\tc'16\n\t\tc'16\n\t\tc'16\n\t\tc'16 \\stopTextSpan\n\t\t\\revert TextSpanner #'dash-fraction\n\t\t\\revert TextSpanner #'bound-details #'left #'text\n\t\t\\revert TextSpanner #'staff-padding\n\t\t\\revert TextSpanner #'color\n\t\t\\revert TextSpanner #'thickness\n\t\t\\revert TextSpanner #'bound-details #'right #'text\n}"
