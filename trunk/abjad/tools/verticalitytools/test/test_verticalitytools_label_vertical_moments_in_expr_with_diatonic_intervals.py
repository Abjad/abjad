from abjad import *


def test_verticalitytools_label_vertical_moments_in_expr_with_diatonic_intervals_01( ):

   score = Score(Staff([ ]) * 3)
   score[0].extend(macros.scale(4))
   #score[1].clef.forced = stafftools.Clef('alto')
   marktools.ClefMark('alto')(score[1])
   score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
   #score[2].clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('bass')(score[2])
   score[2].append(Note(-24, (1, 2)))
   verticalitytools.label_vertical_moments_in_expr_with_diatonic_intervals(score)

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8 _ \markup { \small { \column { 16 12 } } }
                   e'8
                   f'8 _ \markup { \small { \column { 18 11 } } }
           }
           \new Staff {
                   \clef "alto"
                   g4
                   f4 _ \markup { \small { \column { 17 11 } } }
           }
           \new Staff {
                   \clef "bass"
                   c,2 _ \markup { \small { \column { 15 12 } } }
           }
   >>
   '''

   assert componenttools.is_well_formed_component(score)
   assert score.format == '\\new Score <<\n\t\\new Staff {\n\t\tc\'8\n\t\td\'8 _ \\markup { \\small { \\column { 16 12 } } }\n\t\te\'8\n\t\tf\'8 _ \\markup { \\small { \\column { 18 11 } } }\n\t}\n\t\\new Staff {\n\t\t\\clef "alto"\n\t\tg4\n\t\tf4 _ \\markup { \\small { \\column { 17 11 } } }\n\t}\n\t\\new Staff {\n\t\t\\clef "bass"\n\t\tc,2 _ \\markup { \\small { \\column { 15 12 } } }\n\t}\n>>'
