from abjad import *


def test_spannertools_make_solid_text_spanner_above_with_nib_at_right_01():

    t = Staff("c'8 d'8 e'8 f'8")
    spannertools.make_solid_text_spanner_above_with_nib_at_right('foo', t[:])

    r'''
    \new Staff {
        \override TextSpanner #'bound-details #'left #'text = \markup { foo }
        \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
        \override TextSpanner #'bound-details #'right-broken #'text = ##f
        \override TextSpanner #'dash-fraction = #1
        \override TextSpanner #'direction = #up
        c'8 \startTextSpan
        d'8
        e'8
        f'8 \stopTextSpan
        \revert TextSpanner #'bound-details #'left #'text
        \revert TextSpanner #'bound-details #'right #'text
        \revert TextSpanner #'bound-details #'right-broken #'text
        \revert TextSpanner #'dash-fraction
        \revert TextSpanner #'direction
    }
    '''

    assert t.format == "\\new Staff {\n\t\\override TextSpanner #'bound-details #'left #'text = \\markup { foo }\n\t\\override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))\n\t\\override TextSpanner #'bound-details #'right-broken #'text = ##f\n\t\\override TextSpanner #'dash-fraction = #1\n\t\\override TextSpanner #'direction = #up\n\tc'8 \\startTextSpan\n\td'8\n\te'8\n\tf'8 \\stopTextSpan\n\t\\revert TextSpanner #'bound-details #'left #'text\n\t\\revert TextSpanner #'bound-details #'right #'text\n\t\\revert TextSpanner #'bound-details #'right-broken #'text\n\t\\revert TextSpanner #'dash-fraction\n\t\\revert TextSpanner #'direction\n}"
