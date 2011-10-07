from abjad.tools.iotools._LilyPondSyntaxNode import _LilyPondSyntaxNode as Node


class _LilyPondSyntacticalDefinition(object):

    ### SYNTACTICAL RULES ###

    def p_lilypond(self, p):
        '''lilypond : empty
                    | lilypond toplevel_expression
                    | lilypond assignment
                    | lilypond error
                    | lilypond "\\invalid"
        '''
        p[0] = Node('lilypond', p[1:])


    def p_object_id_setting(self, p):
        '''object_id_setting : "\\objectid" STRING
        '''
        p[0] = Node('object_id_setting', p[1:])


    def p_toplevel_expression(self, p):
        '''toplevel_expression : lilypond_header
                               | book_block
                               | bookpart_block
                               | score_block
                               | composite_music
                               | full_markup
                               | full_markup_list
                               | output_def
        '''
        p[0] = Node('toplevel_expression', p[1:])


    def p_embedded_scm(self, p):
        '''embedded_scm : SCM_TOKEN
                        | SCM_IDENTIFIER
        '''
        p[0] = Node('embedded_scm', p[1:])


    def p_lilypond_header_body(self, p):
        '''lilypond_header_body : empty
                                | lilypond_header_body assignment
        '''
        p[0] = Node('lilypond_header_body', p[1:])


    def p_lilypond_header(self, p):
        '''lilypond_header : "\\header" '{' lilypond_header_body '}'
        '''
        p[0] = Node('lilypond_header', p[1:])


    def p_assignment_id(self, p):
        '''assignment_id : STRING
                         | LYRICS_STRING
        '''
        p[0] = Node('assignment_id', p[1:])


    def p_assignment(self, p):
        '''assignment : assignment_id '=' identifier_init
                      | embedded_scm
        '''
        p[0] = Node('assignment', p[1:])


    def p_identifier_init(self, p):
        '''identifier_init : score_block
                           | book_block
                           | bookpart_block
                           | output_def
                           | context_def_spec_block
                           | music
                           | post_event
                           | number_expression
                           | string
                           | embedded_scm
                           | full_markup
                           | DIGIT
        '''
        p[0] = Node('identifier_init', p[1:])


    def p_context_def_spec_block(self, p):
        '''context_def_spec_block : "\\context" '{' context_def_spec_body '}'
        '''
        p[0] = Node('context_def_spec_block', p[1:])


    def p_context_def_spec_body(self, p):
        '''context_def_spec_body : empty
                                 | CONTEXT_DEF_IDENTIFIER
                                 | context_def_spec_body "\\grobdescriptions" embedded_scm
                                 | context_def_spec_body context_mod
        '''
        p[0] = Node('context_def_spec_body', p[1:])


    def p_book_block(self, p):
        '''book_block : "\\book" '{' book_body '}'
        '''
        p[0] = Node('book_block', p[1:])


    def p_book_body(self, p):
        '''book_body : empty
                     | BOOK_IDENTIFIER
                     | book_body paper_block
                     | book_body bookpart_block
                     | book_body score_block
                     | book_body composite_music
                     | book_body full_markup
                     | book_body full_markup_list
                     | book_body lilypond_header
                     | book_body error
                     | book_body object_id_setting
        '''
        p[0] = Node('book_body', p[1:])


    def p_bookpart_block(self, p):
        '''bookpart_block : "\\bookpart" '{' bookpart_body '}'
        '''
        p[0] = Node('bookpart_block', p[1:])


    def p_bookpart_body(self, p):
        '''bookpart_body : empty
                         | BOOK_IDENTIFIER
                         | bookpart_body paper_block
                         | bookpart_body score_block
                         | bookpart_body composite_music
                         | bookpart_body full_markup
                         | bookpart_body full_markup_list
                         | bookpart_body lilypond_header
                         | bookpart_body error
                         | bookpart_body object_id_setting
        '''
        p[0] = Node('bookpart_body', p[1:])


    def p_score_block(self, p):
        '''score_block : "\\score" '{' score_body '}'
        '''
        p[0] = Node('score_block', p[1:])


    def p_score_body(self, p):
        '''score_body : music
                      | SCORE_IDENTIFIER
                      | score_body object_id_setting
                      | score_body lilypond_header
                      | score_body output_def
                      | score_body error
        '''
        p[0] = Node('score_body', p[1:])


    def p_paper_block(self, p):
        '''paper_block : output_def
        '''
        p[0] = Node('paper_block', p[1:])


    def p_output_def(self, p):
        '''output_def : output_def_body '}'
        '''
        p[0] = Node('output_def', p[1:])


    def p_output_def_head(self, p):
        '''output_def_head : "\\paper"
                           | "\\midi"
                           | "\\layout"
        '''
        p[0] = Node('output_def_head', p[1:])


    def p_output_def_head_with_mode_switch(self, p):
        '''output_def_head_with_mode_switch : output_def_head
        '''
        p[0] = Node('output_def_head_with_mode_switch', p[1:])


    def p_output_def_body(self, p):
        '''output_def_body : output_def_head_with_mode_switch '{'
                           | output_def_head_with_mode_switch '{' OUTPUT_DEF_IDENTIFIER
                           | output_def_body assignment
                           | output_def_body context_def_spec_block
                           | output_def_body error
        '''
        p[0] = Node('output_def_body', p[1:])


    def p_tempo_event(self, p):
        '''tempo_event : "\\tempo" steno_duration '=' bare_unsigned
                       | "\\tempo" string steno_duration '=' bare_unsigned
                       | "\\tempo" full_markup steno_duration '=' bare_unsigned
                       | "\\tempo" string
                       | "\\tempo" full_markup
        '''
        p[0] = Node('tempo_event', p[1:])


    def p_music_list(self, p):
        '''music_list : empty
                      | music_list music
                      | music_list embedded_scm
                      | music_list error
        '''
        p[0] = Node('music_list', p[1:])


    def p_music(self, p):
        '''music : simple_music
                 | composite_music
        '''
        p[0] = Node('music', p[1:])


    def p_alternative_music(self, p):
        '''alternative_music : empty
                             | "\\alternative" '{' music_list '}'
        '''
        p[0] = Node('alternative_music', p[1:])


    def p_repeated_music(self, p):
        '''repeated_music : "\\repeat" simple_string unsigned_number music alternative_music
        '''
        p[0] = Node('repeated_music', p[1:])


    def p_sequential_music(self, p):
        '''sequential_music : "\\sequential" '{' music_list '}'
                            | '{' music_list '}'
        '''
        p[0] = Node('sequential_music', p[1:])


    def p_simultaneous_music(self, p):
        '''simultaneous_music : "\\simultaneous" '{' music_list '}'
                              | "<<" music_list ">>"
        '''
        p[0] = Node('simultaneous_music', p[1:])


    def p_simple_music(self, p):
        '''simple_music : event_chord
                        | MUSIC_IDENTIFIER
                        | music_property_def
                        | context_change
        '''
        p[0] = Node('simple_music', p[1:])


