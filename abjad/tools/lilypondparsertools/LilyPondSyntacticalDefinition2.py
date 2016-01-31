# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject
from abjad.tools.lilypondparsertools.SyntaxNode import SyntaxNode


class _LilyPondSyntacticalDefinition2(AbjadObject):
    r'''The syntactical definition of LilyPond's syntax.

    Effectively equivalent to LilyPond's ``parser.yy`` file.

    Not composer-safe.

    Used internally by ``LilyPondParser``.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    start_symbol = 'start_symbol'

    precedence = (
        # ('nonassoc', 'REPEAT'),
        # ('nonassoc', 'ALTERNATIVE'),
        ('nonassoc', 'COMPOSITE'),
        # ('left', 'ADDLYRICS'),
        ('nonassoc', 'DEFAULT'),
        ('nonassoc', 'FUNCTION_ARGLIST'),
        ('right', 'PITCH_IDENTIFIER', 'NOTENAME_PITCH', 'TONICNAME_PITCH',
            'UNSIGNED', 'REAL', 'DURATION_IDENTIFIER', ':'),
        ('nonassoc', 'NUMBER_IDENTIFIER', '/'),
        ('left', '+', '-'),
        # ('left', 'UNARY_MINUS')
        )

    ### INITIALIZER ###

    def __init__(self, client=None):
        self.client = client
        if client is not None:
            self.tokens = self.client._lexdef.tokens
        else:
            self.tokens = []

    ### SYNTACTICAL RULES (ALPHABETICAL) ###

    def p_start_symbol__EMBEDDED_LILY__embedded_lilypond(self, production):
        'start_symbol : EMBEDDED_LILY embedded_lilypond'
        production[0] = SyntaxNode('start_symbol', production[1:])

    def p_start_symbol__lilypond(self, production):
        'start_symbol : lilypond'
        production[0] = SyntaxNode('start_symbol', production[1:])

    ### assignment ###

    def p_assignment__assignment_id__Chr46__property_path__Chr61__identifier_init(self, production):
        "assignment : assignment_id '.' property_path '=' identifier_init"
        production[0] = SyntaxNode('assignment', production[1:])

    def p_assignment__assignment_id__Chr61__identifier_init(self, production):
        "assignment : assignment_id '=' identifier_init"
        production[0] = SyntaxNode('assignment', production[1:])

    def p_assignment__assignment_id__property_path__Chr61__identifier_init(self, production):
        "assignment : assignment_id property_path '=' identifier_init"
        production[0] = SyntaxNode('assignment', production[1:])

    ### assignment_id ###

    def p_assignment_id__STRING(self, production):
        'assignment_id : STRING'
        production[0] = SyntaxNode('assignment_id', production[1:])

    ### bare_number ###

    def p_bare_number__UNSIGNED(self, production):
        'bare_number : UNSIGNED'
        production[0] = SyntaxNode('bare_number', production[1:])

    def p_bare_number__UNSIGNED__NUMBER_IDENTIFIER(self, production):
        'bare_number : UNSIGNED NUMBER_IDENTIFIER'
        production[0] = SyntaxNode('bare_number', production[1:])

    def p_bare_number__bare_number_common(self, production):
        'bare_number : bare_number_common'
        production[0] = SyntaxNode('bare_number', production[1:])

    ### bare_number_common ###

    def p_bare_number_common__NUMBER_IDENTIFIER(self, production):
        'bare_number_common : NUMBER_IDENTIFIER'
        production[0] = SyntaxNode('bare_number_common', production[1:])

    def p_bare_number_common__REAL(self, production):
        'bare_number_common : REAL'
        production[0] = SyntaxNode('bare_number_common', production[1:])

    def p_bare_number_common__REAL__NUMBER_IDENTIFIER(self, production):
        'bare_number_common : REAL NUMBER_IDENTIFIER'
        production[0] = SyntaxNode('bare_number_common', production[1:])

    ### basic_music ###

    def p_basic_music__LYRICSTO__simple_string__lyric_mode_music(self, production):
        'basic_music : LYRICSTO simple_string lyric_mode_music'
        production[0] = SyntaxNode('basic_music', production[1:])

    def p_basic_music__LYRICSTO__symbol__Chr61__simple_string__lyric_mode_music(self, production):
        "basic_music : LYRICSTO symbol '=' simple_string lyric_mode_music"
        production[0] = SyntaxNode('basic_music', production[1:])

    def p_basic_music__music_bare(self, production):
        'basic_music : music_bare'
        production[0] = SyntaxNode('basic_music', production[1:])

    def p_basic_music__music_function_call(self, production):
        'basic_music : music_function_call'
        production[0] = SyntaxNode('basic_music', production[1:])

    def p_basic_music__repeated_music(self, production):
        'basic_music : repeated_music'
        production[0] = SyntaxNode('basic_music', production[1:])

    ### bass_figure ###

    def p_bass_figure__FIGURE_SPACE(self, production):
        'bass_figure : FIGURE_SPACE'
        production[0] = SyntaxNode('bass_figure', production[1:])

    def p_bass_figure__bass_figure__Chr93(self, production):
        "bass_figure : bass_figure ']'"
        production[0] = SyntaxNode('bass_figure', production[1:])

    def p_bass_figure__bass_figure__figured_bass_alteration(self, production):
        'bass_figure : bass_figure figured_bass_alteration'
        production[0] = SyntaxNode('bass_figure', production[1:])

    def p_bass_figure__bass_figure__figured_bass_modification(self, production):
        'bass_figure : bass_figure figured_bass_modification'
        production[0] = SyntaxNode('bass_figure', production[1:])

    def p_bass_figure__bass_number(self, production):
        'bass_figure : bass_number'
        production[0] = SyntaxNode('bass_figure', production[1:])

    ### bass_number ###

    def p_bass_number__STRING(self, production):
        'bass_number : STRING'
        production[0] = SyntaxNode('bass_number', production[1:])

    def p_bass_number__UNSIGNED(self, production):
        'bass_number : UNSIGNED'
        production[0] = SyntaxNode('bass_number', production[1:])

    def p_bass_number__embedded_scm_bare(self, production):
        'bass_number : embedded_scm_bare'
        production[0] = SyntaxNode('bass_number', production[1:])

    def p_bass_number__full_markup(self, production):
        'bass_number : full_markup'
        production[0] = SyntaxNode('bass_number', production[1:])

    ### book_block ###

    def p_book_block__BOOK__Chr123__book_body__Chr125(self, production):
        "book_block : BOOK '{' book_body '}'"
        production[0] = SyntaxNode('book_block', production[1:])

    ### book_body ###

    def p_book_body__BOOK_IDENTIFIER(self, production):
        'book_body : BOOK_IDENTIFIER'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__Empty(self, production):
        'book_body : '
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__SCM_TOKEN(self, production):
        'book_body : book_body SCM_TOKEN'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__bookpart_block(self, production):
        'book_body : book_body bookpart_block'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__composite_music(self, production):
        'book_body : book_body composite_music'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__embedded_scm_active(self, production):
        'book_body : book_body embedded_scm_active'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__error(self, production):
        'book_body : book_body error'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__full_markup(self, production):
        'book_body : book_body full_markup'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__full_markup_list(self, production):
        'book_body : book_body full_markup_list'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__lilypond_header(self, production):
        'book_body : book_body lilypond_header'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__paper_block(self, production):
        'book_body : book_body paper_block'
        production[0] = SyntaxNode('book_body', production[1:])

    def p_book_body__book_body__score_block(self, production):
        'book_body : book_body score_block'
        production[0] = SyntaxNode('book_body', production[1:])

    ### bookpart_block ###

    def p_bookpart_block__BOOKPART__Chr123__bookpart_body__Chr125(self, production):
        "bookpart_block : BOOKPART '{' bookpart_body '}'"
        production[0] = SyntaxNode('bookpart_block', production[1:])

    ### bookpart_body ###

    def p_bookpart_body__BOOK_IDENTIFIER(self, production):
        'bookpart_body : BOOK_IDENTIFIER'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__Empty(self, production):
        'bookpart_body : '
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__SCM_TOKEN(self, production):
        'bookpart_body : bookpart_body SCM_TOKEN'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__composite_music(self, production):
        'bookpart_body : bookpart_body composite_music'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__embedded_scm_active(self, production):
        'bookpart_body : bookpart_body embedded_scm_active'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__error(self, production):
        'bookpart_body : bookpart_body error'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__full_markup(self, production):
        'bookpart_body : bookpart_body full_markup'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__full_markup_list(self, production):
        'bookpart_body : bookpart_body full_markup_list'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__lilypond_header(self, production):
        'bookpart_body : bookpart_body lilypond_header'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__paper_block(self, production):
        'bookpart_body : bookpart_body paper_block'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    def p_bookpart_body__bookpart_body__score_block(self, production):
        'bookpart_body : bookpart_body score_block'
        production[0] = SyntaxNode('bookpart_body', production[1:])

    ### br_bass_figure ###

    def p_br_bass_figure__Chr91__bass_figure(self, production):
        "br_bass_figure : '[' bass_figure"
        production[0] = SyntaxNode('br_bass_figure', production[1:])

    def p_br_bass_figure__bass_figure(self, production):
        'br_bass_figure : bass_figure'
        production[0] = SyntaxNode('br_bass_figure', production[1:])

    ### braced_music_list ###

    def p_braced_music_list__Chr123__music_list__Chr125(self, production):
        "braced_music_list : '{' music_list '}'"
        production[0] = SyntaxNode('braced_music_list', production[1:])

    ### chord_body ###

    def p_chord_body__ANGLE_OPEN__chord_body_elements__ANGLE_CLOSE(self, production):
        'chord_body : ANGLE_OPEN chord_body_elements ANGLE_CLOSE'
        production[0] = SyntaxNode('chord_body', production[1:])

    def p_chord_body__FIGURE_OPEN__figure_list__FIGURE_CLOSE(self, production):
        'chord_body : FIGURE_OPEN figure_list FIGURE_CLOSE'
        production[0] = SyntaxNode('chord_body', production[1:])

    ### chord_body_element ###

    def p_chord_body_element__DRUM_PITCH__post_events(self, production):
        'chord_body_element : DRUM_PITCH post_events'
        production[0] = SyntaxNode('chord_body_element', production[1:])

    def p_chord_body_element__music_function_chord_body(self, production):
        'chord_body_element : music_function_chord_body'
        production[0] = SyntaxNode('chord_body_element', production[1:])

    def p_chord_body_element__pitch_or_tonic_pitch__exclamations__questions__octave_check__post_events(self, production):
        'chord_body_element : pitch_or_tonic_pitch exclamations questions octave_check post_events'
        production[0] = SyntaxNode('chord_body_element', production[1:])

    ### chord_body_elements ###

    def p_chord_body_elements__Empty(self, production):
        'chord_body_elements : '
        production[0] = SyntaxNode('chord_body_elements', production[1:])

    def p_chord_body_elements__chord_body_elements__chord_body_element(self, production):
        'chord_body_elements : chord_body_elements chord_body_element'
        production[0] = SyntaxNode('chord_body_elements', production[1:])

    ### chord_item ###

    def p_chord_item__CHORD_MODIFIER(self, production):
        'chord_item : CHORD_MODIFIER'
        production[0] = SyntaxNode('chord_item', production[1:])

    def p_chord_item__chord_separator(self, production):
        'chord_item : chord_separator'
        production[0] = SyntaxNode('chord_item', production[1:])

    def p_chord_item__step_numbers(self, production):
        'chord_item : step_numbers'
        production[0] = SyntaxNode('chord_item', production[1:])

    ### chord_items ###

    def p_chord_items__Empty(self, production):
        'chord_items : '
        production[0] = SyntaxNode('chord_items', production[1:])

    def p_chord_items__chord_items__chord_item(self, production):
        'chord_items : chord_items chord_item'
        production[0] = SyntaxNode('chord_items', production[1:])

    ### chord_separator ###

    def p_chord_separator__CHORD_BASS__steno_tonic_pitch(self, production):
        'chord_separator : CHORD_BASS steno_tonic_pitch'
        production[0] = SyntaxNode('chord_separator', production[1:])

    def p_chord_separator__CHORD_CARET(self, production):
        'chord_separator : CHORD_CARET'
        production[0] = SyntaxNode('chord_separator', production[1:])

    def p_chord_separator__CHORD_COLON(self, production):
        'chord_separator : CHORD_COLON'
        production[0] = SyntaxNode('chord_separator', production[1:])

    def p_chord_separator__CHORD_SLASH__steno_tonic_pitch(self, production):
        'chord_separator : CHORD_SLASH steno_tonic_pitch'
        production[0] = SyntaxNode('chord_separator', production[1:])

    ### composite_music ###

    def p_composite_music__basic_music(self, production):
        'composite_music : basic_music'
        production[0] = SyntaxNode('composite_music', production[1:])

    def p_composite_music__basic_music__new_lyrics(self, production):
        'composite_music : basic_music new_lyrics'
        production[0] = SyntaxNode('composite_music', production[1:])

    def p_composite_music__contexted_basic_music(self, production):
        'composite_music : contexted_basic_music'
        production[0] = SyntaxNode('composite_music', production[1:])

    ### context_change ###

    def p_context_change__CHANGE__symbol__Chr61__simple_string(self, production):
        "context_change : CHANGE symbol '=' simple_string"
        production[0] = SyntaxNode('context_change', production[1:])

    ### context_def_mod ###

    def p_context_def_mod__ACCEPTS(self, production):
        'context_def_mod : ACCEPTS'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__ALIAS(self, production):
        'context_def_mod : ALIAS'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__CONSISTS(self, production):
        'context_def_mod : CONSISTS'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__DEFAULTCHILD(self, production):
        'context_def_mod : DEFAULTCHILD'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__DENIES(self, production):
        'context_def_mod : DENIES'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__DESCRIPTION(self, production):
        'context_def_mod : DESCRIPTION'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__NAME(self, production):
        'context_def_mod : NAME'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__REMOVE(self, production):
        'context_def_mod : REMOVE'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    def p_context_def_mod__TYPE(self, production):
        'context_def_mod : TYPE'
        production[0] = SyntaxNode('context_def_mod', production[1:])

    ### context_def_spec_block ###

    def p_context_def_spec_block__CONTEXT__Chr123__context_def_spec_body__Chr125(self, production):
        "context_def_spec_block : CONTEXT '{' context_def_spec_body '}'"
        production[0] = SyntaxNode('context_def_spec_block', production[1:])

    ### context_def_spec_body ###

    def p_context_def_spec_body__Empty(self, production):
        'context_def_spec_body : '
        production[0] = SyntaxNode('context_def_spec_body', production[1:])

    def p_context_def_spec_body__context_def_spec_body__context_mod(self, production):
        'context_def_spec_body : context_def_spec_body context_mod'
        production[0] = SyntaxNode('context_def_spec_body', production[1:])

    def p_context_def_spec_body__context_def_spec_body__context_mod_arg(self, production):
        'context_def_spec_body : context_def_spec_body context_mod_arg'
        production[0] = SyntaxNode('context_def_spec_body', production[1:])

    def p_context_def_spec_body__context_def_spec_body__context_modification(self, production):
        'context_def_spec_body : context_def_spec_body context_modification'
        production[0] = SyntaxNode('context_def_spec_body', production[1:])

    ### context_mod ###

    def p_context_mod__context_def_mod__STRING(self, production):
        'context_mod : context_def_mod STRING'
        production[0] = SyntaxNode('context_mod', production[1:])

    def p_context_mod__context_def_mod__embedded_scm(self, production):
        'context_mod : context_def_mod embedded_scm'
        production[0] = SyntaxNode('context_mod', production[1:])

    def p_context_mod__property_operation(self, production):
        'context_mod : property_operation'
        production[0] = SyntaxNode('context_mod', production[1:])

    ### context_mod_arg ###

    def p_context_mod_arg__composite_music(self, production):
        'context_mod_arg : composite_music'
        production[0] = SyntaxNode('context_mod_arg', production[1:])

    def p_context_mod_arg__embedded_scm(self, production):
        'context_mod_arg : embedded_scm'
        production[0] = SyntaxNode('context_mod_arg', production[1:])

    ### context_mod_list ###

    def p_context_mod_list__Empty(self, production):
        'context_mod_list : '
        production[0] = SyntaxNode('context_mod_list', production[1:])

    def p_context_mod_list__context_mod_list__CONTEXT_MOD_IDENTIFIER(self, production):
        'context_mod_list : context_mod_list CONTEXT_MOD_IDENTIFIER'
        production[0] = SyntaxNode('context_mod_list', production[1:])

    def p_context_mod_list__context_mod_list__context_mod(self, production):
        'context_mod_list : context_mod_list context_mod'
        production[0] = SyntaxNode('context_mod_list', production[1:])

    def p_context_mod_list__context_mod_list__context_mod_arg(self, production):
        'context_mod_list : context_mod_list context_mod_arg'
        production[0] = SyntaxNode('context_mod_list', production[1:])

    ### context_modification ###

    def p_context_modification__CONTEXT_MOD_IDENTIFIER(self, production):
        'context_modification : CONTEXT_MOD_IDENTIFIER'
        production[0] = SyntaxNode('context_modification', production[1:])

    def p_context_modification__WITH__CONTEXT_MOD_IDENTIFIER(self, production):
        'context_modification : WITH CONTEXT_MOD_IDENTIFIER'
        production[0] = SyntaxNode('context_modification', production[1:])

    def p_context_modification__WITH__Chr123__context_mod_list__Chr125(self, production):
        "context_modification : WITH '{' context_mod_list '}'"
        production[0] = SyntaxNode('context_modification', production[1:])

    def p_context_modification__WITH__context_modification_arg(self, production):
        'context_modification : WITH context_modification_arg'
        production[0] = SyntaxNode('context_modification', production[1:])

    ### context_modification_arg ###

    def p_context_modification_arg__MUSIC_IDENTIFIER(self, production):
        'context_modification_arg : MUSIC_IDENTIFIER'
        production[0] = SyntaxNode('context_modification_arg', production[1:])

    def p_context_modification_arg__embedded_scm(self, production):
        'context_modification_arg : embedded_scm'
        production[0] = SyntaxNode('context_modification_arg', production[1:])

    ### context_prefix ###

    def p_context_prefix__CONTEXT__symbol__optional_id__optional_context_mod(self, production):
        'context_prefix : CONTEXT symbol optional_id optional_context_mod'
        production[0] = SyntaxNode('context_prefix', production[1:])

    def p_context_prefix__NEWCONTEXT__symbol__optional_id__optional_context_mod(self, production):
        'context_prefix : NEWCONTEXT symbol optional_id optional_context_mod'
        production[0] = SyntaxNode('context_prefix', production[1:])

    ### context_prop_spec ###

    def p_context_prop_spec__symbol_list_rev(self, production):
        'context_prop_spec : symbol_list_rev'
        production[0] = SyntaxNode('context_prop_spec', production[1:])

    ### contextable_music ###

    def p_contextable_music__basic_music(self, production):
        'contextable_music : basic_music'
        production[0] = SyntaxNode('contextable_music', production[1:])

    def p_contextable_music__event_chord(self, production):
        'contextable_music : event_chord'
        production[0] = SyntaxNode('contextable_music', production[1:])

    def p_contextable_music__pitch_as_music(self, production):
        'contextable_music : pitch_as_music'
        production[0] = SyntaxNode('contextable_music', production[1:])

    ### contexted_basic_music ###

    def p_contexted_basic_music__context_prefix__contextable_music(self, production):
        'contexted_basic_music : context_prefix contextable_music'
        production[0] = SyntaxNode('contexted_basic_music', production[1:])

    def p_contexted_basic_music__context_prefix__contextable_music__new_lyrics(self, production):
        'contexted_basic_music : context_prefix contextable_music new_lyrics'
        production[0] = SyntaxNode('contexted_basic_music', production[1:])

    def p_contexted_basic_music__context_prefix__contexted_basic_music(self, production):
        'contexted_basic_music : context_prefix contexted_basic_music'
        production[0] = SyntaxNode('contexted_basic_music', production[1:])

    ### direction_less_event ###

    def p_direction_less_event__EVENT_IDENTIFIER(self, production):
        'direction_less_event : EVENT_IDENTIFIER'
        production[0] = SyntaxNode('direction_less_event', production[1:])

    def p_direction_less_event__event_function_event(self, production):
        'direction_less_event : event_function_event'
        production[0] = SyntaxNode('direction_less_event', production[1:])

    def p_direction_less_event__string_number_event(self, production):
        'direction_less_event : string_number_event'
        production[0] = SyntaxNode('direction_less_event', production[1:])

    def p_direction_less_event__tremolo_type(self, production):
        'direction_less_event : tremolo_type'
        production[0] = SyntaxNode('direction_less_event', production[1:])

    ### direction_reqd_event ###

    def p_direction_reqd_event__gen_text_def(self, production):
        'direction_reqd_event : gen_text_def'
        production[0] = SyntaxNode('direction_reqd_event', production[1:])

    def p_direction_reqd_event__script_abbreviation(self, production):
        'direction_reqd_event : script_abbreviation'
        production[0] = SyntaxNode('direction_reqd_event', production[1:])

    ### dots ###

    def p_dots__Empty(self, production):
        'dots : '
        production[0] = SyntaxNode('dots', production[1:])

    def p_dots__dots__Chr46(self, production):
        "dots : dots '.'"
        production[0] = SyntaxNode('dots', production[1:])

    ### duration_length ###

    def p_duration_length__multiplied_duration(self, production):
        'duration_length : multiplied_duration'
        production[0] = SyntaxNode('duration_length', production[1:])

    ### embedded_lilypond ###

    def p_embedded_lilypond__Empty(self, production):
        'embedded_lilypond : '
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__INVALID__embedded_lilypond(self, production):
        'embedded_lilypond : INVALID embedded_lilypond'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__embedded_lilypond_number(self, production):
        'embedded_lilypond : embedded_lilypond_number'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__error(self, production):
        'embedded_lilypond : error'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__identifier_init_nonumber(self, production):
        'embedded_lilypond : identifier_init_nonumber'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__multiplied_duration(self, production):
        'embedded_lilypond : multiplied_duration'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__music_embedded__music_embedded__music_list(self, production):
        'embedded_lilypond : music_embedded music_embedded music_list'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    def p_embedded_lilypond__post_event__post_events(self, production):
        'embedded_lilypond : post_event post_events'
        production[0] = SyntaxNode('embedded_lilypond', production[1:])

    ### embedded_lilypond_number ###

    def p_embedded_lilypond_number__Chr45__embedded_lilypond_number(self, production):
        "embedded_lilypond_number : '-' embedded_lilypond_number"
        production[0] = SyntaxNode('embedded_lilypond_number', production[1:])

    def p_embedded_lilypond_number__UNSIGNED__NUMBER_IDENTIFIER(self, production):
        'embedded_lilypond_number : UNSIGNED NUMBER_IDENTIFIER'
        production[0] = SyntaxNode('embedded_lilypond_number', production[1:])

    def p_embedded_lilypond_number__bare_number_common(self, production):
        'embedded_lilypond_number : bare_number_common'
        production[0] = SyntaxNode('embedded_lilypond_number', production[1:])

    ### embedded_scm ###

    def p_embedded_scm__embedded_scm_bare(self, production):
        'embedded_scm : embedded_scm_bare'
        production[0] = SyntaxNode('embedded_scm', production[1:])

    def p_embedded_scm__scm_function_call(self, production):
        'embedded_scm : scm_function_call'
        production[0] = SyntaxNode('embedded_scm', production[1:])

    ### embedded_scm_active ###

    def p_embedded_scm_active__SCM_IDENTIFIER(self, production):
        'embedded_scm_active : SCM_IDENTIFIER'
        production[0] = SyntaxNode('embedded_scm_active', production[1:])

    def p_embedded_scm_active__scm_function_call(self, production):
        'embedded_scm_active : scm_function_call'
        production[0] = SyntaxNode('embedded_scm_active', production[1:])

    ### embedded_scm_arg ###

    def p_embedded_scm_arg__embedded_scm_bare_arg(self, production):
        'embedded_scm_arg : embedded_scm_bare_arg'
        production[0] = SyntaxNode('embedded_scm_arg', production[1:])

    def p_embedded_scm_arg__music_assign(self, production):
        'embedded_scm_arg : music_assign'
        production[0] = SyntaxNode('embedded_scm_arg', production[1:])

    def p_embedded_scm_arg__scm_function_call(self, production):
        'embedded_scm_arg : scm_function_call'
        production[0] = SyntaxNode('embedded_scm_arg', production[1:])

    ### embedded_scm_bare ###

    def p_embedded_scm_bare__SCM_IDENTIFIER(self, production):
        'embedded_scm_bare : SCM_IDENTIFIER'
        production[0] = SyntaxNode('embedded_scm_bare', production[1:])

    def p_embedded_scm_bare__SCM_TOKEN(self, production):
        'embedded_scm_bare : SCM_TOKEN'
        production[0] = SyntaxNode('embedded_scm_bare', production[1:])

    ### embedded_scm_bare_arg ###

    def p_embedded_scm_bare_arg__FRACTION(self, production):
        'embedded_scm_bare_arg : FRACTION'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__SCM_ARG(self, production):
        'embedded_scm_bare_arg : SCM_ARG'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__SCM_TOKEN(self, production):
        'embedded_scm_bare_arg : SCM_TOKEN'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__book_block(self, production):
        'embedded_scm_bare_arg : book_block'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__bookpart_block(self, production):
        'embedded_scm_bare_arg : bookpart_block'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__context_def_spec_block(self, production):
        'embedded_scm_bare_arg : context_def_spec_block'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__context_modification(self, production):
        'embedded_scm_bare_arg : context_modification'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__full_markup_list(self, production):
        'embedded_scm_bare_arg : full_markup_list'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__output_def(self, production):
        'embedded_scm_bare_arg : output_def'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__partial_markup(self, production):
        'embedded_scm_bare_arg : partial_markup'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    def p_embedded_scm_bare_arg__score_block(self, production):
        'embedded_scm_bare_arg : score_block'
        production[0] = SyntaxNode('embedded_scm_bare_arg', production[1:])

    ### event_chord ###

    def p_event_chord__CHORD_REPETITION__optional_notemode_duration__post_events(self, production):
        'event_chord : CHORD_REPETITION optional_notemode_duration post_events'
        production[0] = SyntaxNode('event_chord', production[1:])

    def p_event_chord__MULTI_MEASURE_REST__optional_notemode_duration__post_events(self, production):
        'event_chord : MULTI_MEASURE_REST optional_notemode_duration post_events'
        production[0] = SyntaxNode('event_chord', production[1:])

    def p_event_chord__note_chord_element(self, production):
        'event_chord : note_chord_element'
        production[0] = SyntaxNode('event_chord', production[1:])

    def p_event_chord__simple_element__post_events(self, production):
        'event_chord : simple_element post_events'
        production[0] = SyntaxNode('event_chord', production[1:])

    def p_event_chord__tempo_event(self, production):
        'event_chord : tempo_event'
        production[0] = SyntaxNode('event_chord', production[1:])

    ### event_function_event ###

    def p_event_function_event__EVENT_FUNCTION__function_arglist(self, production):
        'event_function_event : EVENT_FUNCTION function_arglist'
        production[0] = SyntaxNode('event_function_event', production[1:])

    ### exclamations ###

    def p_exclamations__Empty(self, production):
        'exclamations : '
        production[0] = SyntaxNode('exclamations', production[1:])

    def p_exclamations__exclamations__Chr33(self, production):
        "exclamations : exclamations '!'"
        production[0] = SyntaxNode('exclamations', production[1:])

    ### figure_list ###

    def p_figure_list__Empty(self, production):
        'figure_list : '
        production[0] = SyntaxNode('figure_list', production[1:])

    def p_figure_list__figure_list__br_bass_figure(self, production):
        'figure_list : figure_list br_bass_figure'
        production[0] = SyntaxNode('figure_list', production[1:])

    ### figured_bass_alteration ###

    def p_figured_bass_alteration__Chr33(self, production):
        "figured_bass_alteration : '!'"
        production[0] = SyntaxNode('figured_bass_alteration', production[1:])

    def p_figured_bass_alteration__Chr43(self, production):
        "figured_bass_alteration : '+'"
        production[0] = SyntaxNode('figured_bass_alteration', production[1:])

    def p_figured_bass_alteration__Chr45(self, production):
        "figured_bass_alteration : '-'"
        production[0] = SyntaxNode('figured_bass_alteration', production[1:])

    ### figured_bass_modification ###

    def p_figured_bass_modification__Chr47(self, production):
        "figured_bass_modification : '/'"
        production[0] = SyntaxNode('figured_bass_modification', production[1:])

    def p_figured_bass_modification__E_BACKSLASH(self, production):
        'figured_bass_modification : E_BACKSLASH'
        production[0] = SyntaxNode('figured_bass_modification', production[1:])

    def p_figured_bass_modification__E_EXCLAMATION(self, production):
        'figured_bass_modification : E_EXCLAMATION'
        production[0] = SyntaxNode('figured_bass_modification', production[1:])

    def p_figured_bass_modification__E_PLUS(self, production):
        'figured_bass_modification : E_PLUS'
        production[0] = SyntaxNode('figured_bass_modification', production[1:])

    ### fingering ###

    def p_fingering__UNSIGNED(self, production):
        'fingering : UNSIGNED'
        production[0] = SyntaxNode('fingering', production[1:])

    ### full_markup ###

    def p_full_markup__markup_mode__markup_top(self, production):
        'full_markup : markup_mode markup_top'
        production[0] = SyntaxNode('full_markup', production[1:])

    ### full_markup_list ###

    def p_full_markup_list__MARKUPLIST__markup_list(self, production):
        'full_markup_list : MARKUPLIST markup_list'
        production[0] = SyntaxNode('full_markup_list', production[1:])

    ### function_arglist ###

    def p_function_arglist__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip_nonbackup__DEFAULT(self, production):
        'function_arglist : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip_nonbackup DEFAULT'
        production[0] = SyntaxNode('function_arglist', production[1:])

    def p_function_arglist__function_arglist_nonbackup(self, production):
        'function_arglist : function_arglist_nonbackup'
        production[0] = SyntaxNode('function_arglist', production[1:])

    ### function_arglist_backup ###

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__Chr45__NUMBER_IDENTIFIER(self, production):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup '-' NUMBER_IDENTIFIER"
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__Chr45__REAL(self, production):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup '-' REAL"
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__Chr45__UNSIGNED(self, production):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup '-' UNSIGNED"
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__DURATION_IDENTIFIER(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup DURATION_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__NUMBER_IDENTIFIER(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup NUMBER_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__REAL(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup REAL'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__SCM_IDENTIFIER(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup SCM_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__STRING(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup STRING'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__UNSIGNED(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup UNSIGNED'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__embedded_scm_arg(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup embedded_scm_arg'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__full_markup(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup full_markup'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__pitch(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup pitch'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__post_event_nofinger(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup post_event_nofinger'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__steno_tonic_pitch(self, production):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup steno_tonic_pitch'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__bare_number_common(self, production):
        'function_arglist_backup : function_arglist_backup REPARSE bare_number_common'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__duration_length(self, production):
        'function_arglist_backup : function_arglist_backup REPARSE duration_length'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__pitch_or_music(self, production):
        'function_arglist_backup : function_arglist_backup REPARSE pitch_or_music'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__function_arglist_backup__REPARSE__symbol_list_arg(self, production):
        'function_arglist_backup : function_arglist_backup REPARSE symbol_list_arg'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    def p_function_arglist_backup__function_arglist_common(self, production):
        'function_arglist_backup : function_arglist_common'
        production[0] = SyntaxNode('function_arglist_backup', production[1:])

    ### function_arglist_common ###

    def p_function_arglist_common__EXPECT_NO_MORE_ARGS(self, production):
        'function_arglist_common : EXPECT_NO_MORE_ARGS'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__EXPECT_SCM__function_arglist_optional__Chr45__NUMBER_IDENTIFIER(self, production):
        "function_arglist_common : EXPECT_SCM function_arglist_optional '-' NUMBER_IDENTIFIER"
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__EXPECT_SCM__function_arglist_optional__bare_number_common(self, production):
        'function_arglist_common : EXPECT_SCM function_arglist_optional bare_number_common'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg(self, production):
        'function_arglist_common : EXPECT_SCM function_arglist_optional embedded_scm_arg'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__EXPECT_SCM__function_arglist_optional__post_event_nofinger(self, production):
        'function_arglist_common : EXPECT_SCM function_arglist_optional post_event_nofinger'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__function_arglist_common_reparse__REPARSE__SCM_ARG(self, production):
        'function_arglist_common : function_arglist_common_reparse REPARSE SCM_ARG'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__function_arglist_common_reparse__REPARSE__bare_number_common(self, production):
        'function_arglist_common : function_arglist_common_reparse REPARSE bare_number_common'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__function_arglist_common_reparse__REPARSE__duration_length(self, production):
        'function_arglist_common : function_arglist_common_reparse REPARSE duration_length'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__function_arglist_common_reparse__REPARSE__lyric_element_music(self, production):
        'function_arglist_common : function_arglist_common_reparse REPARSE lyric_element_music'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__function_arglist_common_reparse__REPARSE__pitch_or_music(self, production):
        'function_arglist_common : function_arglist_common_reparse REPARSE pitch_or_music'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    def p_function_arglist_common__function_arglist_common_reparse__REPARSE__symbol_list_arg(self, production):
        'function_arglist_common : function_arglist_common_reparse REPARSE symbol_list_arg'
        production[0] = SyntaxNode('function_arglist_common', production[1:])

    ### function_arglist_common_reparse ###

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__Chr45__REAL(self, production):
        "function_arglist_common_reparse : EXPECT_SCM function_arglist_optional '-' REAL"
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__Chr45__UNSIGNED(self, production):
        "function_arglist_common_reparse : EXPECT_SCM function_arglist_optional '-' UNSIGNED"
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__DURATION_IDENTIFIER(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional DURATION_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__SCM_IDENTIFIER(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional SCM_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__STRING(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional STRING'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__UNSIGNED(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional UNSIGNED'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__full_markup(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional full_markup'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__pitch(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional pitch'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    def p_function_arglist_common_reparse__EXPECT_SCM__function_arglist_optional__steno_tonic_pitch(self, production):
        'function_arglist_common_reparse : EXPECT_SCM function_arglist_optional steno_tonic_pitch'
        production[0] = SyntaxNode('function_arglist_common_reparse', production[1:])

    ### function_arglist_nonbackup ###

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__Chr45__NUMBER_IDENTIFIER(self, production):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup '-' NUMBER_IDENTIFIER"
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__Chr45__REAL(self, production):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup '-' REAL"
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__Chr45__UNSIGNED(self, production):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup '-' UNSIGNED"
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__bare_number_common(self, production):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup bare_number_common'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__embedded_scm_arg(self, production):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup embedded_scm_arg'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__post_event_nofinger(self, production):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup post_event_nofinger'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_common(self, production):
        'function_arglist_nonbackup : function_arglist_common'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_nonbackup_reparse__REPARSE__SCM_ARG(self, production):
        'function_arglist_nonbackup : function_arglist_nonbackup_reparse REPARSE SCM_ARG'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_nonbackup_reparse__REPARSE__bare_number_common(self, production):
        'function_arglist_nonbackup : function_arglist_nonbackup_reparse REPARSE bare_number_common'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_nonbackup_reparse__REPARSE__duration_length(self, production):
        'function_arglist_nonbackup : function_arglist_nonbackup_reparse REPARSE duration_length'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_nonbackup_reparse__REPARSE__lyric_element_music(self, production):
        'function_arglist_nonbackup : function_arglist_nonbackup_reparse REPARSE lyric_element_music'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_nonbackup_reparse__REPARSE__pitch_or_music(self, production):
        'function_arglist_nonbackup : function_arglist_nonbackup_reparse REPARSE pitch_or_music'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    def p_function_arglist_nonbackup__function_arglist_nonbackup_reparse__REPARSE__symbol_list_arg(self, production):
        'function_arglist_nonbackup : function_arglist_nonbackup_reparse REPARSE symbol_list_arg'
        production[0] = SyntaxNode('function_arglist_nonbackup', production[1:])

    ### function_arglist_nonbackup_reparse ###

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__DURATION_IDENTIFIER(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup DURATION_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__SCM_IDENTIFIER(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup SCM_IDENTIFIER'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__STRING(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup STRING'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__UNSIGNED(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup UNSIGNED'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__full_markup(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup full_markup'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__pitch(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup pitch'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    def p_function_arglist_nonbackup_reparse__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__steno_tonic_pitch(self, production):
        'function_arglist_nonbackup_reparse : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup steno_tonic_pitch'
        production[0] = SyntaxNode('function_arglist_nonbackup_reparse', production[1:])

    ### function_arglist_optional ###

    def p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip_backup__DEFAULT(self, production):
        'function_arglist_optional : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip_backup DEFAULT'
        production[0] = SyntaxNode('function_arglist_optional', production[1:])

    def p_function_arglist_optional__function_arglist_backup(self, production):
        'function_arglist_optional : function_arglist_backup'
        production[0] = SyntaxNode('function_arglist_optional', production[1:])

    def p_function_arglist_optional__function_arglist_skip_backup__BACKUP(self, production):
        'function_arglist_optional : function_arglist_skip_backup BACKUP'
        production[0] = SyntaxNode('function_arglist_optional', production[1:])

    ### function_arglist_partial ###

    def p_function_arglist_partial__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup(self, production):
        'function_arglist_partial : EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup'
        production[0] = SyntaxNode('function_arglist_partial', production[1:])

    def p_function_arglist_partial__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_partial(self, production):
        'function_arglist_partial : EXPECT_OPTIONAL EXPECT_SCM function_arglist_partial'
        production[0] = SyntaxNode('function_arglist_partial', production[1:])

    def p_function_arglist_partial__EXPECT_SCM__function_arglist_optional(self, production):
        'function_arglist_partial : EXPECT_SCM function_arglist_optional'
        production[0] = SyntaxNode('function_arglist_partial', production[1:])

    def p_function_arglist_partial__EXPECT_SCM__function_arglist_partial_optional(self, production):
        'function_arglist_partial : EXPECT_SCM function_arglist_partial_optional'
        production[0] = SyntaxNode('function_arglist_partial', production[1:])

    ### function_arglist_partial_optional ###

    def p_function_arglist_partial_optional__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup(self, production):
        'function_arglist_partial_optional : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup'
        production[0] = SyntaxNode('function_arglist_partial_optional', production[1:])

    def p_function_arglist_partial_optional__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_partial_optional(self, production):
        'function_arglist_partial_optional : EXPECT_OPTIONAL EXPECT_SCM function_arglist_partial_optional'
        production[0] = SyntaxNode('function_arglist_partial_optional', production[1:])

    def p_function_arglist_partial_optional__EXPECT_SCM__function_arglist_optional(self, production):
        'function_arglist_partial_optional : EXPECT_SCM function_arglist_optional'
        production[0] = SyntaxNode('function_arglist_partial_optional', production[1:])

    def p_function_arglist_partial_optional__EXPECT_SCM__function_arglist_partial_optional(self, production):
        'function_arglist_partial_optional : EXPECT_SCM function_arglist_partial_optional'
        production[0] = SyntaxNode('function_arglist_partial_optional', production[1:])

    ### function_arglist_skip_backup ###

    def p_function_arglist_skip_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip_backup(self, production):
        'function_arglist_skip_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip_backup'
        production[0] = SyntaxNode('function_arglist_skip_backup', production[1:])

    def p_function_arglist_skip_backup__function_arglist_backup(self, production):
        'function_arglist_skip_backup : function_arglist_backup'
        production[0] = SyntaxNode('function_arglist_skip_backup', production[1:])

    ### function_arglist_skip_nonbackup ###

    def p_function_arglist_skip_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip_nonbackup(self, production):
        'function_arglist_skip_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip_nonbackup'
        production[0] = SyntaxNode('function_arglist_skip_nonbackup', production[1:])

    def p_function_arglist_skip_nonbackup__function_arglist_nonbackup(self, production):
        'function_arglist_skip_nonbackup : function_arglist_nonbackup'
        production[0] = SyntaxNode('function_arglist_skip_nonbackup', production[1:])

    ### gen_text_def ###

    def p_gen_text_def__STRING(self, production):
        'gen_text_def : STRING'
        production[0] = SyntaxNode('gen_text_def', production[1:])

    def p_gen_text_def__embedded_scm(self, production):
        'gen_text_def : embedded_scm'
        production[0] = SyntaxNode('gen_text_def', production[1:])

    def p_gen_text_def__full_markup(self, production):
        'gen_text_def : full_markup'
        production[0] = SyntaxNode('gen_text_def', production[1:])

    ### grob_prop_path ###

    def p_grob_prop_path__grob_prop_spec(self, production):
        'grob_prop_path : grob_prop_spec'
        production[0] = SyntaxNode('grob_prop_path', production[1:])

    def p_grob_prop_path__grob_prop_spec__property_path(self, production):
        'grob_prop_path : grob_prop_spec property_path'
        production[0] = SyntaxNode('grob_prop_path', production[1:])

    ### grob_prop_spec ###

    def p_grob_prop_spec__symbol_list_rev(self, production):
        'grob_prop_spec : symbol_list_rev'
        production[0] = SyntaxNode('grob_prop_spec', production[1:])

    ### grouped_music_list ###

    def p_grouped_music_list__sequential_music(self, production):
        'grouped_music_list : sequential_music'
        production[0] = SyntaxNode('grouped_music_list', production[1:])

    def p_grouped_music_list__simultaneous_music(self, production):
        'grouped_music_list : simultaneous_music'
        production[0] = SyntaxNode('grouped_music_list', production[1:])

    ### identifier_init ###

    def p_identifier_init__identifier_init_nonumber(self, production):
        'identifier_init : identifier_init_nonumber'
        production[0] = SyntaxNode('identifier_init', production[1:])

    def p_identifier_init__number_expression(self, production):
        'identifier_init : number_expression'
        production[0] = SyntaxNode('identifier_init', production[1:])

    def p_identifier_init__post_event_nofinger__post_events(self, production):
        'identifier_init : post_event_nofinger post_events'
        production[0] = SyntaxNode('identifier_init', production[1:])

    ### identifier_init_nonumber ###

    def p_identifier_init_nonumber__FRACTION(self, production):
        'identifier_init_nonumber : FRACTION'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__book_block(self, production):
        'identifier_init_nonumber : book_block'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__bookpart_block(self, production):
        'identifier_init_nonumber : bookpart_block'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__context_def_spec_block(self, production):
        'identifier_init_nonumber : context_def_spec_block'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__context_modification(self, production):
        'identifier_init_nonumber : context_modification'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__embedded_scm(self, production):
        'identifier_init_nonumber : embedded_scm'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__full_markup_list(self, production):
        'identifier_init_nonumber : full_markup_list'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__music_assign(self, production):
        'identifier_init_nonumber : music_assign'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__output_def(self, production):
        'identifier_init_nonumber : output_def'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__partial_function__ETC(self, production):
        'identifier_init_nonumber : partial_function ETC'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__partial_markup(self, production):
        'identifier_init_nonumber : partial_markup'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__pitch_or_music(self, production):
        'identifier_init_nonumber : pitch_or_music'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__score_block(self, production):
        'identifier_init_nonumber : score_block'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    def p_identifier_init_nonumber__string(self, production):
        'identifier_init_nonumber : string'
        production[0] = SyntaxNode('identifier_init_nonumber', production[1:])

    ### lilypond ###

    def p_lilypond__Empty(self, production):
        'lilypond : '
        production[0] = SyntaxNode('lilypond', production[1:])

    def p_lilypond__lilypond__INVALID(self, production):
        'lilypond : lilypond INVALID'
        production[0] = SyntaxNode('lilypond', production[1:])

    def p_lilypond__lilypond__assignment(self, production):
        'lilypond : lilypond assignment'
        production[0] = SyntaxNode('lilypond', production[1:])

    def p_lilypond__lilypond__error(self, production):
        'lilypond : lilypond error'
        production[0] = SyntaxNode('lilypond', production[1:])

    def p_lilypond__lilypond__toplevel_expression(self, production):
        'lilypond : lilypond toplevel_expression'
        production[0] = SyntaxNode('lilypond', production[1:])

    ### lilypond_header ###

    def p_lilypond_header__HEADER__Chr123__lilypond_header_body__Chr125(self, production):
        "lilypond_header : HEADER '{' lilypond_header_body '}'"
        production[0] = SyntaxNode('lilypond_header', production[1:])

    ### lilypond_header_body ###

    def p_lilypond_header_body__Empty(self, production):
        'lilypond_header_body : '
        production[0] = SyntaxNode('lilypond_header_body', production[1:])

    def p_lilypond_header_body__lilypond_header_body__assignment(self, production):
        'lilypond_header_body : lilypond_header_body assignment'
        production[0] = SyntaxNode('lilypond_header_body', production[1:])

    def p_lilypond_header_body__lilypond_header_body__embedded_scm(self, production):
        'lilypond_header_body : lilypond_header_body embedded_scm'
        production[0] = SyntaxNode('lilypond_header_body', production[1:])

    ### lyric_element ###

    def p_lyric_element__LYRIC_ELEMENT(self, production):
        'lyric_element : LYRIC_ELEMENT'
        production[0] = SyntaxNode('lyric_element', production[1:])

    def p_lyric_element__STRING(self, production):
        'lyric_element : STRING'
        production[0] = SyntaxNode('lyric_element', production[1:])

    def p_lyric_element__full_markup(self, production):
        'lyric_element : full_markup'
        production[0] = SyntaxNode('lyric_element', production[1:])

    ### lyric_element_music ###

    def p_lyric_element_music__lyric_element__optional_notemode_duration__post_events(self, production):
        'lyric_element_music : lyric_element optional_notemode_duration post_events'
        production[0] = SyntaxNode('lyric_element_music', production[1:])

    ### lyric_mode_music ###

    def p_lyric_mode_music__MUSIC_IDENTIFIER(self, production):
        'lyric_mode_music : MUSIC_IDENTIFIER'
        production[0] = SyntaxNode('lyric_mode_music', production[1:])

    def p_lyric_mode_music__grouped_music_list(self, production):
        'lyric_mode_music : grouped_music_list'
        production[0] = SyntaxNode('lyric_mode_music', production[1:])

    ### markup ###

    def p_markup__markup_head_1_list__simple_markup(self, production):
        'markup : markup_head_1_list simple_markup'
        production[0] = SyntaxNode('markup', production[1:])

    def p_markup__simple_markup(self, production):
        'markup : simple_markup'
        production[0] = SyntaxNode('markup', production[1:])

    ### markup_braced_list ###

    def p_markup_braced_list__Chr123__markup_braced_list_body__Chr125(self, production):
        "markup_braced_list : '{' markup_braced_list_body '}'"
        production[0] = SyntaxNode('markup_braced_list', production[1:])

    ### markup_braced_list_body ###

    def p_markup_braced_list_body__Empty(self, production):
        'markup_braced_list_body : '
        production[0] = SyntaxNode('markup_braced_list_body', production[1:])

    def p_markup_braced_list_body__markup_braced_list_body__markup(self, production):
        'markup_braced_list_body : markup_braced_list_body markup'
        production[0] = SyntaxNode('markup_braced_list_body', production[1:])

    def p_markup_braced_list_body__markup_braced_list_body__markup_list(self, production):
        'markup_braced_list_body : markup_braced_list_body markup_list'
        production[0] = SyntaxNode('markup_braced_list_body', production[1:])

    ### markup_command_basic_arguments ###

    def p_markup_command_basic_arguments__EXPECT_MARKUP_LIST__markup_command_list_arguments__markup_list(self, production):
        'markup_command_basic_arguments : EXPECT_MARKUP_LIST markup_command_list_arguments markup_list'
        production[0] = SyntaxNode('markup_command_basic_arguments', production[1:])

    def p_markup_command_basic_arguments__EXPECT_NO_MORE_ARGS(self, production):
        'markup_command_basic_arguments : EXPECT_NO_MORE_ARGS'
        production[0] = SyntaxNode('markup_command_basic_arguments', production[1:])

    def p_markup_command_basic_arguments__EXPECT_SCM__markup_command_list_arguments__embedded_scm(self, production):
        'markup_command_basic_arguments : EXPECT_SCM markup_command_list_arguments embedded_scm'
        production[0] = SyntaxNode('markup_command_basic_arguments', production[1:])

    ### markup_command_list ###

    def p_markup_command_list__MARKUP_LIST_FUNCTION__markup_command_list_arguments(self, production):
        'markup_command_list : MARKUP_LIST_FUNCTION markup_command_list_arguments'
        production[0] = SyntaxNode('markup_command_list', production[1:])

    ### markup_command_list_arguments ###

    def p_markup_command_list_arguments__EXPECT_MARKUP__markup_command_list_arguments__markup(self, production):
        'markup_command_list_arguments : EXPECT_MARKUP markup_command_list_arguments markup'
        production[0] = SyntaxNode('markup_command_list_arguments', production[1:])

    def p_markup_command_list_arguments__markup_command_basic_arguments(self, production):
        'markup_command_list_arguments : markup_command_basic_arguments'
        production[0] = SyntaxNode('markup_command_list_arguments', production[1:])

    ### markup_composed_list ###

    def p_markup_composed_list__markup_head_1_list__markup_uncomposed_list(self, production):
        'markup_composed_list : markup_head_1_list markup_uncomposed_list'
        production[0] = SyntaxNode('markup_composed_list', production[1:])

    ### markup_head_1_item ###

    def p_markup_head_1_item__MARKUP_FUNCTION__EXPECT_MARKUP__markup_command_list_arguments(self, production):
        'markup_head_1_item : MARKUP_FUNCTION EXPECT_MARKUP markup_command_list_arguments'
        production[0] = SyntaxNode('markup_head_1_item', production[1:])

    ### markup_head_1_list ###

    def p_markup_head_1_list__markup_head_1_item(self, production):
        'markup_head_1_list : markup_head_1_item'
        production[0] = SyntaxNode('markup_head_1_list', production[1:])

    def p_markup_head_1_list__markup_head_1_list__markup_head_1_item(self, production):
        'markup_head_1_list : markup_head_1_list markup_head_1_item'
        production[0] = SyntaxNode('markup_head_1_list', production[1:])

    ### markup_list ###

    def p_markup_list__markup_composed_list(self, production):
        'markup_list : markup_composed_list'
        production[0] = SyntaxNode('markup_list', production[1:])

    def p_markup_list__markup_uncomposed_list(self, production):
        'markup_list : markup_uncomposed_list'
        production[0] = SyntaxNode('markup_list', production[1:])

    ### markup_mode ###

    def p_markup_mode__MARKUP(self, production):
        'markup_mode : MARKUP'
        production[0] = SyntaxNode('markup_mode', production[1:])

    ### markup_scm ###

    def p_markup_scm__embedded_scm_bare__BACKUP(self, production):
        'markup_scm : embedded_scm_bare BACKUP'
        production[0] = SyntaxNode('markup_scm', production[1:])

    ### markup_top ###

    def p_markup_top__markup_head_1_list__simple_markup(self, production):
        'markup_top : markup_head_1_list simple_markup'
        production[0] = SyntaxNode('markup_top', production[1:])

    def p_markup_top__markup_list(self, production):
        'markup_top : markup_list'
        production[0] = SyntaxNode('markup_top', production[1:])

    def p_markup_top__simple_markup(self, production):
        'markup_top : simple_markup'
        production[0] = SyntaxNode('markup_top', production[1:])

    ### markup_uncomposed_list ###

    def p_markup_uncomposed_list__SCORELINES__Chr123__score_body__Chr125(self, production):
        "markup_uncomposed_list : SCORELINES '{' score_body '}'"
        production[0] = SyntaxNode('markup_uncomposed_list', production[1:])

    def p_markup_uncomposed_list__markup_braced_list(self, production):
        'markup_uncomposed_list : markup_braced_list'
        production[0] = SyntaxNode('markup_uncomposed_list', production[1:])

    def p_markup_uncomposed_list__markup_command_list(self, production):
        'markup_uncomposed_list : markup_command_list'
        production[0] = SyntaxNode('markup_uncomposed_list', production[1:])

    def p_markup_uncomposed_list__markup_scm__MARKUPLIST_IDENTIFIER(self, production):
        'markup_uncomposed_list : markup_scm MARKUPLIST_IDENTIFIER'
        production[0] = SyntaxNode('markup_uncomposed_list', production[1:])

    ### maybe_notemode_duration ###

    def p_maybe_notemode_duration__Empty(self, production):
        'maybe_notemode_duration : '
        production[0] = SyntaxNode('maybe_notemode_duration', production[1:])

    def p_maybe_notemode_duration__multiplied_duration(self, production):
        'maybe_notemode_duration : multiplied_duration'
        production[0] = SyntaxNode('maybe_notemode_duration', production[1:])

    ### mode_changed_music ###

    def p_mode_changed_music__mode_changing_head__grouped_music_list(self, production):
        'mode_changed_music : mode_changing_head grouped_music_list'
        production[0] = SyntaxNode('mode_changed_music', production[1:])

    def p_mode_changed_music__mode_changing_head_with_context__optional_context_mod__grouped_music_list(self, production):
        'mode_changed_music : mode_changing_head_with_context optional_context_mod grouped_music_list'
        production[0] = SyntaxNode('mode_changed_music', production[1:])

    ### mode_changing_head ###

    def p_mode_changing_head__CHORDMODE(self, production):
        'mode_changing_head : CHORDMODE'
        production[0] = SyntaxNode('mode_changing_head', production[1:])

    def p_mode_changing_head__DRUMMODE(self, production):
        'mode_changing_head : DRUMMODE'
        production[0] = SyntaxNode('mode_changing_head', production[1:])

    def p_mode_changing_head__FIGUREMODE(self, production):
        'mode_changing_head : FIGUREMODE'
        production[0] = SyntaxNode('mode_changing_head', production[1:])

    def p_mode_changing_head__LYRICMODE(self, production):
        'mode_changing_head : LYRICMODE'
        production[0] = SyntaxNode('mode_changing_head', production[1:])

    def p_mode_changing_head__NOTEMODE(self, production):
        'mode_changing_head : NOTEMODE'
        production[0] = SyntaxNode('mode_changing_head', production[1:])

    ### mode_changing_head_with_context ###

    def p_mode_changing_head_with_context__CHORDS(self, production):
        'mode_changing_head_with_context : CHORDS'
        production[0] = SyntaxNode('mode_changing_head_with_context', production[1:])

    def p_mode_changing_head_with_context__DRUMS(self, production):
        'mode_changing_head_with_context : DRUMS'
        production[0] = SyntaxNode('mode_changing_head_with_context', production[1:])

    def p_mode_changing_head_with_context__FIGURES(self, production):
        'mode_changing_head_with_context : FIGURES'
        production[0] = SyntaxNode('mode_changing_head_with_context', production[1:])

    def p_mode_changing_head_with_context__LYRICS(self, production):
        'mode_changing_head_with_context : LYRICS'
        production[0] = SyntaxNode('mode_changing_head_with_context', production[1:])

    ### multiplied_duration ###

    def p_multiplied_duration__multiplied_duration__Chr42__FRACTION(self, production):
        "multiplied_duration : multiplied_duration '*' FRACTION"
        production[0] = SyntaxNode('multiplied_duration', production[1:])

    def p_multiplied_duration__multiplied_duration__Chr42__UNSIGNED(self, production):
        "multiplied_duration : multiplied_duration '*' UNSIGNED"
        production[0] = SyntaxNode('multiplied_duration', production[1:])

    def p_multiplied_duration__steno_duration(self, production):
        'multiplied_duration : steno_duration'
        production[0] = SyntaxNode('multiplied_duration', production[1:])

    ### music ###

    def p_music__lyric_element_music(self, production):
        'music : lyric_element_music'
        production[0] = SyntaxNode('music', production[1:])

    def p_music__music_assign(self, production):
        'music : music_assign'
        production[0] = SyntaxNode('music', production[1:])

    def p_music__pitch_as_music(self, production):
        'music : pitch_as_music'
        production[0] = SyntaxNode('music', production[1:])

    ### music_assign ###

    def p_music_assign__composite_music(self, production):
        'music_assign : composite_music'
        production[0] = SyntaxNode('music_assign', production[1:])

    def p_music_assign__simple_music(self, production):
        'music_assign : simple_music'
        production[0] = SyntaxNode('music_assign', production[1:])

    ### music_bare ###

    def p_music_bare__MUSIC_IDENTIFIER(self, production):
        'music_bare : MUSIC_IDENTIFIER'
        production[0] = SyntaxNode('music_bare', production[1:])

    def p_music_bare__grouped_music_list(self, production):
        'music_bare : grouped_music_list'
        production[0] = SyntaxNode('music_bare', production[1:])

    def p_music_bare__mode_changed_music(self, production):
        'music_bare : mode_changed_music'
        production[0] = SyntaxNode('music_bare', production[1:])

    ### music_embedded ###

    def p_music_embedded__multiplied_duration__post_events(self, production):
        'music_embedded : multiplied_duration post_events'
        production[0] = SyntaxNode('music_embedded', production[1:])

    def p_music_embedded__music(self, production):
        'music_embedded : music'
        production[0] = SyntaxNode('music_embedded', production[1:])

    def p_music_embedded__music_embedded_backup(self, production):
        'music_embedded : music_embedded_backup'
        production[0] = SyntaxNode('music_embedded', production[1:])

    def p_music_embedded__music_embedded_backup__BACKUP__lyric_element_music(self, production):
        'music_embedded : music_embedded_backup BACKUP lyric_element_music'
        production[0] = SyntaxNode('music_embedded', production[1:])

    ### music_embedded_backup ###

    def p_music_embedded_backup__embedded_scm(self, production):
        'music_embedded_backup : embedded_scm'
        production[0] = SyntaxNode('music_embedded_backup', production[1:])

    ### music_function_call ###

    def p_music_function_call__MUSIC_FUNCTION__function_arglist(self, production):
        'music_function_call : MUSIC_FUNCTION function_arglist'
        production[0] = SyntaxNode('music_function_call', production[1:])

    ### music_function_chord_body ###

    def p_music_function_chord_body__MUSIC_IDENTIFIER(self, production):
        'music_function_chord_body : MUSIC_IDENTIFIER'
        production[0] = SyntaxNode('music_function_chord_body', production[1:])

    def p_music_function_chord_body__embedded_scm(self, production):
        'music_function_chord_body : embedded_scm'
        production[0] = SyntaxNode('music_function_chord_body', production[1:])

    def p_music_function_chord_body__music_function_call(self, production):
        'music_function_chord_body : music_function_call'
        production[0] = SyntaxNode('music_function_chord_body', production[1:])

    ### music_list ###

    def p_music_list__Empty(self, production):
        'music_list : '
        production[0] = SyntaxNode('music_list', production[1:])

    def p_music_list__music_list__error(self, production):
        'music_list : music_list error'
        production[0] = SyntaxNode('music_list', production[1:])

    def p_music_list__music_list__music_embedded(self, production):
        'music_list : music_list music_embedded'
        production[0] = SyntaxNode('music_list', production[1:])

    ### music_or_context_def ###

    def p_music_or_context_def__context_def_spec_block(self, production):
        'music_or_context_def : context_def_spec_block'
        production[0] = SyntaxNode('music_or_context_def', production[1:])

    def p_music_or_context_def__music_assign(self, production):
        'music_or_context_def : music_assign'
        production[0] = SyntaxNode('music_or_context_def', production[1:])

    ### music_property_def ###

    def p_music_property_def__OVERRIDE__grob_prop_path__Chr61__scalar(self, production):
        "music_property_def : OVERRIDE grob_prop_path '=' scalar"
        production[0] = SyntaxNode('music_property_def', production[1:])

    def p_music_property_def__REVERT__simple_revert_context__revert_arg(self, production):
        'music_property_def : REVERT simple_revert_context revert_arg'
        production[0] = SyntaxNode('music_property_def', production[1:])

    def p_music_property_def__SET__context_prop_spec__Chr61__scalar(self, production):
        "music_property_def : SET context_prop_spec '=' scalar"
        production[0] = SyntaxNode('music_property_def', production[1:])

    def p_music_property_def__UNSET__context_prop_spec(self, production):
        'music_property_def : UNSET context_prop_spec'
        production[0] = SyntaxNode('music_property_def', production[1:])

    ### new_chord ###

    def p_new_chord__steno_tonic_pitch__maybe_notemode_duration(self, production):
        'new_chord : steno_tonic_pitch maybe_notemode_duration'
        production[0] = SyntaxNode('new_chord', production[1:])

    def p_new_chord__steno_tonic_pitch__optional_notemode_duration__chord_separator__chord_items(self, production):
        'new_chord : steno_tonic_pitch optional_notemode_duration chord_separator chord_items'
        production[0] = SyntaxNode('new_chord', production[1:])

    ### new_lyrics ###

    def p_new_lyrics__ADDLYRICS__lyric_mode_music(self, production):
        'new_lyrics : ADDLYRICS lyric_mode_music'
        production[0] = SyntaxNode('new_lyrics', production[1:])

    def p_new_lyrics__new_lyrics__ADDLYRICS__lyric_mode_music(self, production):
        'new_lyrics : new_lyrics ADDLYRICS lyric_mode_music'
        production[0] = SyntaxNode('new_lyrics', production[1:])

    ### note_chord_element ###

    def p_note_chord_element__chord_body__optional_notemode_duration__post_events(self, production):
        'note_chord_element : chord_body optional_notemode_duration post_events'
        production[0] = SyntaxNode('note_chord_element', production[1:])

    ### number_expression ###

    def p_number_expression__number_expression__Chr43__number_term(self, production):
        "number_expression : number_expression '+' number_term"
        production[0] = SyntaxNode('number_expression', production[1:])

    def p_number_expression__number_expression__Chr45__number_term(self, production):
        "number_expression : number_expression '-' number_term"
        production[0] = SyntaxNode('number_expression', production[1:])

    def p_number_expression__number_term(self, production):
        'number_expression : number_term'
        production[0] = SyntaxNode('number_expression', production[1:])

    ### number_factor ###

    def p_number_factor__Chr45__number_factor(self, production):
        "number_factor : '-' number_factor"
        production[0] = SyntaxNode('number_factor', production[1:])

    def p_number_factor__bare_number(self, production):
        'number_factor : bare_number'
        production[0] = SyntaxNode('number_factor', production[1:])

    ### number_term ###

    def p_number_term__number_factor(self, production):
        'number_term : number_factor'
        production[0] = SyntaxNode('number_term', production[1:])

    def p_number_term__number_factor__Chr42__number_factor(self, production):
        "number_term : number_factor '*' number_factor"
        production[0] = SyntaxNode('number_term', production[1:])

    def p_number_term__number_factor__Chr47__number_factor(self, production):
        "number_term : number_factor '/' number_factor"
        production[0] = SyntaxNode('number_term', production[1:])

    ### octave_check ###

    def p_octave_check__Chr61__quotes(self, production):
        "octave_check : '=' quotes"
        production[0] = SyntaxNode('octave_check', production[1:])

    def p_octave_check__Empty(self, production):
        'octave_check : '
        production[0] = SyntaxNode('octave_check', production[1:])

    ### optional_context_mod ###

    def p_optional_context_mod__Empty(self, production):
        'optional_context_mod : '
        production[0] = SyntaxNode('optional_context_mod', production[1:])

    def p_optional_context_mod__context_modification(self, production):
        'optional_context_mod : context_modification'
        production[0] = SyntaxNode('optional_context_mod', production[1:])

    ### optional_id ###

    def p_optional_id__Chr61__simple_string(self, production):
        "optional_id : '=' simple_string"
        production[0] = SyntaxNode('optional_id', production[1:])

    def p_optional_id__Empty(self, production):
        'optional_id : '
        production[0] = SyntaxNode('optional_id', production[1:])

    ### optional_notemode_duration ###

    def p_optional_notemode_duration__maybe_notemode_duration(self, production):
        'optional_notemode_duration : maybe_notemode_duration'
        production[0] = SyntaxNode('optional_notemode_duration', production[1:])

    ### optional_rest ###

    def p_optional_rest__Empty(self, production):
        'optional_rest : '
        production[0] = SyntaxNode('optional_rest', production[1:])

    def p_optional_rest__REST(self, production):
        'optional_rest : REST'
        production[0] = SyntaxNode('optional_rest', production[1:])

    ### output_def ###

    def p_output_def__output_def_body__Chr125(self, production):
        "output_def : output_def_body '}'"
        production[0] = SyntaxNode('output_def', production[1:])

    ### output_def_body ###

    def p_output_def_body__output_def_body__SCM_TOKEN(self, production):
        'output_def_body : output_def_body SCM_TOKEN'
        production[0] = SyntaxNode('output_def_body', production[1:])

    def p_output_def_body__output_def_body__assignment(self, production):
        'output_def_body : output_def_body assignment'
        production[0] = SyntaxNode('output_def_body', production[1:])

    def p_output_def_body__output_def_body__embedded_scm_active(self, production):
        'output_def_body : output_def_body embedded_scm_active'
        production[0] = SyntaxNode('output_def_body', production[1:])

    def p_output_def_body__output_def_body__error(self, production):
        'output_def_body : output_def_body error'
        production[0] = SyntaxNode('output_def_body', production[1:])

    def p_output_def_body__output_def_body__music_or_context_def(self, production):
        'output_def_body : output_def_body music_or_context_def'
        production[0] = SyntaxNode('output_def_body', production[1:])

    def p_output_def_body__output_def_head_with_mode_switch__Chr123(self, production):
        "output_def_body : output_def_head_with_mode_switch '{'"
        production[0] = SyntaxNode('output_def_body', production[1:])

    ### output_def_head ###

    def p_output_def_head__LAYOUT(self, production):
        'output_def_head : LAYOUT'
        production[0] = SyntaxNode('output_def_head', production[1:])

    def p_output_def_head__MIDI(self, production):
        'output_def_head : MIDI'
        production[0] = SyntaxNode('output_def_head', production[1:])

    def p_output_def_head__PAPER(self, production):
        'output_def_head : PAPER'
        production[0] = SyntaxNode('output_def_head', production[1:])

    ### output_def_head_with_mode_switch ###

    def p_output_def_head_with_mode_switch__output_def_head(self, production):
        'output_def_head_with_mode_switch : output_def_head'
        production[0] = SyntaxNode('output_def_head_with_mode_switch', production[1:])

    ### paper_block ###

    def p_paper_block__output_def(self, production):
        'paper_block : output_def'
        production[0] = SyntaxNode('paper_block', production[1:])

    ### partial_function ###

    def p_partial_function__EVENT_FUNCTION__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__partial_function(self, production):
        'partial_function : EVENT_FUNCTION EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup partial_function'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__EVENT_FUNCTION__EXPECT_SCM__function_arglist_optional__partial_function(self, production):
        'partial_function : EVENT_FUNCTION EXPECT_SCM function_arglist_optional partial_function'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__EVENT_FUNCTION__function_arglist_partial(self, production):
        'partial_function : EVENT_FUNCTION function_arglist_partial'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__MUSIC_FUNCTION__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__partial_function(self, production):
        'partial_function : MUSIC_FUNCTION EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup partial_function'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__MUSIC_FUNCTION__EXPECT_SCM__function_arglist_optional__partial_function(self, production):
        'partial_function : MUSIC_FUNCTION EXPECT_SCM function_arglist_optional partial_function'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__MUSIC_FUNCTION__function_arglist_partial(self, production):
        'partial_function : MUSIC_FUNCTION function_arglist_partial'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__OVERRIDE__grob_prop_path__Chr61(self, production):
        "partial_function : OVERRIDE grob_prop_path '='"
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__OVERRIDE__grob_prop_path__Chr61__partial_function(self, production):
        "partial_function : OVERRIDE grob_prop_path '=' partial_function"
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__SCM_FUNCTION__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_nonbackup__partial_function(self, production):
        'partial_function : SCM_FUNCTION EXPECT_OPTIONAL EXPECT_SCM function_arglist_nonbackup partial_function'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__SCM_FUNCTION__EXPECT_SCM__function_arglist_optional__partial_function(self, production):
        'partial_function : SCM_FUNCTION EXPECT_SCM function_arglist_optional partial_function'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__SCM_FUNCTION__function_arglist_partial(self, production):
        'partial_function : SCM_FUNCTION function_arglist_partial'
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__SET__context_prop_spec__Chr61(self, production):
        "partial_function : SET context_prop_spec '='"
        production[0] = SyntaxNode('partial_function', production[1:])

    def p_partial_function__SET__context_prop_spec__Chr61__partial_function(self, production):
        "partial_function : SET context_prop_spec '=' partial_function"
        production[0] = SyntaxNode('partial_function', production[1:])

    ### partial_markup ###

    def p_partial_markup__markup_mode__markup_head_1_list__ETC(self, production):
        'partial_markup : markup_mode markup_head_1_list ETC'
        production[0] = SyntaxNode('partial_markup', production[1:])

    ### pitch ###

    def p_pitch__PITCH_IDENTIFIER__quotes(self, production):
        'pitch : PITCH_IDENTIFIER quotes'
        production[0] = SyntaxNode('pitch', production[1:])

    def p_pitch__steno_pitch(self, production):
        'pitch : steno_pitch'
        production[0] = SyntaxNode('pitch', production[1:])

    ### pitch_as_music ###

    def p_pitch_as_music__pitch_or_music(self, production):
        'pitch_as_music : pitch_or_music'
        production[0] = SyntaxNode('pitch_as_music', production[1:])

    ### pitch_or_music ###

    def p_pitch_or_music__new_chord__post_events(self, production):
        'pitch_or_music : new_chord post_events'
        production[0] = SyntaxNode('pitch_or_music', production[1:])

    def p_pitch_or_music__pitch__exclamations__questions__octave_check__maybe_notemode_duration__optional_rest__post_events(self, production):
        'pitch_or_music : pitch exclamations questions octave_check maybe_notemode_duration optional_rest post_events'
        production[0] = SyntaxNode('pitch_or_music', production[1:])

    ### pitch_or_tonic_pitch ###

    def p_pitch_or_tonic_pitch__pitch(self, production):
        'pitch_or_tonic_pitch : pitch'
        production[0] = SyntaxNode('pitch_or_tonic_pitch', production[1:])

    def p_pitch_or_tonic_pitch__steno_tonic_pitch(self, production):
        'pitch_or_tonic_pitch : steno_tonic_pitch'
        production[0] = SyntaxNode('pitch_or_tonic_pitch', production[1:])

    ### post_event ###

    def p_post_event__Chr45__fingering(self, production):
        "post_event : '-' fingering"
        production[0] = SyntaxNode('post_event', production[1:])

    def p_post_event__post_event_nofinger(self, production):
        'post_event : post_event_nofinger'
        production[0] = SyntaxNode('post_event', production[1:])

    ### post_event_nofinger ###

    def p_post_event_nofinger__Chr94__fingering(self, production):
        "post_event_nofinger : '^' fingering"
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__Chr95__fingering(self, production):
        "post_event_nofinger : '_' fingering"
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__EXTENDER(self, production):
        'post_event_nofinger : EXTENDER'
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__HYPHEN(self, production):
        'post_event_nofinger : HYPHEN'
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__direction_less_event(self, production):
        'post_event_nofinger : direction_less_event'
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__script_dir__direction_less_event(self, production):
        'post_event_nofinger : script_dir direction_less_event'
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__script_dir__direction_reqd_event(self, production):
        'post_event_nofinger : script_dir direction_reqd_event'
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    def p_post_event_nofinger__script_dir__music_function_call(self, production):
        'post_event_nofinger : script_dir music_function_call'
        production[0] = SyntaxNode('post_event_nofinger', production[1:])

    ### post_events ###

    def p_post_events__Empty(self, production):
        'post_events : '
        production[0] = SyntaxNode('post_events', production[1:])

    def p_post_events__post_events__post_event(self, production):
        'post_events : post_events post_event'
        production[0] = SyntaxNode('post_events', production[1:])

    ### property_operation ###

    def p_property_operation__OVERRIDE__property_path__Chr61__scalar(self, production):
        "property_operation : OVERRIDE property_path '=' scalar"
        production[0] = SyntaxNode('property_operation', production[1:])

    def p_property_operation__REVERT__revert_arg(self, production):
        'property_operation : REVERT revert_arg'
        production[0] = SyntaxNode('property_operation', production[1:])

    def p_property_operation__UNSET__symbol(self, production):
        'property_operation : UNSET symbol'
        production[0] = SyntaxNode('property_operation', production[1:])

    def p_property_operation__symbol__Chr61__scalar(self, production):
        "property_operation : symbol '=' scalar"
        production[0] = SyntaxNode('property_operation', production[1:])

    ### property_path ###

    def p_property_path__symbol_list_rev(self, production):
        'property_path : symbol_list_rev'
        production[0] = SyntaxNode('property_path', production[1:])

    def p_property_path__symbol_list_rev__property_path(self, production):
        'property_path : symbol_list_rev property_path'
        production[0] = SyntaxNode('property_path', production[1:])

    ### questions ###

    def p_questions__Empty(self, production):
        'questions : '
        production[0] = SyntaxNode('questions', production[1:])

    def p_questions__questions__Chr63(self, production):
        "questions : questions '?'"
        production[0] = SyntaxNode('questions', production[1:])

    ### quotes ###

    def p_quotes__Empty(self, production):
        'quotes : '
        production[0] = SyntaxNode('quotes', production[1:])

    def p_quotes__sub_quotes(self, production):
        'quotes : sub_quotes'
        production[0] = SyntaxNode('quotes', production[1:])

    def p_quotes__sup_quotes(self, production):
        'quotes : sup_quotes'
        production[0] = SyntaxNode('quotes', production[1:])

    ### repeated_music ###

    def p_repeated_music__REPEAT__simple_string__unsigned_number__music(self, production):
        'repeated_music : REPEAT simple_string unsigned_number music'
        production[0] = SyntaxNode('repeated_music', production[1:])

    def p_repeated_music__REPEAT__simple_string__unsigned_number__music__ALTERNATIVE__braced_music_list(self, production):
        'repeated_music : REPEAT simple_string unsigned_number music ALTERNATIVE braced_music_list'
        production[0] = SyntaxNode('repeated_music', production[1:])

    ### revert_arg ###

    def p_revert_arg__revert_arg_backup__BACKUP__symbol_list_arg(self, production):
        'revert_arg : revert_arg_backup BACKUP symbol_list_arg'
        production[0] = SyntaxNode('revert_arg', production[1:])

    ### revert_arg_backup ###

    def p_revert_arg_backup__revert_arg_part(self, production):
        'revert_arg_backup : revert_arg_part'
        production[0] = SyntaxNode('revert_arg_backup', production[1:])

    ### revert_arg_part ###

    def p_revert_arg_part__revert_arg_backup__BACKUP__SCM_ARG__Chr46__symbol_list_part(self, production):
        "revert_arg_part : revert_arg_backup BACKUP SCM_ARG '.' symbol_list_part"
        production[0] = SyntaxNode('revert_arg_part', production[1:])

    def p_revert_arg_part__revert_arg_backup__BACKUP__SCM_ARG__symbol_list_part(self, production):
        'revert_arg_part : revert_arg_backup BACKUP SCM_ARG symbol_list_part'
        production[0] = SyntaxNode('revert_arg_part', production[1:])

    def p_revert_arg_part__symbol_list_part(self, production):
        'revert_arg_part : symbol_list_part'
        production[0] = SyntaxNode('revert_arg_part', production[1:])

    ### scalar ###

    def p_scalar__Chr45__bare_number(self, production):
        "scalar : '-' bare_number"
        production[0] = SyntaxNode('scalar', production[1:])

    def p_scalar__SCM_IDENTIFIER(self, production):
        'scalar : SCM_IDENTIFIER'
        production[0] = SyntaxNode('scalar', production[1:])

    def p_scalar__bare_number(self, production):
        'scalar : bare_number'
        production[0] = SyntaxNode('scalar', production[1:])

    def p_scalar__embedded_scm_arg(self, production):
        'scalar : embedded_scm_arg'
        production[0] = SyntaxNode('scalar', production[1:])

    def p_scalar__pitch_or_music(self, production):
        'scalar : pitch_or_music'
        production[0] = SyntaxNode('scalar', production[1:])

    def p_scalar__string(self, production):
        'scalar : string'
        production[0] = SyntaxNode('scalar', production[1:])

    ### scm_function_call ###

    def p_scm_function_call__SCM_FUNCTION__function_arglist(self, production):
        'scm_function_call : SCM_FUNCTION function_arglist'
        production[0] = SyntaxNode('scm_function_call', production[1:])

    ### score_block ###

    def p_score_block__SCORE__Chr123__score_body__Chr125(self, production):
        "score_block : SCORE '{' score_body '}'"
        production[0] = SyntaxNode('score_block', production[1:])

    ### score_body ###

    def p_score_body__score_body__error(self, production):
        'score_body : score_body error'
        production[0] = SyntaxNode('score_body', production[1:])

    def p_score_body__score_items(self, production):
        'score_body : score_items'
        production[0] = SyntaxNode('score_body', production[1:])

    ### score_item ###

    def p_score_item__embedded_scm(self, production):
        'score_item : embedded_scm'
        production[0] = SyntaxNode('score_item', production[1:])

    def p_score_item__music(self, production):
        'score_item : music'
        production[0] = SyntaxNode('score_item', production[1:])

    def p_score_item__output_def(self, production):
        'score_item : output_def'
        production[0] = SyntaxNode('score_item', production[1:])

    ### score_items ###

    def p_score_items__Empty(self, production):
        'score_items : '
        production[0] = SyntaxNode('score_items', production[1:])

    def p_score_items__score_items__lilypond_header(self, production):
        'score_items : score_items lilypond_header'
        production[0] = SyntaxNode('score_items', production[1:])

    def p_score_items__score_items__score_item(self, production):
        'score_items : score_items score_item'
        production[0] = SyntaxNode('score_items', production[1:])

    ### script_abbreviation ###

    def p_script_abbreviation__ANGLE_CLOSE(self, production):
        'script_abbreviation : ANGLE_CLOSE'
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    def p_script_abbreviation__Chr33(self, production):
        "script_abbreviation : '!'"
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    def p_script_abbreviation__Chr43(self, production):
        "script_abbreviation : '+'"
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    def p_script_abbreviation__Chr45(self, production):
        "script_abbreviation : '-'"
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    def p_script_abbreviation__Chr46(self, production):
        "script_abbreviation : '.'"
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    def p_script_abbreviation__Chr94(self, production):
        "script_abbreviation : '^'"
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    def p_script_abbreviation__Chr95(self, production):
        "script_abbreviation : '_'"
        production[0] = SyntaxNode('script_abbreviation', production[1:])

    ### script_dir ###

    def p_script_dir__Chr45(self, production):
        "script_dir : '-'"
        production[0] = SyntaxNode('script_dir', production[1:])

    def p_script_dir__Chr94(self, production):
        "script_dir : '^'"
        production[0] = SyntaxNode('script_dir', production[1:])

    def p_script_dir__Chr95(self, production):
        "script_dir : '_'"
        production[0] = SyntaxNode('script_dir', production[1:])

    ### sequential_music ###

    def p_sequential_music__SEQUENTIAL__braced_music_list(self, production):
        'sequential_music : SEQUENTIAL braced_music_list'
        production[0] = SyntaxNode('sequential_music', production[1:])

    def p_sequential_music__braced_music_list(self, production):
        'sequential_music : braced_music_list'
        production[0] = SyntaxNode('sequential_music', production[1:])

    ### simple_element ###

    def p_simple_element__DRUM_PITCH__optional_notemode_duration(self, production):
        'simple_element : DRUM_PITCH optional_notemode_duration'
        production[0] = SyntaxNode('simple_element', production[1:])

    def p_simple_element__RESTNAME__optional_notemode_duration(self, production):
        'simple_element : RESTNAME optional_notemode_duration'
        production[0] = SyntaxNode('simple_element', production[1:])

    ### simple_markup ###

    def p_simple_markup__MARKUP_FUNCTION__markup_command_basic_arguments(self, production):
        'simple_markup : MARKUP_FUNCTION markup_command_basic_arguments'
        production[0] = SyntaxNode('simple_markup', production[1:])

    def p_simple_markup__SCORE__Chr123__score_body__Chr125(self, production):
        "simple_markup : SCORE '{' score_body '}'"
        production[0] = SyntaxNode('simple_markup', production[1:])

    def p_simple_markup__STRING(self, production):
        'simple_markup : STRING'
        production[0] = SyntaxNode('simple_markup', production[1:])

    def p_simple_markup__markup_scm__MARKUP_IDENTIFIER(self, production):
        'simple_markup : markup_scm MARKUP_IDENTIFIER'
        production[0] = SyntaxNode('simple_markup', production[1:])

    ### simple_music ###

    def p_simple_music__context_change(self, production):
        'simple_music : context_change'
        production[0] = SyntaxNode('simple_music', production[1:])

    def p_simple_music__event_chord(self, production):
        'simple_music : event_chord'
        production[0] = SyntaxNode('simple_music', production[1:])

    def p_simple_music__music_property_def(self, production):
        'simple_music : music_property_def'
        production[0] = SyntaxNode('simple_music', production[1:])

    ### simple_revert_context ###

    def p_simple_revert_context__symbol_list_part(self, production):
        'simple_revert_context : symbol_list_part'
        production[0] = SyntaxNode('simple_revert_context', production[1:])

    ### simple_string ###

    def p_simple_string__STRING(self, production):
        'simple_string : STRING'
        production[0] = SyntaxNode('simple_string', production[1:])

    def p_simple_string__embedded_scm_bare(self, production):
        'simple_string : embedded_scm_bare'
        production[0] = SyntaxNode('simple_string', production[1:])

    ### simultaneous_music ###

    def p_simultaneous_music__DOUBLE_ANGLE_OPEN__music_list__DOUBLE_ANGLE_CLOSE(self, production):
        'simultaneous_music : DOUBLE_ANGLE_OPEN music_list DOUBLE_ANGLE_CLOSE'
        production[0] = SyntaxNode('simultaneous_music', production[1:])

    def p_simultaneous_music__SIMULTANEOUS__braced_music_list(self, production):
        'simultaneous_music : SIMULTANEOUS braced_music_list'
        production[0] = SyntaxNode('simultaneous_music', production[1:])

    ### steno_duration ###

    def p_steno_duration__DURATION_IDENTIFIER__dots(self, production):
        'steno_duration : DURATION_IDENTIFIER dots'
        production[0] = SyntaxNode('steno_duration', production[1:])

    def p_steno_duration__UNSIGNED__dots(self, production):
        'steno_duration : UNSIGNED dots'
        production[0] = SyntaxNode('steno_duration', production[1:])

    ### steno_pitch ###

    def p_steno_pitch__NOTENAME_PITCH__quotes(self, production):
        'steno_pitch : NOTENAME_PITCH quotes'
        production[0] = SyntaxNode('steno_pitch', production[1:])

    ### steno_tonic_pitch ###

    def p_steno_tonic_pitch__TONICNAME_PITCH__quotes(self, production):
        'steno_tonic_pitch : TONICNAME_PITCH quotes'
        production[0] = SyntaxNode('steno_tonic_pitch', production[1:])

    ### step_number ###

    def p_step_number__UNSIGNED(self, production):
        'step_number : UNSIGNED'
        production[0] = SyntaxNode('step_number', production[1:])

    def p_step_number__UNSIGNED__CHORD_MINUS(self, production):
        'step_number : UNSIGNED CHORD_MINUS'
        production[0] = SyntaxNode('step_number', production[1:])

    def p_step_number__UNSIGNED__Chr43(self, production):
        "step_number : UNSIGNED '+'"
        production[0] = SyntaxNode('step_number', production[1:])

    ### step_numbers ###

    def p_step_numbers__step_number(self, production):
        'step_numbers : step_number'
        production[0] = SyntaxNode('step_numbers', production[1:])

    def p_step_numbers__step_numbers__Chr46__step_number(self, production):
        "step_numbers : step_numbers '.' step_number"
        production[0] = SyntaxNode('step_numbers', production[1:])

    ### string ###

    def p_string__STRING(self, production):
        'string : STRING'
        production[0] = SyntaxNode('string', production[1:])

    def p_string__full_markup(self, production):
        'string : full_markup'
        production[0] = SyntaxNode('string', production[1:])

    ### string_number_event ###

    def p_string_number_event__E_UNSIGNED(self, production):
        'string_number_event : E_UNSIGNED'
        production[0] = SyntaxNode('string_number_event', production[1:])

    ### sub_quotes ###

    def p_sub_quotes__Chr44(self, production):
        "sub_quotes : ','"
        production[0] = SyntaxNode('sub_quotes', production[1:])

    def p_sub_quotes__sub_quotes__Chr44(self, production):
        "sub_quotes : sub_quotes ','"
        production[0] = SyntaxNode('sub_quotes', production[1:])

    ### sup_quotes ###

    def p_sup_quotes__Chr39(self, production):
        "sup_quotes : '''"
        production[0] = SyntaxNode('sup_quotes', production[1:])

    def p_sup_quotes__sup_quotes__Chr39(self, production):
        "sup_quotes : sup_quotes '''"
        production[0] = SyntaxNode('sup_quotes', production[1:])

    ### symbol ###

    def p_symbol__STRING(self, production):
        'symbol : STRING'
        production[0] = SyntaxNode('symbol', production[1:])

    def p_symbol__embedded_scm_bare(self, production):
        'symbol : embedded_scm_bare'
        production[0] = SyntaxNode('symbol', production[1:])

    ### symbol_list_arg ###

    def p_symbol_list_arg__SYMBOL_LIST(self, production):
        'symbol_list_arg : SYMBOL_LIST'
        production[0] = SyntaxNode('symbol_list_arg', production[1:])

    def p_symbol_list_arg__SYMBOL_LIST__Chr46__symbol_list_rev(self, production):
        "symbol_list_arg : SYMBOL_LIST '.' symbol_list_rev"
        production[0] = SyntaxNode('symbol_list_arg', production[1:])

    ### symbol_list_element ###

    def p_symbol_list_element__STRING(self, production):
        'symbol_list_element : STRING'
        production[0] = SyntaxNode('symbol_list_element', production[1:])

    def p_symbol_list_element__embedded_scm_bare(self, production):
        'symbol_list_element : embedded_scm_bare'
        production[0] = SyntaxNode('symbol_list_element', production[1:])

    ### symbol_list_part ###

    def p_symbol_list_part__symbol_list_element(self, production):
        'symbol_list_part : symbol_list_element'
        production[0] = SyntaxNode('symbol_list_part', production[1:])

    ### symbol_list_rev ###

    def p_symbol_list_rev__symbol_list_part(self, production):
        'symbol_list_rev : symbol_list_part'
        production[0] = SyntaxNode('symbol_list_rev', production[1:])

    def p_symbol_list_rev__symbol_list_rev__Chr46__symbol_list_part(self, production):
        "symbol_list_rev : symbol_list_rev '.' symbol_list_part"
        production[0] = SyntaxNode('symbol_list_rev', production[1:])

    ### tempo_event ###

    def p_tempo_event__TEMPO__scalar(self, production):
        'tempo_event : TEMPO scalar'
        production[0] = SyntaxNode('tempo_event', production[1:])

    def p_tempo_event__TEMPO__scalar__steno_duration__Chr61__tempo_range(self, production):
        "tempo_event : TEMPO scalar steno_duration '=' tempo_range"
        production[0] = SyntaxNode('tempo_event', production[1:])

    def p_tempo_event__TEMPO__steno_duration__Chr61__tempo_range(self, production):
        "tempo_event : TEMPO steno_duration '=' tempo_range"
        production[0] = SyntaxNode('tempo_event', production[1:])

    ### tempo_range ###

    def p_tempo_range__unsigned_number(self, production):
        'tempo_range : unsigned_number'
        production[0] = SyntaxNode('tempo_range', production[1:])

    def p_tempo_range__unsigned_number__Chr45__unsigned_number(self, production):
        "tempo_range : unsigned_number '-' unsigned_number"
        production[0] = SyntaxNode('tempo_range', production[1:])

    ### toplevel_expression ###

    def p_toplevel_expression__BOOK_IDENTIFIER(self, production):
        'toplevel_expression : BOOK_IDENTIFIER'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__SCM_TOKEN(self, production):
        'toplevel_expression : SCM_TOKEN'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__book_block(self, production):
        'toplevel_expression : book_block'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__bookpart_block(self, production):
        'toplevel_expression : bookpart_block'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__composite_music(self, production):
        'toplevel_expression : composite_music'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__embedded_scm_active(self, production):
        'toplevel_expression : embedded_scm_active'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__full_markup(self, production):
        'toplevel_expression : full_markup'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__full_markup_list(self, production):
        'toplevel_expression : full_markup_list'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__lilypond_header(self, production):
        'toplevel_expression : lilypond_header'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__output_def(self, production):
        'toplevel_expression : output_def'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    def p_toplevel_expression__score_block(self, production):
        'toplevel_expression : score_block'
        production[0] = SyntaxNode('toplevel_expression', production[1:])

    ### tremolo_type ###

    def p_tremolo_type__Chr58(self, production):
        "tremolo_type : ':'"
        production[0] = SyntaxNode('tremolo_type', production[1:])

    def p_tremolo_type__Chr58__UNSIGNED(self, production):
        "tremolo_type : ':' UNSIGNED"
        production[0] = SyntaxNode('tremolo_type', production[1:])

    ### unsigned_number ###

    def p_unsigned_number__NUMBER_IDENTIFIER(self, production):
        'unsigned_number : NUMBER_IDENTIFIER'
        production[0] = SyntaxNode('unsigned_number', production[1:])

    def p_unsigned_number__UNSIGNED(self, production):
        'unsigned_number : UNSIGNED'
        production[0] = SyntaxNode('unsigned_number', production[1:])

    def p_unsigned_number__embedded_scm(self, production):
        'unsigned_number : embedded_scm'
        production[0] = SyntaxNode('unsigned_number', production[1:])

    ### ERROR ###

    def p_error(self, production):
        r'''Error handling.'''
        pass