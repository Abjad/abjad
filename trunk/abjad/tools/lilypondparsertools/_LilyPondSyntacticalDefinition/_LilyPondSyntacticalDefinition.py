from abjad import *
from abjad.exceptions import LilyPondParserError
from abjad.tools import durationtools
from abjad.tools.lilypondparsertools._LilyPondDuration._LilyPondDuration \
    import _LilyPondDuration
from abjad.tools.lilypondparsertools._LilyPondEvent._LilyPondEvent \
    import _LilyPondEvent as Event
from abjad.tools.lilypondparsertools._LilyPondFraction._LilyPondFraction \
    import _LilyPondFraction
from abjad.tools.lilypondparsertools._SyntaxNode._SyntaxNode \
    import _SyntaxNode as Node


class _LilyPondSyntacticalDefinition(object):

    def __init__(self, client):
        self.client = client
        self.tokens = self.client._lexdef.tokens


    start = 'start_symbol'


    precedence = (
#        ('nonassoc', 'REPEAT'),
#        ('nonassoc', 'ALTERNATIVE'),
        ('nonassoc', 'COMPOSITE'),
#        ('left', 'ADDLYRICS'),
        ('nonassoc', 'DEFAULT'),
        ('nonassoc', 'FUNCTION_ARGLIST'),
        ('right', 'PITCH_IDENTIFIER', 'NOTENAME_PITCH', 'TONICNAME_PITCH', 'UNSIGNED', 'REAL', 'DURATION_IDENTIFIER', ':'),
        ('nonassoc', 'NUMBER_IDENTIFIER', '/'),
        ('left', '+', '-'),
#        ('left', 'UNARY_MINUS')
    )


    ### SYNTACTICAL RULES (ALPHABETICAL) ###


#    def p_start_symbol__EMBEDDED_LILY__embedded_lilypond(self, p):
#        'start_symbol : EMBEDDED_LILY embedded_lilypond'
#        p[0] = Node('start_symbol', p[1:])


    def p_start_symbol__lilypond(self, p):
        'start_symbol : lilypond'
        if 1 < len(p[1]):
            lily = lilypondfiletools.LilyPondFile( )
            lily.extend(p[1])
            p[0] = lily
        elif 1 == len(p[1]):
            p[0] = p[1][0]
        else:
            p[0] = None


    ### assignment ###


    def p_assignment__assignment_id__Chr61__identifier_init(self, p):
        "assignment : assignment_id '=' identifier_init"
        p[0] = [p[1], p[3]]


#    def p_assignment__assignment_id__property_path__Chr61__identifier_init(self, p):
#        "assignment : assignment_id property_path '=' identifier_init"
#        p[0] = [p[1], p[3]]


    def p_assignment__embedded_scm(self, p):
        'assignment : embedded_scm'
        p[0] = None


    ### assignment_id ###


#    def p_assignment_id__LYRICS_STRING(self, p):
#        'assignment_id : LYRICS_STRING'
#        p[0] = Node('assignment_id', p[1:])


    def p_assignment_id__STRING(self, p):
        'assignment_id : STRING'
        p[0] = p[1]


    ### bare_number ###


    def p_bare_number__REAL__NUMBER_IDENTIFIER(self, p):
        'bare_number : REAL NUMBER_IDENTIFIER'
        p[0] = p[1]


    def p_bare_number__UNSIGNED__NUMBER_IDENTIFIER(self, p):
        'bare_number : UNSIGNED NUMBER_IDENTIFIER'
        p[0] = p[1]


    def p_bare_number__bare_number_closed(self, p):
        'bare_number : bare_number_closed'
        p[0] = p[1]


    ### bare_number_closed ###


    def p_bare_number_closed__NUMBER_IDENTIFIER(self, p):
        'bare_number_closed : NUMBER_IDENTIFIER'
        p[0] = p[1]


    def p_bare_number_closed__REAL(self, p):
        'bare_number_closed : REAL'
        p[0] = p[1]


    def p_bare_number_closed__UNSIGNED(self, p):
        'bare_number_closed : UNSIGNED'
        p[0] = p[1]


    ### bare_unsigned ###


    def p_bare_unsigned__UNSIGNED(self, p):
        'bare_unsigned : UNSIGNED'
        p[0] = p[1]


    ### bass_figure ###


#    def p_bass_figure__FIGURE_SPACE(self, p):
#        'bass_figure : FIGURE_SPACE'
#        p[0] = Node('bass_figure', p[1:])


#    def p_bass_figure__bass_figure__Chr93(self, p):
#        "bass_figure : bass_figure ']'"
#        p[0] = Node('bass_figure', p[1:])


#    def p_bass_figure__bass_figure__figured_bass_alteration(self, p):
#        'bass_figure : bass_figure figured_bass_alteration'
#        p[0] = Node('bass_figure', p[1:])


#    def p_bass_figure__bass_figure__figured_bass_modification(self, p):
#        'bass_figure : bass_figure figured_bass_modification'
#        p[0] = Node('bass_figure', p[1:])


#    def p_bass_figure__bass_number(self, p):
#        'bass_figure : bass_number'
#        p[0] = Node('bass_figure', p[1:])


    ### bass_number ###


#    def p_bass_number__STRING(self, p):
#        'bass_number : STRING'
#        p[0] = Node('bass_number', p[1:])


#    def p_bass_number__UNSIGNED(self, p):
#        'bass_number : UNSIGNED'
#        p[0] = Node('bass_number', p[1:])


#    def p_bass_number__full_markup(self, p):
#        'bass_number : full_markup'
#        p[0] = Node('bass_number', p[1:])


    ### book_block ###


#    def p_book_block__BOOK__Chr123__book_body__Chr125(self, p):
#        "book_block : BOOK '{' book_body '}'"
#        p[0] = Node('book_block', p[1:])


    ### book_body ###


#    def p_book_body__Empty(self, p):
#        'book_body : '
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__BOOK_IDENTIFIER(self, p):
#        'book_body : BOOK_IDENTIFIER'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__bookpart_block(self, p):
#        'book_body : book_body bookpart_block'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__composite_music(self, p):
#        'book_body : book_body composite_music'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__embedded_scm(self, p):
#        'book_body : book_body embedded_scm'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__error(self, p):
#        'book_body : book_body error'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__full_markup(self, p):
#        'book_body : book_body full_markup'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__full_markup_list(self, p):
#        'book_body : book_body full_markup_list'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__lilypond_header(self, p):
#        'book_body : book_body lilypond_header'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__paper_block(self, p):
#        'book_body : book_body paper_block'
#        p[0] = Node('book_body', p[1:])


#    def p_book_body__book_body__score_block(self, p):
#        'book_body : book_body score_block'
#        p[0] = Node('book_body', p[1:])


    ### bookpart_block ###


#    def p_bookpart_block__BOOKPART__Chr123__bookpart_body__Chr125(self, p):
#        "bookpart_block : BOOKPART '{' bookpart_body '}'"
#        p[0] = Node('bookpart_block', p[1:])


    ### bookpart_body ###


#    def p_bookpart_body__Empty(self, p):
#        'bookpart_body : '
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__BOOK_IDENTIFIER(self, p):
#        'bookpart_body : BOOK_IDENTIFIER'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__composite_music(self, p):
#        'bookpart_body : bookpart_body composite_music'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__embedded_scm(self, p):
#        'bookpart_body : bookpart_body embedded_scm'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__error(self, p):
#        'bookpart_body : bookpart_body error'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__full_markup(self, p):
#        'bookpart_body : bookpart_body full_markup'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__full_markup_list(self, p):
#        'bookpart_body : bookpart_body full_markup_list'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__lilypond_header(self, p):
#        'bookpart_body : bookpart_body lilypond_header'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__paper_block(self, p):
#        'bookpart_body : bookpart_body paper_block'
#        p[0] = Node('bookpart_body', p[1:])


#    def p_bookpart_body__bookpart_body__score_block(self, p):
#        'bookpart_body : bookpart_body score_block'
#        p[0] = Node('bookpart_body', p[1:])


    ### br_bass_figure ###


#    def p_br_bass_figure__Chr91__bass_figure(self, p):
#        "br_bass_figure : '[' bass_figure"
#        p[0] = Node('br_bass_figure', p[1:])


#    def p_br_bass_figure__bass_figure(self, p):
#        'br_bass_figure : bass_figure'
#        p[0] = Node('br_bass_figure', p[1:])


    ### braced_music_list ###


    def p_braced_music_list__Chr123__music_list__Chr125(self, p):
        "braced_music_list : '{' music_list '}'"
        p[0] = p[2]


    ### chord_body ###


    def p_chord_body__ANGLE_OPEN__chord_body_elements__ANGLE_CLOSE(self, p):
        'chord_body : ANGLE_OPEN chord_body_elements ANGLE_CLOSE'
        p[0] = p[2]


    ### chord_body_element ###


#    def p_chord_body_element__DRUM_PITCH__post_events(self, p):
#        'chord_body_element : DRUM_PITCH post_events'
#        p[0] = Node('chord_body_element', p[1:])


    def p_chord_body_element__music_function_chord_body(self, p):
        'chord_body_element : music_function_chord_body'
        p[0] = Node('chord_body_element', p[1:])


    def p_chord_body_element__pitch__exclamations__questions__octave_check__post_events(self, p):
        'chord_body_element : pitch exclamations questions octave_check post_events'
        p[0] = Node('chord_body_element', p[1:])

    ### chord_body_elements ###


    def p_chord_body_elements__Empty(self, p):
        'chord_body_elements : '
        p[0] = [ ]


    def p_chord_body_elements__chord_body_elements__chord_body_element(self, p):
        'chord_body_elements : chord_body_elements chord_body_element'
        p[0] = p[1] + [p[2]]


    ### chord_item ###


#    def p_chord_item__CHORD_MODIFIER(self, p):
#        'chord_item : CHORD_MODIFIER'
#        p[0] = Node('chord_item', p[1:])


#    def p_chord_item__chord_separator(self, p):
#        'chord_item : chord_separator'
#        p[0] = Node('chord_item', p[1:])


#    def p_chord_item__step_numbers(self, p):
#        'chord_item : step_numbers'
#        p[0] = Node('chord_item', p[1:])


    ### chord_items ###


#    def p_chord_items__Empty(self, p):
#        'chord_items : '
#        p[0] = Node('chord_items', p[1:])


#    def p_chord_items__chord_items__chord_item(self, p):
#        'chord_items : chord_items chord_item'
#        p[0] = Node('chord_items', p[1:])


    ### chord_separator ###


#    def p_chord_separator__CHORD_BASS__steno_tonic_pitch(self, p):
#        'chord_separator : CHORD_BASS steno_tonic_pitch'
#        p[0] = Node('chord_separator', p[1:])


#    def p_chord_separator__CHORD_CARET(self, p):
#        'chord_separator : CHORD_CARET'
#        p[0] = Node('chord_separator', p[1:])


#    def p_chord_separator__CHORD_COLON(self, p):
#        'chord_separator : CHORD_COLON'
#        p[0] = Node('chord_separator', p[1:])


#    def p_chord_separator__CHORD_SLASH__steno_tonic_pitch(self, p):
#        'chord_separator : CHORD_SLASH steno_tonic_pitch'
#        p[0] = Node('chord_separator', p[1:])


    ### closed_music ###


    def p_closed_music__complex_music_prefix__closed_music(self, p):
        'closed_music : complex_music_prefix closed_music'
        p[0] = Node('closed_music', p[1:])


    def p_closed_music__music_bare(self, p):
        'closed_music : music_bare'
        p[0] = Node('closed_music', p[1:])


    ### command_element ###


    def p_command_element__Chr124(self, p):
        "command_element : '|'"
        p[0] = Event('BarCheck')


    def p_command_element__E_BACKSLASH(self, p):
        'command_element : E_BACKSLASH'
        p[0] = Event('VoiceSeparator')


