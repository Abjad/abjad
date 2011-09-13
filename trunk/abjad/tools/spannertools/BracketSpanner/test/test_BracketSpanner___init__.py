from abjad import *


def test_BracketSpanner___init___01():
    '''Init empty bracket spanner.
    '''

    bracket = spannertools.BracketSpanner()
    assert isinstance(bracket, spannertools.BracketSpanner)


def test_BracketSpanner___init___02():
    '''Bracket defaults to solid red line with left and right nibs
    and with no nibs at left and right broken edges.
    '''

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    spannertools.BracketSpanner(t[1])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8
            d'8
        }
        {
            \time 2/8
            \override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))
            \override TextSpanner #'bound-details #'left-broken #'text = ##f
            \override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))
            \override TextSpanner #'bound-details #'right-broken #'text = ##f
            \override TextSpanner #'color = #red
            \override TextSpanner #'dash-fraction = #1
            \override TextSpanner #'staff-padding = #2
            \override TextSpanner #'thickness = #1.5
            e'8 \startTextSpan
            f'8 \stopTextSpan
            \revert TextSpanner #'bound-details #'left #'text
            \revert TextSpanner #'bound-details #'left-broken #'text
            \revert TextSpanner #'bound-details #'right #'text
            \revert TextSpanner #'bound-details #'right-broken #'text
            \revert TextSpanner #'color
            \revert TextSpanner #'dash-fraction
            \revert TextSpanner #'staff-padding
            \revert TextSpanner #'thickness
        }
        {
            \time 2/8
            g'8
            a'8
        }
    }
    '''

    assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\t\\override TextSpanner #'bound-details #'left #'text = #(markup #:draw-line '(0 . -1))\n\t\t\\override TextSpanner #'bound-details #'left-broken #'text = ##f\n\t\t\\override TextSpanner #'bound-details #'right #'text = #(markup #:draw-line '(0 . -1))\n\t\t\\override TextSpanner #'bound-details #'right-broken #'text = ##f\n\t\t\\override TextSpanner #'color = #red\n\t\t\\override TextSpanner #'dash-fraction = #1\n\t\t\\override TextSpanner #'staff-padding = #2\n\t\t\\override TextSpanner #'thickness = #1.5\n\t\te'8 \\startTextSpan\n\t\tf'8 \\stopTextSpan\n\t\t\\revert TextSpanner #'bound-details #'left #'text\n\t\t\\revert TextSpanner #'bound-details #'left-broken #'text\n\t\t\\revert TextSpanner #'bound-details #'right #'text\n\t\t\\revert TextSpanner #'bound-details #'right-broken #'text\n\t\t\\revert TextSpanner #'color\n\t\t\\revert TextSpanner #'dash-fraction\n\t\t\\revert TextSpanner #'staff-padding\n\t\t\\revert TextSpanner #'thickness\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"
