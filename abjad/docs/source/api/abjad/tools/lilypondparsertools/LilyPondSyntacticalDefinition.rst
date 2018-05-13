.. _abjad--tools--lilypondparsertools--LilyPondSyntacticalDefinition:

LilyPondSyntacticalDefinition
=============================

.. automodule:: abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition

.. currentmodule:: abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition

.. container:: svg-container

   .. inheritance-diagram:: abjad
      :lineage: abjad.tools.lilypondparsertools.LilyPondSyntacticalDefinition

.. autoclass:: LilyPondSyntacticalDefinition

   .. raw:: html

      <hr/>

   .. rubric:: Special methods
      :class: class-header

   .. automethod:: LilyPondSyntacticalDefinition.__format__

   .. automethod:: LilyPondSyntacticalDefinition.__repr__

   .. raw:: html

      <hr/>

   .. rubric:: Methods
      :class: class-header

   .. automethod:: LilyPondSyntacticalDefinition.p_assignment__assignment_id__Chr61__identifier_init

   .. automethod:: LilyPondSyntacticalDefinition.p_assignment__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_assignment_id__STRING

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_number__REAL__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_number__UNSIGNED__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_number__bare_number_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_number_closed__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_number_closed__REAL

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_number_closed__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_bare_unsigned__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_braced_music_list__Chr123__music_list__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_chord_body__ANGLE_OPEN__chord_body_elements__ANGLE_CLOSE

   .. automethod:: LilyPondSyntacticalDefinition.p_chord_body_element__music_function_chord_body

   .. automethod:: LilyPondSyntacticalDefinition.p_chord_body_element__pitch__exclamations__questions__octave_check__post_events

   .. automethod:: LilyPondSyntacticalDefinition.p_chord_body_elements__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_chord_body_elements__chord_body_elements__chord_body_element

   .. automethod:: LilyPondSyntacticalDefinition.p_closed_music__complex_music_prefix__closed_music

   .. automethod:: LilyPondSyntacticalDefinition.p_closed_music__music_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_command_element__Chr124

   .. automethod:: LilyPondSyntacticalDefinition.p_command_element__E_BACKSLASH

   .. automethod:: LilyPondSyntacticalDefinition.p_command_element__command_event

   .. automethod:: LilyPondSyntacticalDefinition.p_command_event__tempo_event

   .. automethod:: LilyPondSyntacticalDefinition.p_complex_music__complex_music_prefix__music

   .. automethod:: LilyPondSyntacticalDefinition.p_complex_music__music_function_call

   .. automethod:: LilyPondSyntacticalDefinition.p_complex_music_prefix__CONTEXT__simple_string__optional_id__optional_context_mod

   .. automethod:: LilyPondSyntacticalDefinition.p_complex_music_prefix__NEWCONTEXT__simple_string__optional_id__optional_context_mod

   .. automethod:: LilyPondSyntacticalDefinition.p_composite_music__complex_music

   .. automethod:: LilyPondSyntacticalDefinition.p_composite_music__music_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_context_change__CHANGE__STRING__Chr61__STRING

   .. automethod:: LilyPondSyntacticalDefinition.p_context_def_spec_block__CONTEXT__Chr123__context_def_spec_body__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_context_def_spec_body__CONTEXT_DEF_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_context_def_spec_body__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_context_def_spec_body__context_def_spec_body__context_mod

   .. automethod:: LilyPondSyntacticalDefinition.p_context_def_spec_body__context_def_spec_body__context_modification

   .. automethod:: LilyPondSyntacticalDefinition.p_context_def_spec_body__context_def_spec_body__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_context_mod__property_operation

   .. automethod:: LilyPondSyntacticalDefinition.p_context_mod_list__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_context_mod_list__context_mod_list__CONTEXT_MOD_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_context_mod_list__context_mod_list__context_mod

   .. automethod:: LilyPondSyntacticalDefinition.p_context_mod_list__context_mod_list__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_context_modification__CONTEXT_MOD_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_context_modification__WITH__CONTEXT_MOD_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_context_modification__WITH__Chr123__context_mod_list__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_context_modification__WITH__embedded_scm_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_context_prop_spec__simple_string

   .. automethod:: LilyPondSyntacticalDefinition.p_context_prop_spec__simple_string__Chr46__simple_string

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__Chr126

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__Chr40

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__Chr41

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__Chr91

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__Chr93

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__E_ANGLE_CLOSE

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__E_ANGLE_OPEN

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__E_CLOSE

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__E_EXCLAMATION

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_char__E_OPEN

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_event__EVENT_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_event__direction_less_char

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_event__event_function_event

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_less_event__tremolo_type

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_reqd_event__gen_text_def

   .. automethod:: LilyPondSyntacticalDefinition.p_direction_reqd_event__script_abbreviation

   .. automethod:: LilyPondSyntacticalDefinition.p_dots__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_dots__dots__Chr46

   .. automethod:: LilyPondSyntacticalDefinition.p_duration_length__multiplied_duration

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm__embedded_scm_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm__scm_function_call

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_arg__embedded_scm_bare_arg

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_arg__music_arg

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_arg__scm_function_call

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_arg_closed__closed_music

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_arg_closed__embedded_scm_bare_arg

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_arg_closed__scm_function_call_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare__SCM_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare__SCM_TOKEN

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__STRING

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__STRING_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__context_def_spec_block

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__context_modification

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__embedded_scm_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__full_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__full_markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__output_def

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_bare_arg__score_block

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_chord_body__SCM_FUNCTION__music_function_chord_body_arglist

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_chord_body__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_chord_body__chord_body_element

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_chord_body__embedded_scm_bare_arg

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_chord_body__fraction

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_closed__embedded_scm_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_embedded_scm_closed__scm_function_call_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_error

   .. automethod:: LilyPondSyntacticalDefinition.p_event_chord__CHORD_REPETITION__optional_notemode_duration__post_events

   .. automethod:: LilyPondSyntacticalDefinition.p_event_chord__MULTI_MEASURE_REST__optional_notemode_duration__post_events

   .. automethod:: LilyPondSyntacticalDefinition.p_event_chord__command_element

   .. automethod:: LilyPondSyntacticalDefinition.p_event_chord__note_chord_element

   .. automethod:: LilyPondSyntacticalDefinition.p_event_chord__simple_chord_elements__post_events

   .. automethod:: LilyPondSyntacticalDefinition.p_event_function_event__EVENT_FUNCTION__function_arglist_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_exclamations__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_exclamations__exclamations__Chr33

   .. automethod:: LilyPondSyntacticalDefinition.p_fingering__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_fraction__FRACTION

   .. automethod:: LilyPondSyntacticalDefinition.p_fraction__UNSIGNED__Chr47__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_full_markup__MARKUP_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_full_markup__MARKUP__markup_top

   .. automethod:: LilyPondSyntacticalDefinition.p_full_markup_list__MARKUPLIST_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_full_markup_list__MARKUPLIST__markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist__function_arglist_common

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist__function_arglist_nonbackup

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed_keep__duration_length

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_keep__pitch_also_in_chords

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__BACKUP

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__REAL

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__FRACTION

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__REAL

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__post_event_nofinger

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_keep__embedded_scm_arg_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__function_arglist_backup__REPARSE__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__function_arglist_backup__REPARSE__embedded_scm_arg_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_backup__function_arglist_backup__REPARSE__fraction

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_bare__EXPECT_DURATION__function_arglist_closed_optional__duration_length

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_bare__EXPECT_NO_MORE_ARGS

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_skip__DEFAULT

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_skip__DEFAULT

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip__DEFAULT

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_bare__EXPECT_PITCH__function_arglist_optional__pitch_also_in_chords

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed__function_arglist_closed_common

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed__function_arglist_nonbackup

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__REAL

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__fraction

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__post_event_nofinger

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_common__function_arglist_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_keep__function_arglist_backup

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_keep__function_arglist_closed_common

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_optional__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed_optional

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_optional__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_closed_optional

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_optional__function_arglist_backup__BACKUP

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_closed_optional__function_arglist_closed_keep

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__fraction

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__post_event_nofinger

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common__function_arglist_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common__function_arglist_common_minus

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__REAL

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_common_minus__function_arglist_common_minus__REPARSE__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_keep__function_arglist_backup

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_keep__function_arglist_common

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed__duration_length

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist__pitch_also_in_chords

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist__embedded_scm_arg_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__NUMBER_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__REAL

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__FRACTION

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__bare_number_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__post_event_nofinger

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_optional

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_optional

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_optional__function_arglist_backup__BACKUP

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_optional__function_arglist_keep

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_skip

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_skip

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip

   .. automethod:: LilyPondSyntacticalDefinition.p_function_arglist_skip__function_arglist_common

   .. automethod:: LilyPondSyntacticalDefinition.p_gen_text_def__full_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_gen_text_def__simple_string

   .. automethod:: LilyPondSyntacticalDefinition.p_grouped_music_list__sequential_music

   .. automethod:: LilyPondSyntacticalDefinition.p_grouped_music_list__simultaneous_music

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__context_def_spec_block

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__context_modification

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__full_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__full_markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__music

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__number_expression

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__output_def

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__post_event_nofinger

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__score_block

   .. automethod:: LilyPondSyntacticalDefinition.p_identifier_init__string

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond__lilypond__assignment

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond__lilypond__error

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond__lilypond__toplevel_expression

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond_header__HEADER__Chr123__lilypond_header_body__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond_header_body__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_lilypond_header_body__lilypond_header_body__assignment

   .. automethod:: LilyPondSyntacticalDefinition.p_markup__markup_head_1_list__simple_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_markup__simple_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_braced_list__Chr123__markup_braced_list_body__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_braced_list_body__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_braced_list_body__markup_braced_list_body__markup

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_braced_list_body__markup_braced_list_body__markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_command_basic_arguments__EXPECT_MARKUP_LIST__markup_command_list_arguments__markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_command_basic_arguments__EXPECT_NO_MORE_ARGS

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_command_basic_arguments__EXPECT_SCM__markup_command_list_arguments__embedded_scm_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_command_list__MARKUP_LIST_FUNCTION__markup_command_list_arguments

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_command_list_arguments__EXPECT_MARKUP__markup_command_list_arguments__markup

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_command_list_arguments__markup_command_basic_arguments

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_composed_list__markup_head_1_list__markup_braced_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_head_1_item__MARKUP_FUNCTION__EXPECT_MARKUP__markup_command_list_arguments

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_head_1_list__markup_head_1_item

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_head_1_list__markup_head_1_list__markup_head_1_item

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_list__MARKUPLIST_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_list__markup_braced_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_list__markup_command_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_list__markup_composed_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_list__markup_scm__MARKUPLIST_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_scm__embedded_scm_bare__BACKUP

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_top__markup_head_1_list__simple_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_top__markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_markup_top__simple_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_multiplied_duration__multiplied_duration__Chr42__FRACTION

   .. automethod:: LilyPondSyntacticalDefinition.p_multiplied_duration__multiplied_duration__Chr42__bare_unsigned

   .. automethod:: LilyPondSyntacticalDefinition.p_multiplied_duration__steno_duration

   .. automethod:: LilyPondSyntacticalDefinition.p_music__composite_music

   .. automethod:: LilyPondSyntacticalDefinition.p_music__simple_music

   .. automethod:: LilyPondSyntacticalDefinition.p_music_arg__composite_music

   .. automethod:: LilyPondSyntacticalDefinition.p_music_arg__simple_music

   .. automethod:: LilyPondSyntacticalDefinition.p_music_bare__MUSIC_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_music_bare__grouped_music_list

   .. automethod:: LilyPondSyntacticalDefinition.p_music_function_call__MUSIC_FUNCTION__function_arglist

   .. automethod:: LilyPondSyntacticalDefinition.p_music_function_chord_body__MUSIC_FUNCTION__music_function_chord_body_arglist

   .. automethod:: LilyPondSyntacticalDefinition.p_music_function_chord_body_arglist__EXPECT_SCM__music_function_chord_body_arglist__embedded_scm_chord_body

   .. automethod:: LilyPondSyntacticalDefinition.p_music_function_chord_body_arglist__function_arglist_bare

   .. automethod:: LilyPondSyntacticalDefinition.p_music_function_event__MUSIC_FUNCTION__function_arglist_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_music_list__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_music_list__music_list__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_music_list__music_list__error

   .. automethod:: LilyPondSyntacticalDefinition.p_music_list__music_list__music

   .. automethod:: LilyPondSyntacticalDefinition.p_music_property_def__simple_music_property_def

   .. automethod:: LilyPondSyntacticalDefinition.p_note_chord_element__chord_body__optional_notemode_duration__post_events

   .. automethod:: LilyPondSyntacticalDefinition.p_number_expression__number_expression__Chr43__number_term

   .. automethod:: LilyPondSyntacticalDefinition.p_number_expression__number_expression__Chr45__number_term

   .. automethod:: LilyPondSyntacticalDefinition.p_number_expression__number_term

   .. automethod:: LilyPondSyntacticalDefinition.p_number_factor__Chr45__number_factor

   .. automethod:: LilyPondSyntacticalDefinition.p_number_factor__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_number_term__number_factor

   .. automethod:: LilyPondSyntacticalDefinition.p_number_term__number_factor__Chr42__number_factor

   .. automethod:: LilyPondSyntacticalDefinition.p_number_term__number_factor__Chr47__number_factor

   .. automethod:: LilyPondSyntacticalDefinition.p_octave_check__Chr61

   .. automethod:: LilyPondSyntacticalDefinition.p_octave_check__Chr61__sub_quotes

   .. automethod:: LilyPondSyntacticalDefinition.p_octave_check__Chr61__sup_quotes

   .. automethod:: LilyPondSyntacticalDefinition.p_octave_check__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_context_mod__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_context_mod__context_modification

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_id__Chr61__simple_string

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_id__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_notemode_duration__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_notemode_duration__multiplied_duration

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_rest__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_optional_rest__REST

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def__output_def_body__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_body__output_def_body__assignment

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_body__output_def_head_with_mode_switch__Chr123

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_body__output_def_head_with_mode_switch__Chr123__OUTPUT_DEF_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_head__LAYOUT

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_head__MIDI

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_head__PAPER

   .. automethod:: LilyPondSyntacticalDefinition.p_output_def_head_with_mode_switch__output_def_head

   .. automethod:: LilyPondSyntacticalDefinition.p_pitch__PITCH_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_pitch__steno_pitch

   .. automethod:: LilyPondSyntacticalDefinition.p_pitch_also_in_chords__pitch

   .. automethod:: LilyPondSyntacticalDefinition.p_pitch_also_in_chords__steno_tonic_pitch

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event__Chr45__fingering

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event__post_event_nofinger

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__Chr94__fingering

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__Chr95__fingering

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__EXTENDER

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__HYPHEN

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__direction_less_event

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__script_dir__direction_less_event

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__script_dir__direction_reqd_event

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__script_dir__music_function_event

   .. automethod:: LilyPondSyntacticalDefinition.p_post_event_nofinger__string_number_event

   .. automethod:: LilyPondSyntacticalDefinition.p_post_events__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_post_events__post_events__post_event

   .. automethod:: LilyPondSyntacticalDefinition.p_property_operation__OVERRIDE__simple_string__property_path__Chr61__scalar

   .. automethod:: LilyPondSyntacticalDefinition.p_property_operation__REVERT__simple_string__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_property_operation__STRING__Chr61__scalar

   .. automethod:: LilyPondSyntacticalDefinition.p_property_operation__UNSET__simple_string

   .. automethod:: LilyPondSyntacticalDefinition.p_property_path__property_path_revved

   .. automethod:: LilyPondSyntacticalDefinition.p_property_path_revved__embedded_scm_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_property_path_revved__property_path_revved__embedded_scm_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_questions__Empty

   .. automethod:: LilyPondSyntacticalDefinition.p_questions__questions__Chr63

   .. automethod:: LilyPondSyntacticalDefinition.p_scalar__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_scalar__embedded_scm_arg

   .. automethod:: LilyPondSyntacticalDefinition.p_scalar_closed__bare_number

   .. automethod:: LilyPondSyntacticalDefinition.p_scalar_closed__embedded_scm_arg_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_scm_function_call__SCM_FUNCTION__function_arglist

   .. automethod:: LilyPondSyntacticalDefinition.p_scm_function_call_closed__SCM_FUNCTION__function_arglist_closed

   .. automethod:: LilyPondSyntacticalDefinition.p_score_block__SCORE__Chr123__score_body__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_score_body__SCORE_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_score_body__music

   .. automethod:: LilyPondSyntacticalDefinition.p_score_body__score_body__lilypond_header

   .. automethod:: LilyPondSyntacticalDefinition.p_score_body__score_body__output_def

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__ANGLE_CLOSE

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__Chr124

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__Chr43

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__Chr45

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__Chr46

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__Chr94

   .. automethod:: LilyPondSyntacticalDefinition.p_script_abbreviation__Chr95

   .. automethod:: LilyPondSyntacticalDefinition.p_script_dir__Chr45

   .. automethod:: LilyPondSyntacticalDefinition.p_script_dir__Chr94

   .. automethod:: LilyPondSyntacticalDefinition.p_script_dir__Chr95

   .. automethod:: LilyPondSyntacticalDefinition.p_sequential_music__SEQUENTIAL__braced_music_list

   .. automethod:: LilyPondSyntacticalDefinition.p_sequential_music__braced_music_list

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_chord_elements__simple_element

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_element__RESTNAME__optional_notemode_duration

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_element__pitch__exclamations__questions__octave_check__optional_notemode_duration__optional_rest

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_markup__MARKUP_FUNCTION__markup_command_basic_arguments

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_markup__MARKUP_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_markup__SCORE__Chr123__score_body__Chr125

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_markup__STRING

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_markup__STRING_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_markup__markup_scm__MARKUP_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music__context_change

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music__event_chord

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music__music_property_def

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music_property_def__OVERRIDE__context_prop_spec__property_path__Chr61__scalar

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music_property_def__REVERT__context_prop_spec__embedded_scm

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music_property_def__SET__context_prop_spec__Chr61__scalar

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_music_property_def__UNSET__context_prop_spec

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_string__STRING

   .. automethod:: LilyPondSyntacticalDefinition.p_simple_string__STRING_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_simultaneous_music__DOUBLE_ANGLE_OPEN__music_list__DOUBLE_ANGLE_CLOSE

   .. automethod:: LilyPondSyntacticalDefinition.p_simultaneous_music__SIMULTANEOUS__braced_music_list

   .. automethod:: LilyPondSyntacticalDefinition.p_start_symbol__lilypond

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_duration__DURATION_IDENTIFIER__dots

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_duration__bare_unsigned__dots

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_pitch__NOTENAME_PITCH

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_pitch__NOTENAME_PITCH__sub_quotes

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_pitch__NOTENAME_PITCH__sup_quotes

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_tonic_pitch__TONICNAME_PITCH

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_tonic_pitch__TONICNAME_PITCH__sub_quotes

   .. automethod:: LilyPondSyntacticalDefinition.p_steno_tonic_pitch__TONICNAME_PITCH__sup_quotes

   .. automethod:: LilyPondSyntacticalDefinition.p_string__STRING

   .. automethod:: LilyPondSyntacticalDefinition.p_string__STRING_IDENTIFIER

   .. automethod:: LilyPondSyntacticalDefinition.p_string__string__Chr43__string

   .. automethod:: LilyPondSyntacticalDefinition.p_string_number_event__E_UNSIGNED

   .. automethod:: LilyPondSyntacticalDefinition.p_sub_quotes__Chr44

   .. automethod:: LilyPondSyntacticalDefinition.p_sub_quotes__sub_quotes__Chr44

   .. automethod:: LilyPondSyntacticalDefinition.p_sup_quotes__Chr39

   .. automethod:: LilyPondSyntacticalDefinition.p_sup_quotes__sup_quotes__Chr39

   .. automethod:: LilyPondSyntacticalDefinition.p_tempo_event__TEMPO__scalar

   .. automethod:: LilyPondSyntacticalDefinition.p_tempo_event__TEMPO__scalar_closed__steno_duration__Chr61__tempo_range

   .. automethod:: LilyPondSyntacticalDefinition.p_tempo_event__TEMPO__steno_duration__Chr61__tempo_range

   .. automethod:: LilyPondSyntacticalDefinition.p_tempo_range__bare_unsigned

   .. automethod:: LilyPondSyntacticalDefinition.p_tempo_range__bare_unsigned__Chr45__bare_unsigned

   .. automethod:: LilyPondSyntacticalDefinition.p_toplevel_expression__composite_music

   .. automethod:: LilyPondSyntacticalDefinition.p_toplevel_expression__full_markup

   .. automethod:: LilyPondSyntacticalDefinition.p_toplevel_expression__full_markup_list

   .. automethod:: LilyPondSyntacticalDefinition.p_toplevel_expression__lilypond_header

   .. automethod:: LilyPondSyntacticalDefinition.p_toplevel_expression__output_def

   .. automethod:: LilyPondSyntacticalDefinition.p_toplevel_expression__score_block

   .. automethod:: LilyPondSyntacticalDefinition.p_tremolo_type__Chr58

   .. automethod:: LilyPondSyntacticalDefinition.p_tremolo_type__Chr58__bare_unsigned