#    def p_command_element__E_BRACKET_CLOSE(self, p):
#        'command_element : E_BRACKET_CLOSE'
#        raise Exception('Ligatures not supported.')


#    def p_command_element__E_BRACKET_OPEN(self, p):
#        'command_element : E_BRACKET_OPEN'
#        raise Exception('Ligatures not supported.')


    def p_command_element__command_event(self, p):
        'command_element : command_event'
        p[0] = p[1]


    ### command_event ###


#    def p_command_event__E_TILDE(self, p):
#        'command_event : E_TILDE'
#        raise Exception('Pes or Flexa events not supported.')


    def p_command_event__tempo_event(self, p):
        'command_event : tempo_event'
        p[0] = p[1]


    ### complex_music ###


    def p_complex_music__complex_music_prefix__music(self, p):
        'complex_music : complex_music_prefix music'
        context = p[1][1]
        optional_id = p[1][2]
        optional_context_mod = p[1][3]
        music = p[2]
        p[0] = self.client._construct_context_specced_music(
            context, optional_id, optional_context_mod, music)


    def p_complex_music__music_function_call(self, p):
        'complex_music : music_function_call'
        p[0] = p[1]


#    def p_complex_music__re_rhythmed_music(self, p):
#        'complex_music : re_rhythmed_music'
#        p[0] = Node('complex_music', p[1:])


#    def p_complex_music__repeated_music(self, p):
#        'complex_music : repeated_music'
#        p[0] = Node('complex_music', p[1:])


    ### complex_music_prefix ###


    def p_complex_music_prefix__CONTEXT__simple_string__optional_id__optional_context_mod(self, p):
        'complex_music_prefix : CONTEXT simple_string optional_id optional_context_mod'
        p[0] = Node('complex_music_prefix', p[1:])


    def p_complex_music_prefix__NEWCONTEXT__simple_string__optional_id__optional_context_mod(self, p):
        'complex_music_prefix : NEWCONTEXT simple_string optional_id optional_context_mod'
        p[0] = Node('complex_music_prefix', p[1:])


    ### composite_music ###


    def p_composite_music__complex_music(self, p):
        'composite_music : complex_music'
        p[0] = p[1]


    def p_composite_music__music_bare(self, p):
        'composite_music : music_bare'
        p[0] = p[1]


    ### context_change ###


    def p_context_change__CHANGE__STRING__Chr61__STRING(self, p):
        "context_change : CHANGE STRING '=' STRING"
        p[0] = Node('context_change', p[1:])


    ### context_def_mod ###


#    def p_context_def_mod__ACCEPTS(self, p):
#        'context_def_mod : ACCEPTS'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__ALIAS(self, p):
#        'context_def_mod : ALIAS'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__CONSISTS(self, p):
#        'context_def_mod : CONSISTS'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__DEFAULTCHILD(self, p):
#        'context_def_mod : DEFAULTCHILD'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__DENIES(self, p):
#        'context_def_mod : DENIES'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__DESCRIPTION(self, p):
#        'context_def_mod : DESCRIPTION'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__NAME(self, p):
#        'context_def_mod : NAME'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__REMOVE(self, p):
#        'context_def_mod : REMOVE'
#        p[0] = Node('context_def_mod', p[1:])


#    def p_context_def_mod__TYPE(self, p):
#        'context_def_mod : TYPE'
#        p[0] = Node('context_def_mod', p[1:])


    ### context_def_spec_block ###


    def p_context_def_spec_block__CONTEXT__Chr123__context_def_spec_body__Chr125(self, p):
        "context_def_spec_block : CONTEXT '{' context_def_spec_body '}'"
        p[0] = Node('context_def_spec_block', p[1:])


    ### context_def_spec_body ###


    def p_context_def_spec_body__Empty(self, p):
        'context_def_spec_body : '
        p[0] = Node('context_def_spec_body', p[1:])


    def p_context_def_spec_body__CONTEXT_DEF_IDENTIFIER(self, p):
        'context_def_spec_body : CONTEXT_DEF_IDENTIFIER'
        p[0] = Node('context_def_spec_body', p[1:])


    def p_context_def_spec_body__context_def_spec_body__context_mod(self, p):
        'context_def_spec_body : context_def_spec_body context_mod'
        p[0] = Node('context_def_spec_body', p[1:])


    def p_context_def_spec_body__context_def_spec_body__context_modification(self, p):
        'context_def_spec_body : context_def_spec_body context_modification'
        p[0] = Node('context_def_spec_body', p[1:])


    def p_context_def_spec_body__context_def_spec_body__embedded_scm(self, p):
        'context_def_spec_body : context_def_spec_body embedded_scm'
        p[0] = Node('context_def_spec_body', p[1:])


    ### context_mod ###


#    def p_context_mod__context_def_mod__STRING(self, p):
#        'context_mod : context_def_mod STRING'
#        p[0] = Node('context_mod', p[1:])


#    def p_context_mod__context_def_mod__embedded_scm(self, p):
#        'context_mod : context_def_mod embedded_scm'
#        p[0] = Node('context_mod', p[1:])


    def p_context_mod__property_operation(self, p):
        'context_mod : property_operation'
        p[0] = p[1]


    ### context_mod_list ###


    def p_context_mod_list__Empty(self, p):
        'context_mod_list : '
        p[0] = [ ]


    def p_context_mod_list__context_mod_list__CONTEXT_MOD_IDENTIFIER(self, p):
        'context_mod_list : context_mod_list CONTEXT_MOD_IDENTIFIER'
        p[0] = p[1] + [p[2]]


    def p_context_mod_list__context_mod_list__context_mod(self, p):
        'context_mod_list : context_mod_list context_mod'
        p[0] = p[1] + [p[2]]


    def p_context_mod_list__context_mod_list__embedded_scm(self, p):
        'context_mod_list : context_mod_list embedded_scm'
        p[0] = p[1] + [p[2]]


    ### context_modification ###


    def p_context_modification__CONTEXT_MOD_IDENTIFIER(self, p):
        'context_modification : CONTEXT_MOD_IDENTIFIER'
        p[0] = [p[1]]


    def p_context_modification__WITH__CONTEXT_MOD_IDENTIFIER(self, p):
        'context_modification : WITH CONTEXT_MOD_IDENTIFIER'
        p[0] = [p[2]]


    def p_context_modification__WITH__Chr123__context_mod_list__Chr125(self, p):
        "context_modification : WITH '{' context_mod_list '}'"
        p[0] = p[3]
        self.client._lexer.pop_state( )


    def p_context_modification__WITH__embedded_scm_closed(self, p):
        'context_modification : WITH embedded_scm_closed'
        p[0] = [p[2]]


    ### context_prop_spec ###


    def p_context_prop_spec__simple_string(self, p):
        'context_prop_spec : simple_string'
        p[0] = Node('context_prop_spec', p[1:])


    def p_context_prop_spec__simple_string__Chr46__simple_string(self, p):
        "context_prop_spec : simple_string '.' simple_string"
        p[0] = Node('context_prop_spec', p[1:])


    ### direction_less_char ###


    def p_direction_less_char__Chr126(self, p):
        "direction_less_char : '~'"
        p[0] = self.client._resolve_event_identifier('tildeSymbol')


    def p_direction_less_char__Chr40(self, p):
        "direction_less_char : '('"
        p[0] = self.client._resolve_event_identifier('parenthesisOpenSymbol')


    def p_direction_less_char__Chr41(self, p):
        "direction_less_char : ')'"
        p[0] = self.client._resolve_event_identifier('parenthesisCloseSymbol')


    def p_direction_less_char__Chr91(self, p):
        "direction_less_char : '['"
        p[0] = self.client._resolve_event_identifier('bracketOpenSymbol')


    def p_direction_less_char__Chr93(self, p):
        "direction_less_char : ']'"
        p[0] = self.client._resolve_event_identifier('bracketCloseSymbol')


    def p_direction_less_char__E_ANGLE_CLOSE(self, p):
        'direction_less_char : E_ANGLE_CLOSE'
        p[0] = self.client._resolve_event_identifier('escapedBiggerSymbol')


    def p_direction_less_char__E_ANGLE_OPEN(self, p):
        'direction_less_char : E_ANGLE_OPEN'
        p[0] = self.client._resolve_event_identifier('escapedSmallerSymbol')


    def p_direction_less_char__E_CLOSE(self, p):
        'direction_less_char : E_CLOSE'
        p[0] = self.client._resolve_event_identifier('escapedParenthesisCloseSymbol')


    def p_direction_less_char__E_EXCLAMATION(self, p):
        'direction_less_char : E_EXCLAMATION'
        p[0] = self.client._resolve_event_identifier('escapedExclamationSymbol')


    def p_direction_less_char__E_OPEN(self, p):
        'direction_less_char : E_OPEN'
        p[0] = self.client._resolve_event_identifier('escapedParenthesisOpenSymbol')


    ### direction_less_event ###


    def p_direction_less_event__EVENT_IDENTIFIER(self, p):
        'direction_less_event : EVENT_IDENTIFIER'
        identifier = p[1]
        if identifier.startswith('\\'):
            identifier = identifier[1:]
        p[0] = self.client._resolve_event_identifier(identifier)


    def p_direction_less_event__direction_less_char(self, p):
        'direction_less_event : direction_less_char'
        p[0] = p[1]


    def p_direction_less_event__event_function_event(self, p):
        'direction_less_event : event_function_event'
        p[0] = Node('direction_less_event', p[1:])


    def p_direction_less_event__tremolo_type(self, p):
        'direction_less_event : tremolo_type'
        p[0] = p[1]


    ### direction_reqd_event ###


    def p_direction_reqd_event__gen_text_def(self, p):
        'direction_reqd_event : gen_text_def'
        p[0] = p[1]


    def p_direction_reqd_event__script_abbreviation(self, p):
        'direction_reqd_event : script_abbreviation'
        p[0] = p[1]


    ### dots ###


    def p_dots__Empty(self, p):
        'dots : '
        p[0] = Node('dots', 0)


    def p_dots__dots__Chr46(self, p):
        "dots : dots '.'"
        p[0] = Node('dots', p[1].value + 1)


    ### duration_length ###


    def p_duration_length__multiplied_duration(self, p):
        'duration_length : multiplied_duration'
        p[0] = p[1]


    ### embedded_lilypond ###


#    def p_embedded_lilypond__Empty(self, p):
#        'embedded_lilypond : '
#        p[0] = Node('embedded_lilypond', p[1:])


#    def p_embedded_lilypond__INVALID__embedded_lilypond(self, p):
#        'embedded_lilypond : INVALID embedded_lilypond'
#        p[0] = Node('embedded_lilypond', p[1:])


#    def p_embedded_lilypond__error(self, p):
#        'embedded_lilypond : error'
#        p[0] = Node('embedded_lilypond', p[1:])


#    def p_embedded_lilypond__identifier_init(self, p):
#        'embedded_lilypond : identifier_init'
#        p[0] = Node('embedded_lilypond', p[1:])


