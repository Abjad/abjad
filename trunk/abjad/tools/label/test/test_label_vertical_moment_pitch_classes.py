from abjad import *


def test_label_vertical_moment_pitch_classes_01( ):

   score = Score(Staff([ ]) * 3)
   score[0].extend(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   score[1].clef.forced = Clef('alto')
   score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
   score[2].clef.forced = Clef('bass')
   score[2].append(Note(-24, (1, 2)))
   label.vertical_moment_pitch_classes(score)

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8 _ \markup { \small { \column { 7 2 0 } } }
                   e'8
                   f'8 _ \markup { \small { \column { 5 0 } } }
           }
           \new Staff {
                   \clef "alto"
                   g4
                   f4 _ \markup { \small { \column { 5 4 0 } } }
           }
           \new Staff {
                   \clef "bass"
                   c,2 _ \markup { \small { \column { 7 0 } } }
           }
   >>
   '''

   assert componenttools.is_well_formed_component(score)
   assert score.format == '\\new Score <<\n\t\\new Staff {\n\t\tc\'8\n\t\td\'8 _ \\markup { \\small { \\column { 7 2 0 } } }\n\t\te\'8\n\t\tf\'8 _ \\markup { \\small { \\column { 5 0 } } }\n\t}\n\t\\new Staff {\n\t\t\\clef "alto"\n\t\tg4\n\t\tf4 _ \\markup { \\small { \\column { 5 4 0 } } }\n\t}\n\t\\new Staff {\n\t\t\\clef "bass"\n\t\tc,2 _ \\markup { \\small { \\column { 7 0 } } }\n\t}\n>>'