#    def p_optional_context_mod(self, p):
#        '''optional_context_mod : empty
#        '''
#        p[0] = Node('optional_context_mod', p[1:])


#    def p_optional_context_mod(self, p):
#        '''optional_context_mod : "\with"  '{' context_mod_list '}'
#        '''
#        p[0] = Node('optional_context_mod', p[1:])


    def p_optional_context_mod(self, p):
        '''optional_context_mod : empty
                                | "\with"  '{' context_mod_list '}'
        '''
        p[0] = Node('optional_context_mod', p[1:])


    def p_context_mod_list(self, p):
        '''context_mod_list : empty
                            | context_mod_list context_mod
        '''
        p[0] = Node('context_mod_list', p[1:])


    def p_composite_music(self, p):
        '''composite_music : prefix_composite_music
                           | grouped_music_list
        '''
        p[0] = Node('composite_music', p[1:])


    def p_grouped_music_list(self, p):
        '''grouped_music_list : simultaneous_music
                              | sequential_music
        '''
        p[0] = Node('grouped_music_list', p[1:])


    def p_function_scm_argument(self, p):
        '''function_scm_argument : embedded_scm
                                 | simple_string
        '''
        p[0] = Node('function_scm_argument', p[1:])


    def p_function_arglist_music_last(self, p):
        '''function_arglist_music_last : EXPECT_MUSIC function_arglist music
        '''
        p[0] = Node('function_arglist_music_last', p[1:])


    def p_function_arglist_nonmusic_last(self, p):
        '''function_arglist_nonmusic_last : EXPECT_MARKUP function_arglist full_markup
                                          | EXPECT_SCM function_arglist function_scm_argument
        '''
        p[0] = Node('function_arglist_nonmusic_last', p[1:])


    def p_function_arglist_nonmusic(self, p):
        '''function_arglist_nonmusic : EXPECT_NO_MORE_ARGS
                                     | EXPECT_MARKUP function_arglist_nonmusic full_markup
                                     | EXPECT_SCM function_arglist_nonmusic function_scm_argument
        '''
        p[0] = Node('function_arglist_nonmusic', p[1:])


    def p_function_arglist(self, p):
        '''function_arglist : EXPECT_NO_MORE_ARGS
                            | function_arglist_music_last
                            | function_arglist_nonmusic_last
        '''
        p[0] = Node('function_arglist', p[1:])


    def p_generic_prefix_music_scm(self, p):
        '''generic_prefix_music_scm : MUSIC_FUNCTION function_arglist
        '''
        p[0] = Node('generic_prefix_music_scm', p[1:])


    def p_optional_id(self, p):
        '''optional_id : empty
                       | '=' simple_string
        '''
        p[0] = Node('optional_id', p[1:])


    def p_prefix_composite_music(self, p):
        '''prefix_composite_music : generic_prefix_music_scm
                                  | "\context" simple_string optional_id optional_context_mod music
                                  | "\new" simple_string optional_id optional_context_mod music
                                  | "\times" fraction music
                                  | repeated_music
                                  | "\transpose" pitch_also_in_chords pitch_also_in_chords music
                                  | mode_changing_head grouped_music_list
                                  | mode_changing_head_with_context optional_context_mod grouped_music_list
                                  | relative_music
                                  | re_rhythmed_music
        '''
        p[0] = Node('prefix_composite_music', p[1:])


    def p_mode_changing_head(self, p):
        '''mode_changing_head : "\notemode"
                              | "\drummode"
                              | "\figuremode"
                              | "\chordmode"
                              | "\lyricmode"
        '''
        p[0] = Node('mode_changing_head', p[1:])


    def p_mode_changing_head_with_context(self, p):
        '''mode_changing_head_with_context : "\drums"
                                           | "\figures"
                                           | "\chords"
                                           | "\lyrics"
        '''
        p[0] = Node('mode_changing_head_with_context', p[1:])


    def p_relative_music(self, p):
        '''relative_music : "\relative" absolute_pitch music
                          | "\relative" composite_music
        '''
        p[0] = Node('relative_music', p[1:])