#    def p_embedded_lilypond__music__music__music_list(self, p):
#        'embedded_lilypond : music music music_list'
#        p[0] = Node('embedded_lilypond', p[1:])


    ### embedded_scm ###


    def p_embedded_scm__embedded_scm_bare(self, p):
        'embedded_scm : embedded_scm_bare'
        p[0] = p[1]


    def p_embedded_scm__scm_function_call(self, p):
        'embedded_scm : scm_function_call'
        p[0] = p[1]


    ### embedded_scm_arg ###


    def p_embedded_scm_arg__embedded_scm_bare_arg(self, p):
        'embedded_scm_arg : embedded_scm_bare_arg'
        p[0] = p[1]


    def p_embedded_scm_arg__music_arg(self, p):
        'embedded_scm_arg : music_arg'
        p[0] = p[1]


    def p_embedded_scm_arg__scm_function_call(self, p):
        'embedded_scm_arg : scm_function_call'
        p[0] = p[1]


    ### embedded_scm_arg_closed ###


    def p_embedded_scm_arg_closed__closed_music(self, p):
        'embedded_scm_arg_closed : closed_music'
        p[0] = p[1]


    def p_embedded_scm_arg_closed__embedded_scm_bare_arg(self, p):
        'embedded_scm_arg_closed : embedded_scm_bare_arg'
        p[0] = p[1]


    def p_embedded_scm_arg_closed__scm_function_call_closed(self, p):
        'embedded_scm_arg_closed : scm_function_call_closed'
        p[0] = p[1]


    ### embedded_scm_bare ###


    def p_embedded_scm_bare__SCM_IDENTIFIER(self, p):
        'embedded_scm_bare : SCM_IDENTIFIER'
        p[0] = p[1]


    def p_embedded_scm_bare__SCM_TOKEN(self, p):
        'embedded_scm_bare : SCM_TOKEN'
        p[0] = p[1]


    ### embedded_scm_bare_arg ###


    def p_embedded_scm_bare_arg__STRING(self, p):
        'embedded_scm_bare_arg : STRING'
        p[0] = p[1]


    def p_embedded_scm_bare_arg__STRING_IDENTIFIER(self, p):
        'embedded_scm_bare_arg : STRING_IDENTIFIER'
        p[0] = p[1]


#    def p_embedded_scm_bare_arg__book_block(self, p):
#        'embedded_scm_bare_arg : book_block'
#        p[0] = p[1]


#    def p_embedded_scm_bare_arg__bookpart_block(self, p):
#        'embedded_scm_bare_arg : bookpart_block'
#        p[0] = p[1]


    def p_embedded_scm_bare_arg__context_def_spec_block(self, p):
        'embedded_scm_bare_arg : context_def_spec_block'
        p[0] = p[1]


    def p_embedded_scm_bare_arg__context_modification(self, p):
        'embedded_scm_bare_arg : context_modification'
        p[0] = p[1]



    def p_embedded_scm_bare_arg__embedded_scm_bare(self, p):
        'embedded_scm_bare_arg : embedded_scm_bare'
        p[0] = p[1]


    def p_embedded_scm_bare_arg__full_markup(self, p):
        'embedded_scm_bare_arg : full_markup'
        p[0] = p[1]


    def p_embedded_scm_bare_arg__full_markup_list(self, p):
        'embedded_scm_bare_arg : full_markup_list'
        p[0] = p[1]


#    def p_embedded_scm_bare_arg__output_def(self, p):
#        'embedded_scm_bare_arg : output_def'
#        p[0] = p[1]


    def p_embedded_scm_bare_arg__score_block(self, p):
        'embedded_scm_bare_arg : score_block'
        p[0] = p[1]


    ### embedded_scm_chord_body ###


    def p_embedded_scm_chord_body__SCM_FUNCTION__music_function_chord_body_arglist(self, p):
        'embedded_scm_chord_body : SCM_FUNCTION music_function_chord_body_arglist'
        p[0] = Node('embedded_scm_chord_body', p[1:])


    def p_embedded_scm_chord_body__bare_number(self, p):
        'embedded_scm_chord_body : bare_number'
        p[0] = p[1]


    def p_embedded_scm_chord_body__chord_body_element(self, p):
        'embedded_scm_chord_body : chord_body_element'
        p[0] = p[1]


    def p_embedded_scm_chord_body__embedded_scm_bare_arg(self, p):
        'embedded_scm_chord_body : embedded_scm_bare_arg'
        p[0] = p[1]


    def p_embedded_scm_chord_body__fraction(self, p):
        'embedded_scm_chord_body : fraction'
        p[0] = p[1]


#    def p_embedded_scm_chord_body__lyric_element(self, p):
#        'embedded_scm_chord_body : lyric_element'
#        p[0] = p[1]


    ### embedded_scm_closed ###


    def p_embedded_scm_closed__embedded_scm_bare(self, p):
        'embedded_scm_closed : embedded_scm_bare'
        p[0] = p[1]


    def p_embedded_scm_closed__scm_function_call_closed(self, p):
        'embedded_scm_closed : scm_function_call_closed'
        p[0] = p[1]


    ### event_chord ###


    def p_event_chord__CHORD_REPETITION__optional_notemode_duration__post_events(self, p):
        'event_chord : CHORD_REPETITION optional_notemode_duration post_events'
        pitches = self.client._last_chord.written_pitches
        duration = p[2].duration
        chord = Chord(pitches, duration)
        self.client._chord_pitch_orders[chord] = pitches
        if p[2].multiplier is not None:
            chord.duration_multiplier = p[2].multiplier
        self.client._process_post_events(chord, p[3])
        marktools.Annotation('UnrelativableMusic')(chord)
        if self.client._last_chord not in self.client._repeated_chords:
            self.client._repeated_chords[self.client._last_chord] = [ ]
        self.client._repeated_chords[self.client._last_chord].append(chord)
        p[0] = chord


    def p_event_chord__MULTI_MEASURE_REST__optional_notemode_duration__post_events(self, p):
        'event_chord : MULTI_MEASURE_REST optional_notemode_duration post_events'
        rest = resttools.MultiMeasureRest(p[2].duration)
        if p[2].multiplier is not None:
            rest.duration_multiplier = p[2].multiplier
        self.client._process_post_events(rest, p[3])
        p[0] = rest


    def p_event_chord__command_element(self, p):
        'event_chord : command_element'
        p[0] = p[1]


    def p_event_chord__note_chord_element(self, p):
        'event_chord : note_chord_element'
        self.client._last_chord = p[1]
        p[0] = p[1]


    def p_event_chord__simple_chord_elements__post_events(self, p):
        'event_chord : simple_chord_elements post_events'
        self.client._process_post_events(p[1], p[2])
        p[0] = p[1]


    ### event_function_event ###


    def p_event_function_event__EVENT_FUNCTION__function_arglist_closed(self, p):
        'event_function_event : EVENT_FUNCTION function_arglist_closed'
        p[0] = Node('event_function_event', p[1:])


    ### exclamations ###


    def p_exclamations__Empty(self, p):
        'exclamations : '
        p[0] = ''


    def p_exclamations__exclamations__Chr33(self, p):
        "exclamations : exclamations '!'"
        p[0] = p[1] + '!'


    ### figure_list ###


#    def p_figure_list__Empty(self, p):
#        'figure_list : '
#        p[0] = Node('figure_list', p[1:])


#    def p_figure_list__figure_list__br_bass_figure(self, p):
#        'figure_list : figure_list br_bass_figure'
#        p[0] = Node('figure_list', p[1:])


    ### figure_spec ###


#    def p_figure_spec__FIGURE_OPEN__figure_list__FIGURE_CLOSE(self, p):
#        'figure_spec : FIGURE_OPEN figure_list FIGURE_CLOSE'
#        p[0] = Node('figure_spec', p[1:])


    ### figured_bass_alteration ###


#    def p_figured_bass_alteration__Chr33(self, p):
#        "figured_bass_alteration : '!'"
#        p[0] = Node('figured_bass_alteration', p[1:])


#    def p_figured_bass_alteration__Chr43(self, p):
#        "figured_bass_alteration : '+'"
#        p[0] = Node('figured_bass_alteration', p[1:])


#    def p_figured_bass_alteration__Chr45(self, p):
#        "figured_bass_alteration : '-'"
#        p[0] = Node('figured_bass_alteration', p[1:])


    ### figured_bass_modification ###


#    def p_figured_bass_modification__Chr47(self, p):
#        "figured_bass_modification : '/'"
#        p[0] = Node('figured_bass_modification', p[1:])


#    def p_figured_bass_modification__E_BACKSLASH(self, p):
#        'figured_bass_modification : E_BACKSLASH'
#        p[0] = Node('figured_bass_modification', p[1:])


#    def p_figured_bass_modification__E_EXCLAMATION(self, p):
#        'figured_bass_modification : E_EXCLAMATION'
#        p[0] = Node('figured_bass_modification', p[1:])


