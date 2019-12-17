from abjad.system.Tag import Tag

from .ScoreTemplate import ScoreTemplate


class StringOrchestraScoreTemplate(ScoreTemplate):
    r"""
    String orchestra score template.

    ..  container:: example

        >>> template = abjad.StringOrchestraScoreTemplate()
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=89)
        \context Score = "Score"                                                                 %! abjad.StringOrchestraScoreTemplate.__call__()
        <<                                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()
            \tag #'(Violin_1 Violin_2 Violin_3 Violin_4 Violin_5 Violin_6 Viola_1 Viola_2 Viola_3 Viola_4 Cello_1 Cello_2 Cello_3 Contrabass_1 Contrabass_2) %! abjad.StringOrchestraScoreTemplate.__call__()
            \context GlobalContext = "Global_Context"                                            %! abjad.StringOrchestraScoreTemplate.__call__()
            {                                                                                    %! abjad.StringOrchestraScoreTemplate.__call__()
            }                                                                                    %! abjad.StringOrchestraScoreTemplate.__call__()
            \context StaffGroup = "Outer_Staff_Group"                                            %! abjad.StringOrchestraScoreTemplate.__call__()
            <<                                                                                   %! abjad.StringOrchestraScoreTemplate.__call__()
                \context ViolinStaffGroup = "Violin_Staff_Group"                                 %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Violin_1                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_1_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_1_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_1_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_1_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_1_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Violin_2                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_2_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_2_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_2_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_2_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_2_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Violin_3                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_3_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_3_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_3_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_3_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_3_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Violin_4                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_4_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_4_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_4_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_4_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_4_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Violin_5                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_5_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_5_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_5_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_5_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_5_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Violin_6                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_6_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_6_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_6_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_6_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_6_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                \context ViolaStaffGroup = "Viola_Staff_Group"                                   %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Viola_1                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Viola_1_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Viola_1_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Viola_1_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Viola_1_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Viola_1_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "alto"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Viola_2                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Viola_2_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Viola_2_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Viola_2_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Viola_2_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Viola_2_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "alto"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Viola_3                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Viola_3_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Viola_3_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Viola_3_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Viola_3_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Viola_3_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "alto"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Viola_4                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Viola_4_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Viola_4_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Viola_4_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Viola_4_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Viola_4_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "alto"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                \context CelloStaffGroup = "Cello_Staff_Group"                                   %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Cello_1                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Cello_1_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Cello_1_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Cello_1_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Cello_1_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Cello_1_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Cello_2                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Cello_2_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Cello_2_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Cello_2_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Cello_2_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Cello_2_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Cello_3                                                               %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Cello_3_Staff_Group"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Cello_3_Bowing_Staff"                            %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Cello_3_Bowing_Voice"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Cello_3_Fingering_Staff"                      %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Cello_3_Fingering_Voice"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                \context ContrabassStaffGroup = "Contrabass_Staff_Group"                         %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Contrabass_1                                                          %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Contrabass_1_Staff_Group"              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Contrabass_1_Bowing_Staff"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Contrabass_1_Bowing_Voice"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Contrabass_1_Fingering_Staff"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Contrabass_1_Fingering_Voice"             %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass_8"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Contrabass_2                                                          %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Contrabass_2_Staff_Group"              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Contrabass_2_Bowing_Staff"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Contrabass_2_Bowing_Voice"                   %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Contrabass_2_Fingering_Staff"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Contrabass_2_Fingering_Voice"             %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass_8"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
            >>                                                                                   %! abjad.StringOrchestraScoreTemplate.__call__()
        >>                                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()

    ..  container:: example

        As a string quartet:

        >>> template = abjad.StringOrchestraScoreTemplate(
        ...     violin_count=2,
        ...     viola_count=1,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=89)
        \context Score = "Score"                                                                 %! abjad.StringOrchestraScoreTemplate.__call__()
        <<                                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()
            \tag #'(Violin_1 Violin_2 Viola Cello)                                               %! abjad.StringOrchestraScoreTemplate.__call__()
            \context GlobalContext = "Global_Context"                                            %! abjad.StringOrchestraScoreTemplate.__call__()
            {                                                                                    %! abjad.StringOrchestraScoreTemplate.__call__()
            }                                                                                    %! abjad.StringOrchestraScoreTemplate.__call__()
            \context StaffGroup = "Outer_Staff_Group"                                            %! abjad.StringOrchestraScoreTemplate.__call__()
            <<                                                                                   %! abjad.StringOrchestraScoreTemplate.__call__()
                \context ViolinStaffGroup = "Violin_Staff_Group"                                 %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Violin_1                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_1_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_1_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_1_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_1_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_1_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \tag #'Violin_2                                                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Violin_2_Staff_Group"                  %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Violin_2_Bowing_Staff"                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Violin_2_Bowing_Voice"                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Violin_2_Fingering_Staff"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Violin_2_Fingering_Voice"                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                \context ViolaStaffGroup = "Viola_Staff_Group"                                   %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Viola                                                                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Viola_Staff_Group"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Viola_Bowing_Staff"                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Viola_Bowing_Voice"                          %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Viola_Fingering_Staff"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Viola_Fingering_Voice"                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "alto"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                \context CelloStaffGroup = "Cello_Staff_Group"                                   %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Cello                                                                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Cello_Staff_Group"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Cello_Bowing_Staff"                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Cello_Bowing_Voice"                          %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Cello_Fingering_Staff"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Cello_Fingering_Voice"                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
            >>                                                                                   %! abjad.StringOrchestraScoreTemplate.__call__()
        >>                                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()

    ..  container:: example

        As a cello solo:

        >>> template = abjad.StringOrchestraScoreTemplate(
        ...     violin_count=0,
        ...     viola_count=0,
        ...     cello_count=1,
        ...     contrabass_count=0,
        ...     )
        >>> abjad.show(template) # doctest: +SKIP

        >>> abjad.f(template.__illustrate__()[abjad.Score], strict=89)
        \context Score = "Score"                                                                 %! abjad.StringOrchestraScoreTemplate.__call__()
        <<                                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()
            \tag #'(Cello)                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()
            \context GlobalContext = "Global_Context"                                            %! abjad.StringOrchestraScoreTemplate.__call__()
            {                                                                                    %! abjad.StringOrchestraScoreTemplate.__call__()
            }                                                                                    %! abjad.StringOrchestraScoreTemplate.__call__()
            \context StaffGroup = "Outer_Staff_Group"                                            %! abjad.StringOrchestraScoreTemplate.__call__()
            <<                                                                                   %! abjad.StringOrchestraScoreTemplate.__call__()
                \context CelloStaffGroup = "Cello_Staff_Group"                                   %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                <<                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
                    \tag #'Cello                                                                 %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    \context StringPerformerStaffGroup = "Cello_Staff_Group"                     %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    <<                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context BowingStaff = "Cello_Bowing_Staff"                              %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context BowingVoice = "Cello_Bowing_Voice"                          %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        \context FingeringStaff = "Cello_Fingering_Staff"                        %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        <<                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            \context FingeringVoice = "Cello_Fingering_Voice"                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                            {                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                                \clef "bass"                                                     %! abjad.ScoreTemplate.attach_defaults(3)
                                s1                                                               %! abjad.ScoreTemplate.__illustrate__()
                            }                                                                    %! StringOrchestraScoreTemplate._make_performer_staff_group()
                        >>                                                                       %! StringOrchestraScoreTemplate._make_performer_staff_group()
                    >>                                                                           %! StringOrchestraScoreTemplate._make_performer_staff_group()
                >>                                                                               %! abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()
            >>                                                                                   %! abjad.StringOrchestraScoreTemplate.__call__()
        >>                                                                                       %! abjad.StringOrchestraScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_cello_count",
        "_contrabass_count",
        "_split_hands",
        "_use_percussion_clefs",
        "_viola_count",
        "_violin_count",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        violin_count=6,
        viola_count=4,
        cello_count=3,
        contrabass_count=2,
        split_hands=True,
        use_percussion_clefs=False,
    ):
        assert 0 <= violin_count
        assert 0 <= viola_count
        assert 0 <= cello_count
        assert 0 <= contrabass_count
        super().__init__()
        self._violin_count = int(violin_count)
        self._viola_count = int(viola_count)
        self._cello_count = int(cello_count)
        self._contrabass_count = int(contrabass_count)
        self._split_hands = bool(split_hands)
        self._use_percussion_clefs = bool(use_percussion_clefs)

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls string orchestra template.

        Returns score.
        """
        import abjad

        site = "abjad.StringOrchestraScoreTemplate.__call__()"
        tag = Tag(site)

        ### TAGS ###

        tag_names = []

        ### SCORE ###

        staff_group = abjad.StaffGroup(name="Outer_Staff_Group", tag=tag)

        score = abjad.Score([staff_group], name="Score", tag=tag)

        ### VIOLINS ###

        if self.violin_count:
            clef_name = "treble"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = abjad.Violin()
            instrument_count = self.violin_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name, count=instrument_count, instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### VIOLAS ###

        if self.viola_count:
            clef_name = "alto"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = abjad.Viola()
            instrument_count = self.viola_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name, count=instrument_count, instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### CELLOS ###

        if self.cello_count:
            clef_name = "bass"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = abjad.Cello()
            instrument_count = self.cello_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name, count=instrument_count, instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### BASSES ###

        if self.contrabass_count:
            clef_name = "bass_8"
            if self.use_percussion_clefs:
                clef_name = "percussion"
            instrument = abjad.Contrabass()
            instrument_count = self.contrabass_count
            (
                instrument_staff_group,
                instrument_tag_names,
            ) = self._make_instrument_staff_group(
                clef_name=clef_name, count=instrument_count, instrument=instrument,
            )
            staff_group.append(instrument_staff_group)
            tag_names.extend(instrument_tag_names)

        ### TIME SIGNATURE CONTEXT ###

        global_context = abjad.Context(
            lilypond_type="GlobalContext", name="Global_Context", tag=tag
        )
        instrument_tags = " ".join(tag_names)
        tag_string = r"\tag #'({})".format(instrument_tags)
        literal = abjad.LilyPondLiteral(tag_string, "before")
        abjad.attach(literal, global_context, tag=tag)
        score.insert(0, global_context)
        return score

    ### PRIVATE METHODS ###

    def _make_instrument_staff_group(self, clef_name=None, count=None, instrument=None):
        import abjad

        site = "abjad.StringOrchestraScoreTemplate._make_instrument_staff_group()"
        tag = Tag(site)
        name = instrument.name.title()
        instrument_staff_group = abjad.StaffGroup(
            lilypond_type="{}StaffGroup".format(name),
            name="{}_Staff_Group".format(name),
            tag=tag,
        )
        tag_names = []
        if count == 1:
            performer_staff_group, tag_name = self._make_performer_staff_group(
                clef_name=clef_name, instrument=instrument, number=None
            )
            instrument_staff_group.append(performer_staff_group)
            tag_names.append(tag_name)
        else:
            for i in range(1, count + 1):
                performer_staff_group, tag_name = self._make_performer_staff_group(
                    clef_name=clef_name, instrument=instrument, number=i
                )
                instrument_staff_group.append(performer_staff_group)
                tag_names.append(tag_name)
        return instrument_staff_group, tag_names

    def _make_performer_staff_group(self, clef_name=None, instrument=None, number=None):
        import abjad

        site = "StringOrchestraScoreTemplate._make_performer_staff_group()"
        tag = Tag(site)
        if number is not None:
            name = "{}_{}".format(instrument.name.title(), number)
        else:
            name = instrument.name.title()
        pitch_range = instrument.pitch_range
        staff_group = abjad.StaffGroup(
            lilypond_type="StringPerformerStaffGroup",
            name="{}_Staff_Group".format(name),
            tag=tag,
        )
        tag_name = name.replace(" ", "")
        tag_string = r"\tag #'{}".format(tag_name)
        tag_command = abjad.LilyPondLiteral(tag_string, "before")
        abjad.attach(tag_command, staff_group, tag=tag)
        if self.split_hands:
            lh_voice = abjad.Voice(
                [],
                lilypond_type="FingeringVoice",
                name="{}_Fingering_Voice".format(name),
                tag=tag,
            )
            abbreviation = lh_voice.name.lower().replace(" ", "_")
            self.voice_abbreviations[abbreviation] = lh_voice.name
            lh_staff = abjad.Staff(
                [lh_voice],
                lilypond_type="FingeringStaff",
                name="{}_Fingering_Staff".format(name),
                tag=tag,
            )
            lh_staff.simultaneous = True
            abjad.annotate(lh_staff, "pitch_range", pitch_range)
            abjad.annotate(lh_staff, "default_clef", abjad.Clef(clef_name))
            rh_voice = abjad.Voice(
                [],
                lilypond_type="BowingVoice",
                name="{}_Bowing_Voice".format(name),
                tag=tag,
            )
            abbreviation = rh_voice.name.lower().replace(" ", "_")
            self.voice_abbreviations[abbreviation] = rh_voice.name
            rh_staff = abjad.Staff(
                [rh_voice],
                lilypond_type="BowingStaff",
                name="{}_Bowing_Staff".format(name),
                tag=tag,
            )
            rh_staff.simultaneous = True
            staff_group.extend([rh_staff, lh_staff])
        else:
            lh_voice = abjad.Voice(
                [],
                lilypond_type="FingeringVoice",
                name="{}_Voice".format(name),
                tag=tag,
            )
            lh_staff = abjad.Staff(
                [lh_voice],
                lilypond_type="FingeringStaff",
                name="{}_Staff".format(name),
                tag=tag,
            )
            lh_staff.simultaneous = True
            abjad.annotate(lh_staff, "pitch_range", pitch_range)
            abjad.annotate(lh_staff, "default_clef", abjad.Clef(clef_name))
            staff_group.append(lh_staff)
        return staff_group, tag_name

    ### PUBLIC PROPERTIES ###

    @property
    def cello_count(self):
        """
        Number of cellos in string orchestra.

        Returns nonnegative integer.
        """
        return self._cello_count

    @property
    def contrabass_count(self):
        """
        Number of contrabasses in string orchestra.

        Returns nonnegative integer.
        """
        return self._contrabass_count

    @property
    def split_hands(self):
        """
        Is true if each performer's hand receives a separate staff.
        """
        return self._split_hands

    @property
    def use_percussion_clefs(self):
        """
        Is true if each staff should use a percussion clef rather than the
        normal clef for that instrument.
        """
        return self._use_percussion_clefs

    @property
    def viola_count(self):
        """
        Number of violas in string orcestra.

        Returns nonnegative integer.
        """
        return self._viola_count

    @property
    def violin_count(self):
        """
        Number of violins in string orchestra.

        Returns nonnegative integer.
        """
        return self._violin_count
