from abjad import *
import py.test
py.test.skip('fix me.')


def test_layouttools_set_line_breaks_cyclically_by_line_duration_in_seconds_ge_01( ):
   '''Iterate klass instances in expr and accumulate duration in seconds.
   Add line break after every total less than or equal to line_duration.'''

   t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 4)
   macros.diatonicize(t)
   marktools.TempoMark(Fraction(1, 8), 44)(t)

   r'''
   \new Staff {
           {
                   \time 2/8
                   \tempo 8=44
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
           {
                   \time 2/8
                   b'8
                   c''8
                   %% tempo 8=44 ends here
           }
   }
   '''

   layouttools.set_line_breaks_cyclically_by_line_duration_in_seconds_ge(t, Fraction(6))

   r'''
   \new Staff {
           {
                   \time 2/8
                   \tempo 8=44
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
                   \break
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
           {
                   \time 2/8
                   b'8
                   c''8
           }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\tempo 8=44\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t\t\\break\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tb'8\n\t\tc''8\n\t}\n}"