#    def p_figured_bass_modification__E_PLUS(self, p):
#        'figured_bass_modification : E_PLUS'
#        p[0] = Node('figured_bass_modification', p[1:])


    ### fingering ###


    def p_fingering__UNSIGNED(self, p):
        'fingering : UNSIGNED'
        p[0] = Node('fingering', p[1:])


    ### fraction ###


    def p_fraction__FRACTION(self, p):
        'fraction : FRACTION'
        p[0] = p[1]


    def p_fraction__UNSIGNED__Chr47__UNSIGNED(self, p):
        "fraction : UNSIGNED '/' UNSIGNED"
        p[0] = Fraction(p[1], p[3])


    ### full_markup ###


    def p_full_markup__MARKUP_IDENTIFIER(self, p):
        'full_markup : MARKUP_IDENTIFIER'
        p[0] = Node('full_markup', p[1:])


    def p_full_markup__MARKUP__markup_top(self, p):
        'full_markup : MARKUP markup_top'
        p[0] = markuptools.Markup(p[2])


    ### full_markup_list ###


    def p_full_markup_list__MARKUPLIST_IDENTIFIER(self, p):
        'full_markup_list : MARKUPLIST_IDENTIFIER'
        p[0] = Node('full_markup_list', p[1:])


    def p_full_markup_list__MARKUPLIST__markup_list(self, p):
        'full_markup_list : MARKUPLIST markup_list'
        p[0] = Node('full_markup_list', p[1:])


    ### function_arglist ###


    def p_function_arglist__function_arglist_common(self, p):
        'function_arglist : function_arglist_common'
        p[0] = p[1]


    def p_function_arglist__function_arglist_nonbackup(self, p):
        'function_arglist : function_arglist_nonbackup'
        p[0] = p[1]


    ### function_arglist_backup ###


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed_keep__duration_length(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_closed_keep duration_length'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_keep__pitch_also_in_chords(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_keep pitch_also_in_chords'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_backup__BACKUP(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_backup BACKUP'
        p[0] = p[3] + [p[1]]
        self.client._backup_token(False, None)


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__NUMBER_IDENTIFIER(self, p):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep '-' NUMBER_IDENTIFIER"
        n = -1 * p[5]
        if self.client._test_scheme_predicate(p[2], n):
            p[0] = p[3] + [p[1]]
        else:
            self.client._backup_token('NUMBER_IDENTIFIER', n)


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__REAL(self, p):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep '-' REAL"
        n = -1 * p[5]
        if self.client._test_scheme_predicate(p[2], n):
            self.client._reparse_token(p[2], 'REAL', n)
            p[0] = p[3]
        else:
            self.client._backup_token('REAL', n)


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__Chr45__UNSIGNED(self, p):
        "function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep '-' UNSIGNED"
        n = -1 * p[5]
        if self.client._test_scheme_predicates(p[2], n):
            self.client._reparse_token(p[2], 'REAL', n)
            p[0] = p[3]
        else:
            # This would normally create a FingeringEvent, and test that against the predicate
            self.client._backup_token('REAL', n)
            p[0] = p[3] + [p[1]]


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__FRACTION(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep FRACTION'
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token('FRACTION', p[4])


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__NUMBER_IDENTIFIER(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep NUMBER_IDENTIFIER'
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token('NUMBER_IDENTIFIER', p[4])


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__REAL(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep REAL'
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3]         
            self.client._reparse_token(p[2], 'REAL', p[4])
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token('REAL', p[4])


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__UNSIGNED(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep UNSIGNED'
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3]
            self.client._reparse_token(p[2], 'UNSIGNED', p[4])
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token('UNSIGNED', p[4])


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed_keep__post_event_nofinger(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed_keep post_event_nofinger'
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token('EVENT_IDENTIFIER', p[4])


    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_keep__embedded_scm_arg_closed(self, p):
        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_keep embedded_scm_arg_closed'
        if self.client._test_scheme_predicate(p[2], p[4]):
            p[0] = p[3] + [p[4]]
        else:
            p[0] = p[3] + [p[1]]
            self.client._backup_token('SCM_IDENTIFIER', p[4])


#    def p_function_arglist_backup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_keep__lyric_element(self, p):
#        'function_arglist_backup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_keep lyric_element'
#        if self.client._test_scheme_predicate(p[2], p[4]):
#            p[0] = p[3] + [p[4]]
#        else:
#            p[0] = p[3] + [p[1]]
#            self.client._backup_token('LYRICS_STRING', p[4])


    def p_function_arglist_backup__function_arglist_backup__REPARSE__bare_number(self, p):
        'function_arglist_backup : function_arglist_backup REPARSE bare_number'
        p[0] = self.client._check_scheme_argument(p[1], p[3], p[2])


    def p_function_arglist_backup__function_arglist_backup__REPARSE__embedded_scm_arg_closed(self, p):
        'function_arglist_backup : function_arglist_backup REPARSE embedded_scm_arg_closed'
        p[0] = self.client._check_scheme_argument(p[1], p[3], p[2])


    def p_function_arglist_backup__function_arglist_backup__REPARSE__fraction(self, p):
        'function_arglist_backup : function_arglist_backup REPARSE fraction'
        p[0] = self.client._check_scheme_argument(p[1], p[3], p[2])


    ### function_arglist_bare ###


    def p_function_arglist_bare__EXPECT_DURATION__function_arglist_closed_optional__duration_length(self, p):
        'function_arglist_bare : EXPECT_DURATION function_arglist_closed_optional duration_length'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_bare__EXPECT_NO_MORE_ARGS(self, p):
        'function_arglist_bare : EXPECT_NO_MORE_ARGS'
        p[0] = [ ]


    def p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_skip__DEFAULT(self, p):
        'function_arglist_bare : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_skip DEFAULT'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_skip__DEFAULT(self, p):
        'function_arglist_bare : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_skip DEFAULT'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_bare__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip__DEFAULT(self, p):
        'function_arglist_bare : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip DEFAULT'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_bare__EXPECT_PITCH__function_arglist_optional__pitch_also_in_chords(self, p):
        'function_arglist_bare : EXPECT_PITCH function_arglist_optional pitch_also_in_chords'
        p[0] = p[2] + [p[3]]


    ### function_arglist_closed ###


    def p_function_arglist_closed__function_arglist_closed_common(self, p):
        'function_arglist_closed : function_arglist_closed_common'
        p[0] = p[1]


    def p_function_arglist_closed__function_arglist_nonbackup(self, p):
        'function_arglist_closed : function_arglist_nonbackup'
        p[0] = p[1]


    ### function_arglist_closed_common ###


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__NUMBER_IDENTIFIER(self, p):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional '-' NUMBER_IDENTIFIER"
        p[0] = p[2] + [-1 * p[4]]


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__REAL(self, p):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional '-' REAL"
        p[0] = p[2] + [-1 * p[4]]


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__Chr45__UNSIGNED(self, p):
        "function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional '-' UNSIGNED"
        p[0] = p[2] + [-1 * p[4]]


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__bare_number(self, p):
        'function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional bare_number'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__fraction(self, p):
        'function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional fraction'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_closed_optional__post_event_nofinger(self, p):
        'function_arglist_closed_common : EXPECT_SCM function_arglist_closed_optional post_event_nofinger'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg_closed(self, p):
        'function_arglist_closed_common : EXPECT_SCM function_arglist_optional embedded_scm_arg_closed'
        p[0] = p[2] + [p[3]]


#    def p_function_arglist_closed_common__EXPECT_SCM__function_arglist_optional__lyric_element(self, p):
#        'function_arglist_closed_common : EXPECT_SCM function_arglist_optional lyric_element'
#        p[0] = p[2] + [p[3]]


    def p_function_arglist_closed_common__function_arglist_bare(self, p):
        'function_arglist_closed_common : function_arglist_bare'
        p[0] = p[1]


    ### function_arglist_closed_keep ###


    def p_function_arglist_closed_keep__function_arglist_backup(self, p):
        'function_arglist_closed_keep : function_arglist_backup'
        p[0] = p[1]


    def p_function_arglist_closed_keep__function_arglist_closed_common(self, p):
        'function_arglist_closed_keep : function_arglist_closed_common'
        p[0] = p[1]


    ### function_arglist_closed_optional ###


    def p_function_arglist_closed_optional__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed_optional(self, p):
        'function_arglist_closed_optional : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_closed_optional'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_closed_optional__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_closed_optional(self, p):
        'function_arglist_closed_optional : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_closed_optional'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_closed_optional__function_arglist_backup__BACKUP(self, p):
        'function_arglist_closed_optional : function_arglist_backup BACKUP'
        p[0] = p[1]


    def p_function_arglist_closed_optional__function_arglist_closed_keep(self, p):
        'function_arglist_closed_optional : function_arglist_closed_keep %prec FUNCTION_ARGLIST'
        p[0] = p[1]


    ### function_arglist_common ###


    def p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__bare_number(self, p):
        'function_arglist_common : EXPECT_SCM function_arglist_closed_optional bare_number'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__fraction(self, p):
        'function_arglist_common : EXPECT_SCM function_arglist_closed_optional fraction'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_common__EXPECT_SCM__function_arglist_closed_optional__post_event_nofinger(self, p):
        'function_arglist_common : EXPECT_SCM function_arglist_closed_optional post_event_nofinger'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_common__EXPECT_SCM__function_arglist_optional__embedded_scm_arg(self, p):
        'function_arglist_common : EXPECT_SCM function_arglist_optional embedded_scm_arg'
        p[0] = p[2] + [p[3]]


    def p_function_arglist_common__function_arglist_bare(self, p):
        'function_arglist_common : function_arglist_bare'
        p[0] = p[1]


#    def p_function_arglist_common__function_arglist_common_lyric(self, p):
#        'function_arglist_common : function_arglist_common_lyric'
#        p[0] = p[1]


    def p_function_arglist_common__function_arglist_common_minus(self, p):
        'function_arglist_common : function_arglist_common_minus'
        p[0] = p[1]


    ### function_arglist_common_lyric ###


#    def p_function_arglist_common_lyric__EXPECT_SCM__function_arglist_optional__lyric_element(self, p):
#        'function_arglist_common_lyric : EXPECT_SCM function_arglist_optional lyric_element'
#        p[0] = p[2] + [p[3]]


#    def p_function_arglist_common_lyric__function_arglist_common_lyric__REPARSE__lyric_element_arg(self, p):
#        'function_arglist_common_lyric : function_arglist_common_lyric REPARSE lyric_element_arg'
#        p[0] = p[1] + [p[3]]


    ### function_arglist_common_minus ###


    def p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__NUMBER_IDENTIFIER(self, p):
        "function_arglist_common_minus : EXPECT_SCM function_arglist_closed_optional '-' NUMBER_IDENTIFIER"
        p[0] = p[2] + [-1 * p[4]]


    def p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__REAL(self, p):
        "function_arglist_common_minus : EXPECT_SCM function_arglist_closed_optional '-' REAL"
        p[0] = p[2] + [-1 * p[3]]


    def p_function_arglist_common_minus__EXPECT_SCM__function_arglist_closed_optional__Chr45__UNSIGNED(self, p):
        "function_arglist_common_minus : EXPECT_SCM function_arglist_closed_optional '-' UNSIGNED"
        p[0] = p[2] + [-1 * p[3]]


    def p_function_arglist_common_minus__function_arglist_common_minus__REPARSE__bare_number(self, p):
        'function_arglist_common_minus : function_arglist_common_minus REPARSE bare_number'
        p[0] = p[1] + [p[3]]


    ### function_arglist_keep ###


    def p_function_arglist_keep__function_arglist_backup(self, p):
        'function_arglist_keep : function_arglist_backup'
        p[0] = p[1]


    def p_function_arglist_keep__function_arglist_common(self, p):
        'function_arglist_keep : function_arglist_common'
        p[0] = p[1]


    ### function_arglist_nonbackup ###


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_closed__duration_length(self, p):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_closed duration_length'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist__pitch_also_in_chords(self, p):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_PITCH function_arglist pitch_also_in_chords'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist__embedded_scm_arg_closed(self, p):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist embedded_scm_arg_closed'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__NUMBER_IDENTIFIER(self, p):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed '-' NUMBER_IDENTIFIER"
        p[0] = p[3] + [-1 * p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__REAL(self, p):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed '-' REAL"
        p[0] = p[3] + [-1 * p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__Chr45__UNSIGNED(self, p):
        "function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed '-' UNSIGNED"
        p[0] = p[3] + [-1 * p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__FRACTION(self, p):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed FRACTION'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__bare_number_closed(self, p):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed bare_number_closed'
        p[0] = p[3] + [p[4]]


    def p_function_arglist_nonbackup__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_closed__post_event_nofinger(self, p):
        'function_arglist_nonbackup : EXPECT_OPTIONAL EXPECT_SCM function_arglist_closed post_event_nofinger'
        p[0] = p[3] + [p[4]]


    ### function_arglist_optional ###


    def p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_optional(self, p):
        'function_arglist_optional : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_optional'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_optional__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_optional(self, p):
        'function_arglist_optional : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_optional'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_optional__function_arglist_backup__BACKUP(self, p):
        'function_arglist_optional : function_arglist_backup BACKUP'
        p[0] = p[1]


    def p_function_arglist_optional__function_arglist_keep(self, p):
        'function_arglist_optional : function_arglist_keep %prec FUNCTION_ARGLIST'
        p[0] = p[1]


    ### function_arglist_skip ###


    def p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_DURATION__function_arglist_skip(self, p):
        'function_arglist_skip : EXPECT_OPTIONAL EXPECT_DURATION function_arglist_skip %prec FUNCTION_ARGLIST'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_PITCH__function_arglist_skip(self, p):
        'function_arglist_skip : EXPECT_OPTIONAL EXPECT_PITCH function_arglist_skip %prec FUNCTION_ARGLIST'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_skip__EXPECT_OPTIONAL__EXPECT_SCM__function_arglist_skip(self, p):
        'function_arglist_skip : EXPECT_OPTIONAL EXPECT_SCM function_arglist_skip %prec FUNCTION_ARGLIST'
        p[0] = p[3] + [p[1]]


    def p_function_arglist_skip__function_arglist_common(self, p):
        'function_arglist_skip : function_arglist_common'
        p[0] = p[1]


    ### gen_text_def ###


    def p_gen_text_def__full_markup(self, p):
        'gen_text_def : full_markup'
        p[0] = p[1]


    def p_gen_text_def__simple_string(self, p):
        'gen_text_def : simple_string'
        p[0] = markuptools.Markup(p[1])


    ### grouped_music_list ###


    def p_grouped_music_list__sequential_music(self, p):
        'grouped_music_list : sequential_music'
        p[0] = p[1]


    def p_grouped_music_list__simultaneous_music(self, p):
        'grouped_music_list : simultaneous_music'
        p[0] = p[1]


    ### identifier_init ###


#    def p_identifier_init__book_block(self, p):
#        'identifier_init : book_block'
#        p[0] = Node('book_block', p[1])


#    def p_identifier_init__bookpart_block(self, p):
#        'identifier_init : bookpart_block'
#        p[0] = Node('bookpart_block', p[1])


    def p_identifier_init__context_def_spec_block(self, p):
        'identifier_init : context_def_spec_block'
        p[0] = Node('context_def_spec_block', p[1])


    def p_identifier_init__context_modification(self, p):
        'identifier_init : context_modification'
        p[0] = Node('context_modification', p[1])


    def p_identifier_init__embedded_scm(self, p):
        'identifier_init : embedded_scm'
        p[0] = Node('embedded_scm', p[1])


    def p_identifier_init__full_markup(self, p):
        'identifier_init : full_markup'
        p[0] = Node('full_markup', p[1])


    def p_identifier_init__full_markup_list(self, p):
        'identifier_init : full_markup_list'
        p[0] = Node('full_markup_list', p[1])


    def p_identifier_init__music(self, p):
        'identifier_init : music'
        p[0] = Node('music', p[1])


    def p_identifier_init__number_expression(self, p):
        'identifier_init : number_expression'
        p[0] = Node('number_expression', p[1])


#    def p_identifier_init__output_def(self, p):
#        'identifier_init : output_def'
#        p[0] = Node('output_def', p[1])


    def p_identifier_init__post_event_nofinger(self, p):
        'identifier_init : post_event_nofinger'
        p[0] = Node('post_event_nofinger', p[1])


    def p_identifier_init__score_block(self, p):
        'identifier_init : score_block'
        p[0] = Node('score_block', p[1])


    def p_identifier_init__string(self, p):
        'identifier_init : string'
        p[0] = Node('string', p[1])


    ### lilypond ###


    def p_lilypond__Empty(self, p):
        'lilypond : '
        p[0] = [ ]


#    def p_lilypond__lilypond__INVALID(self, p):
#        'lilypond : lilypond INVALID'
#        p[0] = p[1]


    def p_lilypond__lilypond__assignment(self, p):
        'lilypond : lilypond assignment'
        p[0] = p[1]
        if p[2] is not None:
            self.client._assignments[p[2][0]] = p[2][1]


    def p_lilypond__lilypond__error(self, p):
        'lilypond : lilypond error'
        p[0] = p[1]


    def p_lilypond__lilypond__toplevel_expression(self, p):
        'lilypond : lilypond toplevel_expression'
        p[0] = p[1] + [p[2]]


    ### lilypond_header ###


#    def p_lilypond_header__HEADER__Chr123__lilypond_header_body__Chr125(self, p):
#        "lilypond_header : HEADER '{' lilypond_header_body '}'"
#        p[0] = Node('lilypond_header', p[1:])


    ### lilypond_header_body ###


#    def p_lilypond_header_body__Empty(self, p):
#        'lilypond_header_body : '
#        p[0] = Node('lilypond_header_body', p[1:])


#    def p_lilypond_header_body__lilypond_header_body__assignment(self, p):
#        'lilypond_header_body : lilypond_header_body assignment'
#        p[0] = Node('lilypond_header_body', p[1:])


    ### lyric_element ###


#    def p_lyric_element__LYRICS_STRING(self, p):
#        'lyric_element : LYRICS_STRING'
#        p[0] = Node('lyric_element', p[1:])


#    def p_lyric_element__lyric_markup(self, p):
#        'lyric_element : lyric_markup'
#        p[0] = Node('lyric_element', p[1:])


    ### lyric_element_arg ###


#    def p_lyric_element_arg__LYRIC_ELEMENT__optional_notemode_duration__post_events(self, p):
#        'lyric_element_arg : LYRIC_ELEMENT optional_notemode_duration post_events'
#        p[0] = Node('lyric_element_arg', p[1:])


#    def p_lyric_element_arg__lyric_element(self, p):
#        'lyric_element_arg : lyric_element'
#        p[0] = Node('lyric_element_arg', p[1:])


#    def p_lyric_element_arg__lyric_element__multiplied_duration__post_events(self, p):
#        'lyric_element_arg : lyric_element multiplied_duration post_events'
#        p[0] = Node('lyric_element_arg', p[1:])


#    def p_lyric_element_arg__lyric_element__post_event__post_events(self, p):
#        'lyric_element_arg : lyric_element post_event post_events'
#        p[0] = Node('lyric_element_arg', p[1:])


    ### lyric_element_music ###


#    def p_lyric_element_music__lyric_element__optional_notemode_duration__post_events(self, p):
#        'lyric_element_music : lyric_element optional_notemode_duration post_events'
#        p[0] = Node('lyric_element_music', p[1:])


    ### lyric_markup ###


#    def p_lyric_markup__LYRIC_MARKUP_IDENTIFIER(self, p):
#        'lyric_markup : LYRIC_MARKUP_IDENTIFIER'
#        p[0] = Node('lyric_markup', p[1:])


#    def p_lyric_markup__LYRIC_MARKUP__markup_top(self, p):
#        'lyric_markup : LYRIC_MARKUP markup_top'
#        p[0] = Node('lyric_markup', p[1:])


    ### markup ###


    def p_markup__markup_head_1_list__simple_markup(self, p):
        'markup : markup_head_1_list simple_markup'
        p[0] = Node('markup', p[1:])


    def p_markup__simple_markup(self, p):
        'markup : simple_markup'
        p[0] = Node('markup', p[1:])


    ### markup_braced_list ###


    def p_markup_braced_list__Chr123__markup_braced_list_body__Chr125(self, p):
        "markup_braced_list : '{' markup_braced_list_body '}'"
        p[0] = Node('markup_braced_list', p[1:])


    ### markup_braced_list_body ###


    def p_markup_braced_list_body__Empty(self, p):
        'markup_braced_list_body : '
        p[0] = Node('markup_braced_list_body', p[1:])


    def p_markup_braced_list_body__markup_braced_list_body__markup(self, p):
        'markup_braced_list_body : markup_braced_list_body markup'
        p[0] = Node('markup_braced_list_body', p[1:])


    def p_markup_braced_list_body__markup_braced_list_body__markup_list(self, p):
        'markup_braced_list_body : markup_braced_list_body markup_list'
        p[0] = Node('markup_braced_list_body', p[1:])


    ### markup_command_basic_arguments ###


    def p_markup_command_basic_arguments__EXPECT_MARKUP_LIST__markup_command_list_arguments__markup_list(self, p):
        'markup_command_basic_arguments : EXPECT_MARKUP_LIST markup_command_list_arguments markup_list'
        p[0] = Node('markup_command_basic_arguments', p[1:])


    def p_markup_command_basic_arguments__EXPECT_NO_MORE_ARGS(self, p):
        'markup_command_basic_arguments : EXPECT_NO_MORE_ARGS'
        p[0] = Node('markup_command_basic_arguments', p[1:])


    def p_markup_command_basic_arguments__EXPECT_SCM__markup_command_list_arguments__embedded_scm_closed(self, p):
        'markup_command_basic_arguments : EXPECT_SCM markup_command_list_arguments embedded_scm_closed'
        p[0] = Node('markup_command_basic_arguments', p[1:])


    ### markup_command_list ###


    def p_markup_command_list__MARKUP_LIST_FUNCTION__markup_command_list_arguments(self, p):
        'markup_command_list : MARKUP_LIST_FUNCTION markup_command_list_arguments'
        p[0] = Node('markup_command_list', p[1:])


    ### markup_command_list_arguments ###


    def p_markup_command_list_arguments__EXPECT_MARKUP__markup_command_list_arguments__markup(self, p):
        'markup_command_list_arguments : EXPECT_MARKUP markup_command_list_arguments markup'
        p[0] = Node('markup_command_list_arguments', p[1:])


    def p_markup_command_list_arguments__markup_command_basic_arguments(self, p):
        'markup_command_list_arguments : markup_command_basic_arguments'
        p[0] = Node('markup_command_list_arguments', p[1:])


    ### markup_composed_list ###


    def p_markup_composed_list__markup_head_1_list__markup_braced_list(self, p):
        'markup_composed_list : markup_head_1_list markup_braced_list'
        p[0] = Node('markup_composed_list', p[1:])


    ### markup_head_1_item ###


    def p_markup_head_1_item__MARKUP_FUNCTION__EXPECT_MARKUP__markup_command_list_arguments(self, p):
        'markup_head_1_item : MARKUP_FUNCTION EXPECT_MARKUP markup_command_list_arguments'
        p[0] = Node('markup_head_1_item', p[1:])


    ### markup_head_1_list ###


    def p_markup_head_1_list__markup_head_1_item(self, p):
        'markup_head_1_list : markup_head_1_item'
        p[0] = Node('markup_head_1_list', p[1:])


    def p_markup_head_1_list__markup_head_1_list__markup_head_1_item(self, p):
        'markup_head_1_list : markup_head_1_list markup_head_1_item'
        p[0] = Node('markup_head_1_list', p[1:])


    ### markup_list ###


    def p_markup_list__MARKUPLIST_IDENTIFIER(self, p):
        'markup_list : MARKUPLIST_IDENTIFIER'
        p[0] = Node('markup_list', p[1:])


    def p_markup_list__markup_braced_list(self, p):
        'markup_list : markup_braced_list'
        p[0] = Node('markup_list', p[1:])


    def p_markup_list__markup_command_list(self, p):
        'markup_list : markup_command_list'
        p[0] = Node('markup_list', p[1:])


    def p_markup_list__markup_composed_list(self, p):
        'markup_list : markup_composed_list'
        p[0] = Node('markup_list', p[1:])


    def p_markup_list__markup_scm__MARKUPLIST_IDENTIFIER(self, p):
        'markup_list : markup_scm MARKUPLIST_IDENTIFIER'
        p[0] = Node('markup_list', p[1:])


    ### markup_scm ###


    def p_markup_scm__embedded_scm_bare__BACKUP(self, p):
        'markup_scm : embedded_scm_bare BACKUP'
        p[0] = Node('markup_scm', p[1:])


    ### markup_top ###


    def p_markup_top__markup_head_1_list__simple_markup(self, p):
        'markup_top : markup_head_1_list simple_markup'
        p[0] = Node('markup_top', p[1:])


    def p_markup_top__markup_list(self, p):
        'markup_top : markup_list'
        p[0] = Node('markup_top', p[1:])


    def p_markup_top__simple_markup(self, p):
        'markup_top : simple_markup'
        p[0] = Node('markup_top', p[1:])


    ### mode_changed_music ###


#    def p_mode_changed_music__mode_changing_head__grouped_music_list(self, p):
#        'mode_changed_music : mode_changing_head grouped_music_list'
#        p[0] = Node('mode_changed_music', p[1:])


#    def p_mode_changed_music__mode_changing_head_with_context__optional_context_mod__grouped_music_list(self, p):
#        'mode_changed_music : mode_changing_head_with_context optional_context_mod grouped_music_list'
#        p[0] = Node('mode_changed_music', p[1:])


    ### mode_changing_head ###


#    def p_mode_changing_head__CHORDMODE(self, p):
#        'mode_changing_head : CHORDMODE'
#        p[0] = Node('mode_changing_head', p[1:])


#    def p_mode_changing_head__DRUMMODE(self, p):
#        'mode_changing_head : DRUMMODE'
#        p[0] = Node('mode_changing_head', p[1:])


#    def p_mode_changing_head__FIGUREMODE(self, p):
#        'mode_changing_head : FIGUREMODE'
#        p[0] = Node('mode_changing_head', p[1:])


#    def p_mode_changing_head__LYRICMODE(self, p):
#        'mode_changing_head : LYRICMODE'
#        p[0] = Node('mode_changing_head', p[1:])


#    def p_mode_changing_head__NOTEMODE(self, p):
#        'mode_changing_head : NOTEMODE'
#        p[0] = Node('mode_changing_head', p[1:])


    ### mode_changing_head_with_context ###


#    def p_mode_changing_head_with_context__CHORDS(self, p):
#        'mode_changing_head_with_context : CHORDS'
#        p[0] = Node('mode_changing_head_with_context', p[1:])


#    def p_mode_changing_head_with_context__DRUMS(self, p):
#        'mode_changing_head_with_context : DRUMS'
#        p[0] = Node('mode_changing_head_with_context', p[1:])


#    def p_mode_changing_head_with_context__FIGURES(self, p):
#        'mode_changing_head_with_context : FIGURES'
#        p[0] = Node('mode_changing_head_with_context', p[1:])


#    def p_mode_changing_head_with_context__LYRICS(self, p):
#        'mode_changing_head_with_context : LYRICS'
#        p[0] = Node('mode_changing_head_with_context', p[1:])


    ### multiplied_duration ###


    def p_multiplied_duration__multiplied_duration__Chr42__FRACTION(self, p):
        "multiplied_duration : multiplied_duration '*' FRACTION"
        if p[1].multiplier is not None:
            p[0] = _LilyPondDuration(p[1].duration, p[1].multiplier * p[3])
        else:
            p[0] = _LilyPondDuration(p[1].duration, Fraction(p[3].numerator, p[3].denominator))


    def p_multiplied_duration__multiplied_duration__Chr42__bare_unsigned(self, p):
        "multiplied_duration : multiplied_duration '*' bare_unsigned"
        if p[1].multiplier is not None:
            p[0] = _LilyPondDuration(p[1].duration, p[1].multiplier * p[3])
        else:
            p[0] = _LilyPondDuration(p[1].duration, p[3])


    def p_multiplied_duration__steno_duration(self, p):
        'multiplied_duration : steno_duration'
        p[0] = p[1]


    ### music ###


    def p_music__composite_music(self, p):
        'music : composite_music %prec COMPOSITE'
        p[0] = p[1]


#    def p_music__lyric_element_music(self, p):
#        'music : lyric_element_music'
#        p[0] = p[1]


    def p_music__simple_music(self, p):
        'music : simple_music'
        p[0] = p[1]


    ### music_arg ###


    def p_music_arg__composite_music(self, p):
        'music_arg : composite_music %prec COMPOSITE'
        p[0] = p[1]


    def p_music_arg__simple_music(self, p):
        'music_arg : simple_music'
        p[0] = p[1]


    ### music_bare ###


    def p_music_bare__MUSIC_IDENTIFIER(self, p):
        'music_bare : MUSIC_IDENTIFIER'
        p[0] = p[1]


    def p_music_bare__grouped_music_list(self, p):
        'music_bare : grouped_music_list'
        p[0] = p[1]


#    def p_music_bare__mode_changed_music(self, p):
#        'music_bare : mode_changed_music'
#        p[0] = Node('music_bare', p[1:])


    ### music_function_call ###


    def p_music_function_call__MUSIC_FUNCTION__function_arglist(self, p):
        'music_function_call : MUSIC_FUNCTION function_arglist'
        p[0] = self.client._guile(p[1], p[2])


    ### music_function_chord_body ###


    def p_music_function_chord_body__MUSIC_FUNCTION__music_function_chord_body_arglist(self, p):
        'music_function_chord_body : MUSIC_FUNCTION music_function_chord_body_arglist'
        p[0] = Node('music_function_chord_body', p[1:])


    ### music_function_chord_body_arglist ###


    def p_music_function_chord_body_arglist__EXPECT_SCM__music_function_chord_body_arglist__embedded_scm_chord_body(self, p):
        'music_function_chord_body_arglist : EXPECT_SCM music_function_chord_body_arglist embedded_scm_chord_body'
        p[0] = p[2] + [p[3]]


    def p_music_function_chord_body_arglist__function_arglist_bare(self, p):
        'music_function_chord_body_arglist : function_arglist_bare'
        p[0] = p[1]


    ### music_function_event ###


    def p_music_function_event__MUSIC_FUNCTION__function_arglist_closed(self, p):
        'music_function_event : MUSIC_FUNCTION function_arglist_closed'
        p[0] = Node('music_function_event', p[1:])


    ### music_list ###


    def p_music_list__Empty(self, p):
        'music_list : '
        p[0] = [ ]


    def p_music_list__music_list__embedded_scm(self, p):
        'music_list : music_list embedded_scm'
        p[0] = p[1] + [p[2]]


    def p_music_list__music_list__error(self, p):
        'music_list : music_list error'
        p[0] = p[1] + [p[2]]


    def p_music_list__music_list__music(self, p):
        'music_list : music_list music'
        p[0] = p[1] + [p[2]]


    ### music_property_def ###


    def p_music_property_def__simple_music_property_def(self, p):
        'music_property_def : simple_music_property_def'
        p[0] = Node('music_property_def', p[1:])


    ### new_chord ###


#    def p_new_chord__steno_tonic_pitch__optional_notemode_duration(self, p):
#        'new_chord : steno_tonic_pitch optional_notemode_duration'
#        p[0] = Node('new_chord', p[1:])


#    def p_new_chord__steno_tonic_pitch__optional_notemode_duration__chord_separator__chord_items(self, p):
#        'new_chord : steno_tonic_pitch optional_notemode_duration chord_separator chord_items'
#        p[0] = Node('new_chord', p[1:])


    ### new_lyrics ###


#    def p_new_lyrics__ADDLYRICS__composite_music(self, p):
#        'new_lyrics : ADDLYRICS composite_music'
#        p[0] = Node('new_lyrics', p[1:])


#    def p_new_lyrics__new_lyrics__ADDLYRICS__composite_music(self, p):
#        'new_lyrics : new_lyrics ADDLYRICS composite_music'
#        p[0] = Node('new_lyrics', p[1:])


    ### note_chord_element ###


    def p_note_chord_element__chord_body__optional_notemode_duration__post_events(self, p):
        'note_chord_element : chord_body optional_notemode_duration post_events'
        pitches = [ ]
        post_events = [ ]
        for node in p[1]:
            if 5 == len(node):
                pitches.append(node[0])
                post_events.extend(node[4])
        post_events.extend(p[3])
        chord = Chord(pitches, p[2].duration)
        self.client._chord_pitch_orders[chord] = pitches
        if p[2].multiplier is not None:
            chord.duration_multiplier = p[2].multiplier
        self.client._process_post_events(chord, post_events)
        p[0] = chord


    ### number_expression ###


    def p_number_expression__number_expression__Chr43__number_term(self, p):
        "number_expression : number_expression '+' number_term"
        p[0] = float(p[1]) + p[3]


    def p_number_expression__number_expression__Chr45__number_term(self, p):
        "number_expression : number_expression '-' number_term"
        p[0] = float(p[1]) - p[3]


    def p_number_expression__number_term(self, p):
        'number_expression : number_term'
        p[0] = p[1]


    ### number_factor ###


    def p_number_factor__Chr45__number_factor(self, p):
        "number_factor : '-' number_factor"
        p[0] = -1 * p[2]


    def p_number_factor__bare_number(self, p):
        'number_factor : bare_number'
        p[0] = p[1]


    ### number_term ###


    def p_number_term__number_factor(self, p):
        'number_term : number_factor'
        p[0] = p[1]


    def p_number_term__number_factor__Chr42__number_factor(self, p):
        "number_term : number_factor '*' number_factor"
        p[0] = float(p[1]) * p[3]


    def p_number_term__number_factor__Chr47__number_factor(self, p):
        "number_term : number_factor '/' number_factor"
        p[0] = float(p[1]) / p[3]


    ### octave_check ###


    def p_octave_check__Empty(self, p):
        'octave_check : '
        p[0] = Node('octave_check', p[1:])


    def p_octave_check__Chr61(self, p):
        "octave_check : '='"
        p[0] = Node('octave_check', p[1:])


    def p_octave_check__Chr61__sub_quotes(self, p):
        "octave_check : '=' sub_quotes"
        p[0] = Node('octave_check', p[1:])


    def p_octave_check__Chr61__sup_quotes(self, p):
        "octave_check : '=' sup_quotes"
        p[0] = Node('octave_check', p[1:])


    ### optional_context_mod ###


    def p_optional_context_mod__Empty(self, p):
        'optional_context_mod : '
        p[0] = [ ]


    def p_optional_context_mod__context_modification(self, p):
        'optional_context_mod : context_modification'
        p[0] = p[1]


    ### optional_id ###


    def p_optional_id__Empty(self, p):
        'optional_id : '
        p[0] = None


    def p_optional_id__Chr61__simple_string(self, p):
        "optional_id : '=' simple_string"
        p[0] = p[2]


    ### optional_notemode_duration ###


    def p_optional_notemode_duration__Empty(self, p):
        'optional_notemode_duration : '
        p[0] = self.client._default_duration


    def p_optional_notemode_duration__multiplied_duration(self, p):
        'optional_notemode_duration : multiplied_duration'
        p[0] = p[1]
        self.client._default_duration = p[1]

    ### optional_rest ###


    def p_optional_rest__Empty(self, p):
        'optional_rest : '
        p[0] = False


    def p_optional_rest__REST(self, p):
        'optional_rest : REST'
        p[0] = True


    ### output_def ###


#    def p_output_def__output_def_body__Chr125(self, p):
#        "output_def : output_def_body '}'"
#        p[0] = Node('output_def', p[1:])


    ### output_def_body ###


#    def p_output_def_body__output_def_body__assignment(self, p):
#        'output_def_body : output_def_body assignment'
#        p[0] = Node('output_def_body', p[1:])


#    def p_output_def_body__output_def_body__context_def_spec_block(self, p):
#        'output_def_body : output_def_body context_def_spec_block'
#        p[0] = Node('output_def_body', p[1:])


#    def p_output_def_body__output_def_body__error(self, p):
#        'output_def_body : output_def_body error'
#        p[0] = Node('output_def_body', p[1:])


#    def p_output_def_body__output_def_head_with_mode_switch__Chr123(self, p):
#        "output_def_body : output_def_head_with_mode_switch '{'"
#        p[0] = Node('output_def_body', p[1:])


#    def p_output_def_body__output_def_head_with_mode_switch__Chr123__OUTPUT_DEF_IDENTIFIER(self, p):
#        "output_def_body : output_def_head_with_mode_switch '{' OUTPUT_DEF_IDENTIFIER"
#        p[0] = Node('output_def_body', p[1:])


    ### output_def_head ###


#    def p_output_def_head__LAYOUT(self, p):
#        'output_def_head : LAYOUT'
#        p[0] = Node('output_def_head', p[1:])


#    def p_output_def_head__MIDI(self, p):
#        'output_def_head : MIDI'
#        p[0] = Node('output_def_head', p[1:])


#    def p_output_def_head__PAPER(self, p):
#        'output_def_head : PAPER'
#        p[0] = Node('output_def_head', p[1:])


    ### output_def_head_with_mode_switch ###


#    def p_output_def_head_with_mode_switch__output_def_head(self, p):
#        'output_def_head_with_mode_switch : output_def_head'
#        p[0] = Node('output_def_head_with_mode_switch', p[1:])


    ### paper_block ###


#    def p_paper_block__output_def(self, p):
#        'paper_block : output_def'
#        p[0] = Node('paper_block', p[1:])


    ### pitch ###


    def p_pitch__PITCH_IDENTIFIER(self, p):
        'pitch : PITCH_IDENTIFIER'
        p[0] = p[1]


    def p_pitch__steno_pitch(self, p):
        'pitch : steno_pitch'
        p[0] = p[1]


    ### pitch_also_in_chords ###


    def p_pitch_also_in_chords__pitch(self, p):
        'pitch_also_in_chords : pitch'
        p[0] = p[1]


    def p_pitch_also_in_chords__steno_tonic_pitch(self, p):
        'pitch_also_in_chords : steno_tonic_pitch'
        p[0] = p[1]


    ### post_event ###


    def p_post_event__Chr45__fingering(self, p):
        "post_event : '-' fingering"
        p[0] = None


    def p_post_event__post_event_nofinger(self, p):
        'post_event : post_event_nofinger'
        p[0] = p[1]


    ### post_event_nofinger ###


    def p_post_event_nofinger__Chr94__fingering(self, p):
        "post_event_nofinger : '^' fingering"
        p[0] = None


    def p_post_event_nofinger__Chr95__fingering(self, p):
        "post_event_nofinger : '_' fingering"
        p[0] = None


    def p_post_event_nofinger__EXTENDER(self, p):
        'post_event_nofinger : EXTENDER'
        p[0] = None


    def p_post_event_nofinger__HYPHEN(self, p):
        'post_event_nofinger : HYPHEN'
        p[0] = None


    def p_post_event_nofinger__direction_less_event(self, p):
        'post_event_nofinger : direction_less_event'
        p[0] = p[1]


    def p_post_event_nofinger__script_dir__direction_less_event(self, p):
        'post_event_nofinger : script_dir direction_less_event'
        p[2].direction = p[1]
        p[0] = p[2]


    def p_post_event_nofinger__script_dir__direction_reqd_event(self, p):
        'post_event_nofinger : script_dir direction_reqd_event'
        # TODO: Give marks, markup and spanners the same direction_string functionality. #
        p[2].direction = p[1]
        p[0] = p[2]


    def p_post_event_nofinger__script_dir__music_function_event(self, p):
        'post_event_nofinger : script_dir music_function_event'
        p[0] = p[2]


    def p_post_event_nofinger__string_number_event(self, p):
        'post_event_nofinger : string_number_event'
        p[0] = None


    ### post_events ###


    def p_post_events__Empty(self, p):
        'post_events : '
        p[0] = [ ]


    def p_post_events__post_events__post_event(self, p):
        'post_events : post_events post_event'
        p[0] = p[1] + [p[2]]


    ### property_operation ###


    def p_property_operation__OVERRIDE__simple_string__property_path__Chr61__scalar(self, p):
        "property_operation : OVERRIDE simple_string property_path '=' scalar"
        p[0] = Event('PropertyOperation',
            keyword='override', 
            context=p[2], 
            property=p[3],
            value=p[5])


    def p_property_operation__REVERT__simple_string__embedded_scm(self, p):
        'property_operation : REVERT simple_string embedded_scm'
        p[0] = Event('PropertyOperation',
            keyword='revert', 
            context=p[2], 
            property=p[3])


    def p_property_operation__STRING__Chr61__scalar(self, p):
        "property_operation : STRING '=' scalar"
        p[0] = Event('PropertyOperation',
            keyword='set',
            property=p[1],
            value=p[2])


    def p_property_operation__UNSET__simple_string(self, p):
        'property_operation : UNSET simple_string'
        p[0] = Event('PropertyOperation',
            keyword='unset',
            property=p[2])


    ### property_path ###


    def p_property_path__property_path_revved(self, p):
        'property_path : property_path_revved'
        p[0] = p[1]


    ### property_path_revved ###


    def p_property_path_revved__embedded_scm_closed(self, p):
        'property_path_revved : embedded_scm_closed'
        p[0] = [p[1]]


    def p_property_path_revved__property_path_revved__embedded_scm_closed(self, p):
        'property_path_revved : property_path_revved embedded_scm_closed'
        p[0] = p[1] + [p[2]]


    ### questions ###


    def p_questions__Empty(self, p):
        'questions : '
        p[0] = ''


    def p_questions__questions__Chr63(self, p):
        "questions : questions '?'"
        p[0] = p[1] + '?'


    ### re_rhythmed_music ###


#    def p_re_rhythmed_music__LYRICSTO__simple_string__music(self, p):
#        're_rhythmed_music : LYRICSTO simple_string music'
#        p[0] = Node('re_rhythmed_music', p[1:])


#    def p_re_rhythmed_music__composite_music__new_lyrics(self, p):
#        're_rhythmed_music : composite_music new_lyrics %prec COMPOSITE'
#        p[0] = Node('re_rhythmed_music', p[1:])


    ### repeated_music ###


#    def p_repeated_music__REPEAT__simple_string__unsigned_number__music(self, p):
#        'repeated_music : REPEAT simple_string unsigned_number music'
#        p[0] = Node('repeated_music', p[1:])


#    def p_repeated_music__REPEAT__simple_string__unsigned_number__music__ALTERNATIVE__braced_music_list(self, p):
#        'repeated_music : REPEAT simple_string unsigned_number music ALTERNATIVE braced_music_list'
#        p[0] = Node('repeated_music', p[1:])


    ### scalar ###


    def p_scalar__bare_number(self, p):
        'scalar : bare_number'
        p[0] = p[1]


    def p_scalar__embedded_scm_arg(self, p):
        'scalar : embedded_scm_arg'
        p[0] = p[1]


#    def p_scalar__lyric_element(self, p):
#        'scalar : lyric_element'
#        p[0] = p[1]


    ### scalar_closed ###


    def p_scalar_closed__bare_number(self, p):
        'scalar_closed : bare_number'
        p[0] = p[1]


    def p_scalar_closed__embedded_scm_arg_closed(self, p):
        'scalar_closed : embedded_scm_arg_closed'
        p[0] = p[1]


#    def p_scalar_closed__lyric_element(self, p):
#        'scalar_closed : lyric_element'
#        p[0] = p[1]


    ### scm_function_call ###


    def p_scm_function_call__SCM_FUNCTION__function_arglist(self, p):
        'scm_function_call : SCM_FUNCTION function_arglist'
        p[0] = self.client._guile(p[1], p[2])


    ### scm_function_call_closed ###


    def p_scm_function_call_closed__SCM_FUNCTION__function_arglist_closed(self, p):
        'scm_function_call_closed : SCM_FUNCTION function_arglist_closed %prec FUNCTION_ARGLIST'
        p[0] = self.client._guile(p[1], p[2])


    ### score_block ###


    def p_score_block__SCORE__Chr123__score_body__Chr125(self, p):
        "score_block : SCORE '{' score_body '}'"
        score_block = lilypondfiletools.ScoreBlock()
        score_block.append(p[3])
        p[0] = score_block


    ### score_body ###


    def p_score_body__SCORE_IDENTIFIER(self, p):
        'score_body : SCORE_IDENTIFIER'
        p[0] = p[1]


    def p_score_body__music(self, p):
        'score_body : music'
        p[0] = p[1]


#    def p_score_body__score_body__error(self, p):
#        'score_body : score_body error'
#        p[0] = Node('score_body', p[1:])


#    def p_score_body__score_body__lilypond_header(self, p):
#        'score_body : score_body lilypond_header'
#        p[0] = Node('score_body', p[1:])


#    def p_score_body__score_body__output_def(self, p):
#        'score_body : score_body output_def'
#        p[0] = Node('score_body', p[1:])


    ### script_abbreviation ###


    def p_script_abbreviation__ANGLE_CLOSE(self, p):
        'script_abbreviation : ANGLE_CLOSE'
        kind = self.client._current_module['dashLarger']['alias']
        p[0] = marktools.Articulation(kind)


    def p_script_abbreviation__Chr124(self, p):
        "script_abbreviation : '|'"
        kind = self.client._current_module['dashBar']['alias']
        p[0] = marktools.Articulation(kind)


    def p_script_abbreviation__Chr43(self, p):
        "script_abbreviation : '+'"
        kind = self.client._current_module['dashPlus']['alias']
        p[0] = marktools.Articulation(kind)


    def p_script_abbreviation__Chr45(self, p):
        "script_abbreviation : '-'"
        kind = self.client._current_module['dashDash']['alias']
        p[0] = marktools.Articulation(kind)


    def p_script_abbreviation__Chr46(self, p):
        "script_abbreviation : '.'"
        kind = self.client._current_module['dashDot']['alias']
        p[0] = marktools.Articulation(kind)


    def p_script_abbreviation__Chr94(self, p):
        "script_abbreviation : '^'"
        kind = self.client._current_module['dashHat']['alias']
        p[0] = marktools.Articulation(kind)


    def p_script_abbreviation__Chr95(self, p):
        "script_abbreviation : '_'"
        kind = self.client._current_module['dashUnderscore']['alias']
        p[0] = marktools.Articulation(kind)


    ### script_dir ###


    def p_script_dir__Chr45(self, p):
        "script_dir : '-'"
        p[0] = p[1]


    def p_script_dir__Chr94(self, p):
        "script_dir : '^'"
        p[0] = p[1]


    def p_script_dir__Chr95(self, p):
        "script_dir : '_'"
        p[0] = p[1]


    ### sequential_music ###


    def p_sequential_music__SEQUENTIAL__braced_music_list(self, p):
        'sequential_music : SEQUENTIAL braced_music_list'
        p[0] = self.client._construct_sequential_music(p[2])


    def p_sequential_music__braced_music_list(self, p):
        'sequential_music : braced_music_list'
        p[0] = self.client._construct_sequential_music(p[1])
            

    ### simple_chord_elements ###


#    def p_simple_chord_elements__figure_spec__optional_notemode_duration(self, p):
#        'simple_chord_elements : figure_spec optional_notemode_duration'
#        p[0] = Node('simple_chord_elements', p[1:])


#    def p_simple_chord_elements__new_chord(self, p):
#        'simple_chord_elements : new_chord'
#        p[0] = Node('simple_chord_elements', p[1:])


    def p_simple_chord_elements__simple_element(self, p):
        'simple_chord_elements : simple_element'
        p[0] = p[1]


    ### simple_element ###


#    def p_simple_element__DRUM_PITCH__optional_notemode_duration(self, p):
#        'simple_element : DRUM_PITCH optional_notemode_duration'
#        raise Exception('Drum pitches not supported.')


    def p_simple_element__RESTNAME__optional_notemode_duration(self, p):
        'simple_element : RESTNAME optional_notemode_duration'
        if p[1] == 'r':
            rest = Rest(p[2].duration)
        else:
            rest = skiptools.Skip(p[2].duration)
        if p[2].multiplier is not None:
            rest.duration_multiplier = p[2].multiplier
        p[0] = rest


    def p_simple_element__pitch__exclamations__questions__octave_check__optional_notemode_duration__optional_rest(self, p):
        'simple_element : pitch exclamations questions octave_check optional_notemode_duration optional_rest'
        if not p[6]:
            leaf = Note(p[1], p[5].duration)
        else:
            leaf = Rest(p[5][0])
            resttools.set_vertical_positioning_pitch_on_rest(leaf, p[1])
        if p[5].multiplier is not None:
            leaf.duration_multiplier = p[5].multiplier
        # TODO: handle exclamations, questions, octave_check
        p[0] = leaf


    ### simple_markup ###


#    def p_simple_markup__LYRIC_MARKUP_IDENTIFIER(self, p):
#        'simple_markup : LYRIC_MARKUP_IDENTIFIER'
#        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup__MARKUP_FUNCTION__markup_command_basic_arguments(self, p):
        'simple_markup : MARKUP_FUNCTION markup_command_basic_arguments'
        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup__MARKUP_IDENTIFIER(self, p):
        'simple_markup : MARKUP_IDENTIFIER'
        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup__SCORE__Chr123__score_body__Chr125(self, p):
        "simple_markup : SCORE '{' score_body '}'"
        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup__STRING(self, p):
        'simple_markup : STRING'
        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup__STRING_IDENTIFIER(self, p):
        'simple_markup : STRING_IDENTIFIER'
        p[0] = Node('simple_markup', p[1:])


    def p_simple_markup__markup_scm__MARKUP_IDENTIFIER(self, p):
        'simple_markup : markup_scm MARKUP_IDENTIFIER'
        p[0] = Node('simple_markup', p[1:])


    ### simple_music ###


    def p_simple_music__context_change(self, p):
        'simple_music : context_change'
        p[0] = p[1]


    def p_simple_music__event_chord(self, p):
        'simple_music : event_chord'
        p[0] = p[1]


    def p_simple_music__music_property_def(self, p):
        'simple_music : music_property_def'
        p[0] = p[1]


    ### simple_music_property_def ###


    def p_simple_music_property_def__OVERRIDE__context_prop_spec__property_path__Chr61__scalar(self, p):
        "simple_music_property_def : OVERRIDE context_prop_spec property_path '=' scalar"
        p[0] = Node('simple_music_property_def', p[1:])


    def p_simple_music_property_def__REVERT__context_prop_spec__embedded_scm(self, p):
        'simple_music_property_def : REVERT context_prop_spec embedded_scm'
        p[0] = Node('simple_music_property_def', p[1:])


    def p_simple_music_property_def__SET__context_prop_spec__Chr61__scalar(self, p):
        "simple_music_property_def : SET context_prop_spec '=' scalar"
        p[0] = Node('simple_music_property_def', p[1:])


    def p_simple_music_property_def__UNSET__context_prop_spec(self, p):
        'simple_music_property_def : UNSET context_prop_spec'
        p[0] = Node('simple_music_property_def', p[1:])


    ### simple_string ###


#    def p_simple_string__LYRICS_STRING(self, p):
#        'simple_string : LYRICS_STRING'
#        p[0] = p[1]


    def p_simple_string__STRING(self, p):
        'simple_string : STRING'
        p[0] = p[1]


    def p_simple_string__STRING_IDENTIFIER(self, p):
        'simple_string : STRING_IDENTIFIER'
        p[0] = p[1]


    ### simultaneous_music ###


    def p_simultaneous_music__DOUBLE_ANGLE_OPEN__music_list__DOUBLE_ANGLE_CLOSE(self, p):
        'simultaneous_music : DOUBLE_ANGLE_OPEN music_list DOUBLE_ANGLE_CLOSE'
        p[0] = self.client._construct_simultaneous_music(p[2])


    def p_simultaneous_music__SIMULTANEOUS__braced_music_list(self, p):
        'simultaneous_music : SIMULTANEOUS braced_music_list'
        p[0] = self.client._construct_simultaneous_music(p[2])


    ### steno_duration ###


    def p_steno_duration__DURATION_IDENTIFIER__dots(self, p):
        'steno_duration : DURATION_IDENTIFIER dots'
        dots = p[2].value
        duration = p[1].duration
        multiplier = p[1].multiplier
        if dots:
            token = durationtools.assignable_rational_to_lilypond_duration_string(duration)
            token += '.' * dots
            duration = Duration(durationtools.duration_token_to_rational(token))
        p[0] = _LilyPondDuration(duration, multiplier)


    def p_steno_duration__bare_unsigned__dots(self, p):
        'steno_duration : bare_unsigned dots'
        assert durationtools.is_duration_token(p[1])
        dots = p[2].value
        token = str(p[1]) + '.' * dots
        duration = Duration(durationtools.duration_token_to_rational(token))
        p[0] = _LilyPondDuration(duration, None)


    ### steno_pitch ###


    def p_steno_pitch__NOTENAME_PITCH(self, p):
        'steno_pitch : NOTENAME_PITCH'
        p[0] = pitchtools.NamedChromaticPitch(str(p[1]))


    def p_steno_pitch__NOTENAME_PITCH__sub_quotes(self, p):
        'steno_pitch : NOTENAME_PITCH sub_quotes'
        p[0] = pitchtools.NamedChromaticPitch(str(p[1]) + ',' * p[2])


    def p_steno_pitch__NOTENAME_PITCH__sup_quotes(self, p):
        'steno_pitch : NOTENAME_PITCH sup_quotes'
        p[0] = pitchtools.NamedChromaticPitch(str(p[1]) + '\'' * p[2])


    ### steno_tonic_pitch ###


    def p_steno_tonic_pitch__TONICNAME_PITCH(self, p):
        'steno_tonic_pitch : TONICNAME_PITCH'
        p[0] = Node('steno_tonic_pitch', p[1:])


    def p_steno_tonic_pitch__TONICNAME_PITCH__sub_quotes(self, p):
        'steno_tonic_pitch : TONICNAME_PITCH sub_quotes'
        p[0] = Node('steno_tonic_pitch', p[1:])


    def p_steno_tonic_pitch__TONICNAME_PITCH__sup_quotes(self, p):
        'steno_tonic_pitch : TONICNAME_PITCH sup_quotes'
        p[0] = Node('steno_tonic_pitch', p[1:])


    ### step_number ###


#    def p_step_number__bare_unsigned(self, p):
#        'step_number : bare_unsigned'
#        p[0] = Node('step_number', p[1:])


#    def p_step_number__bare_unsigned__CHORD_MINUS(self, p):
#        'step_number : bare_unsigned CHORD_MINUS'
#        p[0] = Node('step_number', p[1:])


#    def p_step_number__bare_unsigned__Chr43(self, p):
#        "step_number : bare_unsigned '+'"
#        p[0] = Node('step_number', p[1:])


    ### step_numbers ###


#    def p_step_numbers__step_number(self, p):
#        'step_numbers : step_number'
#        p[0] = Node('step_numbers', p[1:])


#    def p_step_numbers__step_numbers__Chr46__step_number(self, p):
#        "step_numbers : step_numbers '.' step_number"
#        p[0] = Node('step_numbers', p[1:])


    ### string ###


    def p_string__STRING(self, p):
        'string : STRING'
        p[0] = Node('string', p[1:])


    def p_string__STRING_IDENTIFIER(self, p):
        'string : STRING_IDENTIFIER'
        p[0] = Node('string', p[1:])


    def p_string__string__Chr43__string(self, p):
        "string : string '+' string"
        p[0] = Node('string', p[1:])


    ### string_number_event ###


    def p_string_number_event__E_UNSIGNED(self, p):
        'string_number_event : E_UNSIGNED'
        p[0] = Node('string_number_event', p[1:])


    ### sub_quotes ###


    def p_sub_quotes__Chr44(self, p):
        "sub_quotes : ','"
        p[0] = 1


    def p_sub_quotes__sub_quotes__Chr44(self, p):
        "sub_quotes : sub_quotes ','"
        p[0] = p[1] + 1


    ### sup_quotes ###


    def p_sup_quotes__Chr39(self, p):
        "sup_quotes : '\\''"
        p[0] = 1


    def p_sup_quotes__sup_quotes__Chr39(self, p):
        "sup_quotes : sup_quotes '\\''"
        p[0] = p[1] + 1


    ### tempo_event ###


    def p_tempo_event__TEMPO__scalar(self, p):
        'tempo_event : TEMPO scalar'
        p[0] = contexttools.TempoMark(str(p[2]))


    def p_tempo_event__TEMPO__scalar_closed__steno_duration__Chr61__tempo_range(self, p):
        "tempo_event : TEMPO scalar_closed steno_duration '=' tempo_range"
        p[0] = contexttools.TempoMark(str(p[2]), p[3].duration, p[5])


    def p_tempo_event__TEMPO__steno_duration__Chr61__tempo_range(self, p):
        "tempo_event : TEMPO steno_duration '=' tempo_range"
        p[0] = contexttools.TempoMark(p[2].duration, p[4])


    ### tempo_range ###


    def p_tempo_range__bare_unsigned(self, p):
        'tempo_range : bare_unsigned'
        p[0] = p[1]


    def p_tempo_range__bare_unsigned__Chr126__bare_unsigned(self, p):
        "tempo_range : bare_unsigned '~' bare_unsigned"
        p[0] = (p[1], p[3])


    ### toplevel_expression ###


#    def p_toplevel_expression__book_block(self, p):
#        'toplevel_expression : book_block'
#        p[0] = p[1]


#    def p_toplevel_expression__bookpart_block(self, p):
#        'toplevel_expression : bookpart_block'
#        p[0] = p[1]


    def p_toplevel_expression__composite_music(self, p):
        'toplevel_expression : composite_music'
        p[0] = p[1]


    def p_toplevel_expression__full_markup(self, p):
        'toplevel_expression : full_markup'
        p[0] = p[1]


    def p_toplevel_expression__full_markup_list(self, p):
        'toplevel_expression : full_markup_list'
        p[0] = p[1]


#    def p_toplevel_expression__lilypond_header(self, p):
#        'toplevel_expression : lilypond_header'
#        p[0] = p[1]


#    def p_toplevel_expression__output_def(self, p):
#        'toplevel_expression : output_def'
#        p[0] = p[1]


    def p_toplevel_expression__score_block(self, p):
        'toplevel_expression : score_block'
        p[0] = p[1]


    ### tremolo_type ###


    def p_tremolo_type__Chr58(self, p):
        "tremolo_type : ':'"
        p[0] = None


    def p_tremolo_type__Chr58__bare_unsigned(self, p):
        "tremolo_type : ':' bare_unsigned"
        p[0] = marktools.StemTremolo(p[2])


    ### unsigned_number ###


#    def p_unsigned_number__NUMBER_IDENTIFIER(self, p):
#        'unsigned_number : NUMBER_IDENTIFIER'
#        p[0] = p[1]


#    def p_unsigned_number__UNSIGNED(self, p):
#        'unsigned_number : UNSIGNED'
#        p[0] = p[1]


    ### PLY error ###


    def p_error(self, p):
        raise LilyPondParserError
        #print "Syntax error at %s" % p