#    def p_new_lyrics(self, p):
#        '''new_lyrics : "\addlyrics"  grouped_music_list
#        '''
#        p[0] = Node('new_lyrics', p[1:])


#    def p_new_lyrics(self, p):
#        '''new_lyrics : new_lyrics "\addlyrics"  grouped_music_list
#        '''
#        p[0] = Node('new_lyrics', p[1:])


    def p_new_lyrics(self, p):
        '''new_lyrics : "\addlyrics"  grouped_music_list
                      | new_lyrics "\addlyrics"  grouped_music_list
        '''
        p[0] = Node('new_lyrics', p[1:])


#    def p_re_rhythmed_music(self, p):
#        '''re_rhythmed_music : grouped_music_list new_lyrics
#        '''
#        p[0] = Node('re_rhythmed_music', p[1:])


#    def p_re_rhythmed_music(self, p):
#        '''re_rhythmed_music : "\lyricsto" simple_string  music
#        '''
#        p[0] = Node('re_rhythmed_music', p[1:])


    def p_re_rhythmed_music(self, p):
        '''re_rhythmed_music : grouped_music_list new_lyrics
                             | "\lyricsto" simple_string  music
        '''
        p[0] = Node('re_rhythmed_music', p[1:])


    def p_context_change(self, p):
        '''context_change : "\change" STRING '=' STRING
        '''
        p[0] = Node('context_change', p[1:])


    def p_property_path_revved(self, p):
        '''property_path_revved : embedded_scm
                                | property_path_revved embedded_scm
        '''
        p[0] = Node('property_path_revved', p[1:])


    def p_property_path(self, p):
        '''property_path : property_path_revved
        '''
        p[0] = Node('property_path', p[1:])


    def p_property_operation(self, p):
        '''property_operation : STRING '=' scalar
                              | "\unset" simple_string
                              | "\override" simple_string property_path '=' embedded_scm
                              | "\revert" simple_string embedded_scm
        '''
        p[0] = Node('property_operation', p[1:])


    def p_context_def_mod(self, p):
        '''context_def_mod : "\consists"
                           | "\remove"
                           | "\accepts"
                           | "\defaultchild"
                           | "\denies"
                           | "\alias"
                           | "\type"
                           | "\description"
                           | "\name"
        '''
        p[0] = Node('context_def_mod', p[1:])


    def p_context_mod(self, p):
        '''context_mod : property_operation
                       | context_def_mod STRING
        '''
        p[0] = Node('context_mod', p[1:])


    def p_context_prop_spec(self, p):
        '''context_prop_spec : simple_string
                             | simple_string '.' simple_string
        '''
        p[0] = Node('context_prop_spec', p[1:])


    def p_simple_music_property_def(self, p):
        '''simple_music_property_def : "\override" context_prop_spec property_path '=' scalar
                                     | "\revert" context_prop_spec embedded_scm
                                     | "\set" context_prop_spec '=' scalar
                                     | "\unset" context_prop_spec
        '''
        p[0] = Node('simple_music_property_def', p[1:])


    def p_music_property_def(self, p):
        '''music_property_def : simple_music_property_def
                              | "\once" simple_music_property_def
        '''
        p[0] = Node('music_property_def', p[1:])


    def p_string(self, p):
        '''string : STRING
                  | STRING_IDENTIFIER
                  | string '+' string
        '''
        p[0] = Node('string', p[1:])


    def p_simple_string(self, p):
        '''simple_string : STRING
                         | LYRICS_STRING
                         | STRING_IDENTIFIER
        '''
        p[0] = Node('simple_string', p[1:])


    def p_scalar(self, p):
        '''scalar : string
                  | LYRICS_STRING
                  | bare_number
                  | embedded_scm
                  | full_markup
                  | DIGIT
        '''
        p[0] = Node('scalar', p[1:])


    def p_event_chord(self, p):
        '''event_chord : simple_chord_elements post_events
                       | MULTI_MEASURE_REST optional_notemode_duration post_events
                       | command_element
                       | note_chord_element
        '''
        p[0] = Node('event_chord', p[1:])


    def p_note_chord_element(self, p):
        '''note_chord_element : chord_body optional_notemode_duration post_events
        '''
        p[0] = Node('note_chord_element', p[1:])


    def p_chord_body(self, p):
        '''chord_body : "<" chord_body_elements ">"
        '''
        p[0] = Node('chord_body', p[1:])


    def p_chord_body_elements(self, p):
        '''chord_body_elements : empty
                               | chord_body_elements chord_body_element
        '''
        p[0] = Node('chord_body_elements', p[1:])


    def p_chord_body_element(self, p):
        '''chord_body_element : pitch exclamations questions octave_check post_events
                              | DRUM_PITCH post_events
                              | music_function_chord_body
        '''
        p[0] = Node('chord_body_element', p[1:])


    def p_music_function_identifier_musicless_prefix(self, p):
        '''music_function_identifier_musicless_prefix : MUSIC_FUNCTION
        '''
        p[0] = Node('music_function_identifier_musicless_prefix', p[1:])


    def p_music_function_chord_body(self, p):
        '''music_function_chord_body : music_function_identifier_musicless_prefix EXPECT_MUSIC function_arglist_nonmusic chord_body_element
                                     | music_function_identifier_musicless_prefix function_arglist_nonmusic
        '''
        p[0] = Node('music_function_chord_body', p[1:])


    def p_music_function_event(self, p):
        '''music_function_event : music_function_identifier_musicless_prefix EXPECT_MUSIC function_arglist_nonmusic post_event
                                | music_function_identifier_musicless_prefix function_arglist_nonmusic
        '''
        p[0] = Node('music_function_event', p[1:])


    def p_command_element(self, p):
        '''command_element : command_event
                           | "\skip" duration_length
                           | "\["
                           | "\]"
                           | "\"
                           | '|'
                           | "\partial" duration_length
                           | "\time" fraction
                           | "\mark" scalar
        '''
        p[0] = Node('command_element', p[1:])
    

    def p_command_event(self, p):
        '''command_event : "\~"
                         | "\mark" "\default"
                         | tempo_event
                         | "\key" "\default"
                         | "\key" NOTENAME_PITCH SCM_IDENTIFIER
        '''
        p[0] = Node('command_event', p[1:])


    def p_post_events(self, p):
        '''post_events: empty
                      | post_events post_event
        '''
        p[0] = Node('post_events', p[1:])


    def p_post_event(self, p):
        '''post_event : direction_less_event
                      | '-' music_function_event
                      | "--"
                      | "__"
                      | script_dir direction_reqd_event
                      | script_dir direction_less_event
                      | string_number_event
        '''
        p[0] = Node('post_event', p[1:])


    def p_string_number_event(self, p):
        '''string_number_event : E_UNSIGNED
        '''
        p[0] = Node('string_number_event', p[1:])


    def p_direction_less_char(self, p):
        '''direction_less_char : '['
                               | ']'
                               | '~'
                               | '('
                               | ')'
                               | "\!"
                               | "\("
                               | "\)"
                               | "\>"
                               | "\<"
        '''
        p[0] = Node('direction_less_char', p[1:])


    def p_direction_less_event(self, p):
        '''direction_less_event : direction_less_char
                                | EVENT_IDENTIFIER
                                | tremolo_type
        '''
        p[0] = Node('direction_less_event', p[1:])


    def p_direction_reqd_event(self, p):
        '''direction_reqd_event : gen_text_def
                                | script_abbreviation
        '''
        p[0] = Node('direction_reqd_event', p[1:])


    def p_octave_check(self, p):
        '''octave_check : empty
                        | '='
                        | '=' sub_quotes
                        | '=' sup_quotes
        '''
        p[0] = Node('octave_check', p[1:])


    def p_sup_quotes(self, p):
        '''sup_quotes : "'"
                      | sup_quotes "'"
        '''
        p[0] = Node('sup_quotes', p[1:])


    def p_sub_quotes(self, p):
        '''sub_quotes : ','
                      | sub_quotes ','
        '''
        p[0] = Node('sub_quotes', p[1:])


    def p_steno_pitch(self, p):
        '''steno_pitch : NOTENAME_PITCH
                       | NOTENAME_PITCH sup_quotes
                       | NOTENAME_PITCH sub_quotes
        '''
        p[0] = Node('steno_pitch', p[1:])


    def p_steno_tonic_pitch(self, p):
        '''steno_tonic_pitch : TONICNAME_PITCH
                             | TONICNAME_PITCH sup_quotes
                             | TONICNAME_PITCH sub_quotes
        '''
        p[0] = Node('steno_tonic_pitch', p[1:])


    def p_pitch(self, p):
        '''pitch : steno_pitch
        '''
        p[0] = Node('pitch', p[1:])


    def p_pitch_also_in_chords(self, p):
        '''pitch_also_in_chords : pitch
                                | steno_tonic_pitch
        '''
        p[0] = Node('pitch_also_in_chords', p[1:])


    def p_gen_text_def(self, p):
        '''gen_text_def : full_markup
                        | string
                        | DIGIT
        '''
        p[0] = Node('gen_text_def', p[1:])


    def p_script_abbreviation(self, p):
        '''script_abbreviation : '^'
                               | '+'
                               | '-'
                               | '|'
                               | ">"
                               | '.'
                               | '_'
        '''
        p[0] = Node('script_abbreviation', p[1:])


    def p_script_dir(self, p):
        '''script_dir : '_'
                      | '^'
                      | '-'
        '''
        p[0] = Node('script_dir', p[1:])


    def p_absolute_pitch(self, p):
        '''absolute_pitch : steno_pitch
        '''
        p[0] = Node('absolute_pitch', p[1:])


    def p_duration_length(self, p):
        '''duration_length : multiplied_duration
        '''
        p[0] = Node('duration_length', p[1:])


    def p_optional_notemode_duration(self, p):
        '''optional_notemode_duration : empty
                                      | multiplied_duration
        '''
        p[0] = Node('optional_notemode_duration', p[1:])


    def p_steno_duration(self, p):
        '''steno_duration : bare_unsigned dots
                          | DURATION_IDENTIFIER dots
        '''
        p[0] = Node('steno_duration', p[1:])


    def p_multiplied_duration(self, p):
        '''multiplied_duration : steno_duration
                               | multiplied_duration '*' bare_unsigned
                               | multiplied_duration '*' FRACTION
        '''
        p[0] = Node('multiplied_duration', p[1:])


    def p_fraction(self, p):
        '''fraction : FRACTION
                    | UNSIGNED '/' UNSIGNED
        '''
        p[0] = Node('fraction', p[1:])


    def p_dots(self, p):
        '''dots : empty
                | dots '.'
        '''
        p[0] = Node('dots', p[1:])


    def p_tremolo_type(self, p):
        '''tremolo_type : ':'
                        | ':' bare_unsigned
        '''
        p[0] = Node('tremolo_type', p[1:])


    def p_bass_number(self, p):
        '''bass_number : DIGIT
                       | UNSIGNED
                       | STRING
                       | full_markup
        '''
        p[0] = Node('bass_number', p[1:])


    def p_figured_bass_alteration(self, p):
        '''figured_bass_alteration : '-'
                                   | '+'
                                   | '!'
        '''
        p[0] = Node('figured_bass_alteration', p[1:])


    def p_bass_figure(self, p):
        '''bass_figure : "_"
                       | bass_number
                       | bass_figure ']'
                       | bass_figure figured_bass_alteration
                       | bass_figure figured_bass_modification
        '''
        p[0] = Node('bass_figure', p[1:])


    def p_figured_bass_modification(self, p):
        '''figured_bass_modification : "\+"
                                     | "\!"
                                     | '/'
                                     | "\"
        '''
        p[0] = Node('figured_bass_modification', p[1:])


    def p_br_bass_figure(self, p):
        '''br_bass_figure : bass_figure
                          | '[' bass_figure
        '''
        p[0] = Node('br_bass_figure', p[1:])


    def p_figure_list(self, p):
        '''figure_list : empty
                       | figure_list br_bass_figure
        '''
        p[0] = Node('figure_list', p[1:])


    def p_figure_spec(self, p):
        '''figure_spec : FIGURE_OPEN figure_list FIGURE_CLOSE
        '''
        p[0] = Node('figure_spec', p[1:])


    def p_optional_rest(self, p):
        '''optional_rest : empty
                         | "\rest"
        '''
        p[0] = Node('optional_rest', p[1:])


    def p_simple_element(self, p):
        '''simple_element : pitch exclamations questions octave_check optional_notemode_duration optional_rest
                          | DRUM_PITCH optional_notemode_duration
                          | RESTNAME optional_notemode_duration
                          | lyric_element optional_notemode_duration
        '''
        p[0] = Node('simple_element', p[1:])


    def p_simple_chord_elements(self, p):
        '''simple_chord_elements : simple_element
                                 | new_chord
                                 | figure_spec optional_notemode_duration
        '''
        p[0] = Node('simple_chord_elements', p[1:])


    def p_lyric_element(self, p):
        '''lyric_element : lyric_markup
                         | LYRICS_STRING
        '''
        p[0] = Node('lyric_element', p[1:])


    def p_new_chord(self, p):
        '''new_chord : steno_tonic_pitch optional_notemode_duration
                     | steno_tonic_pitch optional_notemode_duration chord_separator chord_items
        '''
        p[0] = Node('new_chord', p[1:])


    def p_chord_items(self, p):
        '''chord_items : empty
                       | chord_items chord_item
        '''
        p[0] = Node('chord_items', p[1:])


    def p_chord_separator(self, p):
        '''chord_separator : ":"
                           | "^"
                           | "/" steno_tonic_pitch
                           | "/+" steno_tonic_pitch
        '''
        p[0] = Node('chord_separator', p[1:])


    def p_chord_item(self, p):
        '''chord_item : chord_separator
                      | step_numbers
                      | CHORD_MODIFIER
        '''
        p[0] = Node('chord_item', p[1:])


    def p_step_numbers(self, p):
        '''step_numbers : step_number
                        | step_numbers '.' step_number
        '''
        p[0] = Node('step_numbers', p[1:])


    def p_step_number(self, p):
        '''step_number : bare_unsigned
                       | bare_unsigned '+'
                       | bare_unsigned "-"
        '''
        p[0] = Node('step_number', p[1:])


    def p_number_expression(self, p):
        '''number_expression : number_expression '+' number_term
                             | number_expression '-' number_term
                             | number_term
        '''
        p[0] = Node('number_expression', p[1:])


    def p_number_term(self, p):
        '''number_term : number_factor
                       | number_factor '*' number_factor
                       | number_factor '/' number_factor
        '''
        p[0] = Node('number_term', p[1:])


    def p_number_factor(self, p):
        '''number_factor : '-' number_factor
                         | bare_number
        '''
        p[0] = Node('number_factor', p[1:])


    def p_bare_number(self, p):
        '''bare_number : UNSIGNED
                       | REAL
                       | NUMBER_IDENTIFIER
                       | REAL NUMBER_IDENTIFIER
                       | UNSIGNED NUMBER_IDENTIFIER
        '''
        p[0] = Node('bare_number', p[1:])


    def p_bare_unsigned(self, p):
        '''bare_unsigned : UNSIGNED
                         | DIGIT
        '''
        p[0] = Node('bare_unsigned', p[1:])


    def p_unsigned_number(self, p):
        '''unsigned_number: bare_unsigned
                   | NUMBER_IDENTIFIER
        '''
        p[0] = Node('unsigned_number', p[1:])


    def p_exclamations(self, p):
        '''exclamations : empty
                        | exclamations '!'
        '''
        p[0] = Node('exclamations', p[1:])


    def p_questions(self, p):
        '''questions : empty
                     | questions '?'
        '''
        p[0] = Node('questions', p[1:])


#    def p_lyric_markup(self, p):
#        '''lyric_markup : LYRIC_MARKUP_IDENTIFIER
#        '''
#        p[0] = Node('lyric_markup', p[1:])


#    def p_lyric_markup(self, p):
#        '''lyric_markup : LYRIC_MARKUP  markup_top
#        '''
#        p[0] = Node('lyric_markup', p[1:])


    def p_lyric_markup(self, p):
        '''lyric_markup : LYRIC_MARKUP_IDENTIFIER
                        | LYRIC_MARKUP  markup_top
        '''
        p[0] = Node('lyric_markup', p[1:])


    def p_full_markup_list(self, p):
        '''full_markup_list : "\markuplines"  markup_list
        '''
        p[0] = Node('full_markup_list', p[1:])


#    def p_full_markup(self, p):
#        '''full_markup : MARKUP_IDENTIFIER
#        '''
#        p[0] = Node('full_markup', p[1:])


#    def p_full_markup(self, p):
#        '''full_markup : "\markup"  markup_top
#        '''
#        p[0] = Node('full_markup', p[1:])


    def p_full_markup(self, p):
        '''full_markup : MARKUP_IDENTIFIER
                       | "\markup"  markup_top
        '''
        p[0] = Node('full_markup', p[1:])


    def p_markup_top(self, p):
        '''markup_top : markup_list
                      | markup_head_1_list simple_markup
                      | simple_markup
        '''
        p[0] = Node('markup_top', p[1:])


    def p_markup_list(self, p):
        '''markup_list : markup_composed_list
                       | markup_braced_list
                       | markup_command_list
        '''
        p[0] = Node('markup_list', p[1:])


    def p_markup_composed_list(self, p):
        '''markup_composed_list : markup_head_1_list markup_braced_list
        '''
        p[0] = Node('markup_composed_list', p[1:])


    def p_markup_braced_list(self, p):
        '''markup_braced_list : '{' markup_braced_list_body '}'
        '''
        p[0] = Node('markup_braced_list', p[1:])


    def p_markup_braced_list_body(self, p):
        '''markup_braced_list_body : empty
                                   | markup_braced_list_body markup
                                   | markup_braced_list_body markup_list
        '''
        p[0] = Node('markup_braced_list_body', p[1:])


    def p_markup_command_list(self, p):
        '''markup_command_list : MARKUP_LIST_HEAD_EMPTY
                               | MARKUP_LIST_HEAD_LIST0 markup_list
                               | MARKUP_LIST_HEAD_SCM0 embedded_scm
                               | MARKUP_LIST_HEAD_SCM0_LIST1 embedded_scm markup_list
                               | MARKUP_LIST_HEAD_SCM0_SCM1_LIST2 embedded_scm embedded_scm markup_list
        '''
        p[0] = Node('markup_command_list', p[1:])


    def p_markup_head_1_item(self, p):
        '''markup_head_1_item : MARKUP_HEAD_MARKUP0
                              | MARKUP_HEAD_SCM0_MARKUP1 embedded_scm
                              | MARKUP_HEAD_SCM0_SCM1_MARKUP2 embedded_scm embedded_scm
        '''
        p[0] = Node('markup_head_1_item', p[1:])


    def p_markup_head_1_list(self, p):
        '''markup_head_1_list : markup_head_1_item
                              | markup_head_1_list markup_head_1_item
        '''
        p[0] = Node('markup_head_1_list', p[1:])


    def p_simple_markup(self, p):
        '''simple_markup : STRING
                         | MARKUP_IDENTIFIER
                         | LYRIC_MARKUP_IDENTIFIER
                         | STRING_IDENTIFIER
        '''
        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup(self, p):
        '''simple_markup : "\score"  '{' score_body '}'
                         | MARKUP_HEAD_SCM0 embedded_scm
                         | MARKUP_HEAD_SCM0_SCM1_SCM2 embedded_scm embedded_scm embedded_scm
                         | MARKUP_HEAD_SCM0_SCM1 embedded_scm embedded_scm
                         | MARKUP_HEAD_SCM0_MARKUP1_MARKUP2 embedded_scm markup markup
                         | MARKUP_HEAD_SCM0_SCM1_MARKUP2_MARKUP3 embedded_scm embedded_scm markup markup
                         | MARKUP_HEAD_EMPTY
                         | MARKUP_HEAD_LIST0 markup_list
                         | MARKUP_HEAD_MARKUP0_MARKUP1 markup markup
        '''
        p[0] = Node('simple_markup', p[1:])


    def p_markup(self, p):
        '''markup : markup_head_1_list simple_markup
                  | simple_markup
        '''
        p[0] = Node('markup', p[1:])


    def p_empty(self, p):
        '''empty :
        '''
        p[0] = Node('empty', p[1:])


    def p_error(p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

