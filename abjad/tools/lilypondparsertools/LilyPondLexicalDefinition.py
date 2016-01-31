# -*- coding: utf-8 -*-
import copy
from ply import lex
from abjad.tools import scoretools
from abjad.tools.abctools import AbjadObject
from abjad.tools.exceptiontools import LilyPondParserError
from abjad.tools.exceptiontools import SchemeParserFinishedError


class LilyPondLexicalDefinition(AbjadObject):
    r'''The lexical definition of LilyPond's syntax.

    Effectively equivalent to LilyPond's ``lexer.ll`` file.

    Not composer-safe.

    Used internally by ``LilyPondParser``.
    '''

    ### CHARACTERS ###

    characters = {
        '>': 'E_ANGLE_CLOSE',
        '<': 'E_ANGLE_OPEN',
        '!': 'E_EXCLAMATION',
        '(': 'E_OPEN',
        ')': 'E_CLOSE',
        '[': 'E_BRACKET_OPEN',
        '+': 'E_PLUS',
        ']': 'E_BRACKET_CLOSE',
        '~': 'E_TILDE',
        '\\': 'E_BACKSLASH',
        }

    ### IDENTIFIERS ###

    identifiers = {
        'book_block': 'BOOK_IDENTIFIER',
        'bookpart_block': 'BOOK_IDENTIFIER',
        'context_def_spec_block': 'CONTEXT_DEF_IDENTIFIER',
        'context_modification': 'CONTEXT_MOD_IDENTIFIER',
        'post_event_nofinger': 'EVENT_IDENTIFIER',
        'full_markup': 'MARKUP_IDENTIFIER',
        'full_markup_list': 'MARKUPLINES_IDENTIFIER',
        'music': 'MUSIC_IDENTIFIER',
        'number_expression': 'NUMBER_IDENTIFIER',
        'output_def': 'OUTPUT_DEF_IDENTIFIER',
        'embedded_scm': 'SCM_IDENTIFIER',
        'score_block': 'SCORE_IDENTIFIER',
        'string': 'STRING_IDENTIFIER',
        # 'PITCH_IDENTIFIER' ?
        # 'DURATION_IDENTIFIER' ?
        # 'LYRIC_MARKUP_IDENTIFIER' ?
        }

    ### PREDICATES ###

    predicates = {
        'ly:music?': 'EXPECT_SCM',
        'ly:pitch?': 'EXPECT_PITCH',
        'ly:duration?': 'EXPECT_DURATION',
        'markup?': 'EXPECT_MARKUP',
        'cheap-markup?': 'EXPECT_MARKUP',
        'markup-list?': 'EXPECT_MARKUP_LIST',
        }

    function_predicates = {
        'ly:music?': 'MUSIC_FUNCTION',
        'ly:event?': 'EVENT_FUNCTION',
        }

    ### STATES ###

    # SOURCE: lexer.ll +126
    states = (
        # ('chords', 'exclusive'),
        # ('figures', 'exclusive'),
        # ('incl', 'exclusive'),
        # ('lyrics', 'exclusive'),
        ('longcomment', 'exclusive'),
        # ('maininput', 'exclusive'),
        ('markup', 'exclusive'),
        ('notes', 'exclusive'),
        ('quote', 'exclusive'),
        ('commandquote', 'exclusive'),
        # ('sourcefileline', 'exclusive'),
        # ('sourcefilename', 'exclusive'),
        ('version', 'exclusive'),
        )

    states += (
        ('scheme', 'exclusive'),  # For Abjad.
        )

    ### PATTERNS ###

    # SOURCE: lexer.ll +156
    A = r'[a-zA-Z\200-\377]'
    AA = r'({A}|_)'.format(A=A)
    N = r'[0-9]'
    ANY_CHAR = r'(.|\n)'
    WORD = r'{A}([-_]{A}|{A})*'.format(A=A)
    COMMAND = r'\\{WORD}'.format(WORD=WORD)

    # SOURCE: lexer.ll +164
    SPECIAL = r'[-+*/=<>{}!?_^'',.:]'
    SHORTHAND = r'(.|\\.)'
    UNSIGNED = r'{N}+'.format(N=N)
    E_UNSIGNED = r'\\{N}+'.format(N=N)
    FRACTION = r'{N}+\/{N}+'.format(N=N)
    INT = r'-?{UNSIGNED}'.format(UNSIGNED=UNSIGNED)
    REAL = r'({INT}\.{N}*)|(-?\.{N}+)'.format(INT=INT, N=N)
    STRICTREAL = r'{UNSIGNED}\.{UNSIGNED}'.format(UNSIGNED=UNSIGNED)
    WHITE = r'[ \n\t\f\r]'
    HORIZONTALWHITE = r'[ \t]'
    BLACK = r'[^ \n\t\f\r]'
    RESTNAME = r'[rs]'
    ESCAPED = r'''[nt\\''""]'''
    EXTENDER = r'__'
    HYPHEN = r'--'
    BOM_UTF8 = r'\357\273\277'

    ### TOKENS ###

    # SOURCE: parser.yy +250
    keywords = {
        #r'\accepts': 'ACCEPTS',
        #r'\addlyrics': 'ADDLYRICS',
        #r'\alias': 'ALIAS',
        #r'\alternative': 'ALTERNATIVE',
        #r'\book': 'BOOK',
        #r'\bookpart': 'BOOKPART',
        r'\change': 'CHANGE',
        #r'\chordmode': 'CHORDMODE',
        #r'\chords': 'CHORDS',
        #r'\consists': 'CONSISTS',
        r'\context': 'CONTEXT',
        r'\default': 'DEFAULT',
        #r'\defaultchild': 'DEFAULTCHILD',
        #r'\denies': 'DENIES',
        #r'\description': 'DESCRIPTION',
        #r'\drummode': 'DRUMMODE',
        #r'\drums': 'DRUMS',
        #r'\etc': 'ETC',
        #r'\figuremode': 'FIGUREMODE',
        #r'\figures': 'FIGURES',
        r'\header': 'HEADER',
        #r'\version-error': 'INVALID',
        r'\layout': 'LAYOUT',
        #r'\lyricmode': 'LYRICMODE',
        #r'\lyrics': 'LYRICS',
        #r'\lyricsto': 'LYRICSTO',
        r'\markup': 'MARKUP',
        r'\markuplist': 'MARKUPLIST',
        r'\midi': 'MIDI',
        #r'\name': 'NAME',
        r'\new': 'NEWCONTEXT',
        #r'\notemode': 'NOTEMODE',
        r'\override': 'OVERRIDE',
        r'\paper': 'PAPER',
        #r'\remove': 'REMOVE',
        #r'\repeat': 'REPEAT',
        r'\rest': 'REST',
        r'\revert': 'REVERT',
        r'\score': 'SCORE',
        #r'\score-lines': 'SCORELINES',
        r'\sequential': 'SEQUENTIAL',
        r'\set': 'SET',
        r'\simultaneous': 'SIMULTANEOUS',
        r'\tempo': 'TEMPO',
        #r'\type': 'TYPE',
        r'\unset': 'UNSET',
        r'\with': 'WITH',
        }

    single_characters = {
        #r'/+': 'CHORD_BASS',
        #r'^': 'CHORD_CARET',
        #r':': 'CHORD_COLON',
        #r'-': 'CHORD_MINUS',
        #r'/': 'CHORD_SLASH',
        r'<': 'ANGLE_OPEN',
        r'>': 'ANGLE_CLOSE',
        #r'_': 'FIGURE_SPACE',
        }

    double_characters = {
        r'<<': 'DOUBLE_ANGLE_OPEN',
        r'>>': 'DOUBLE_ANGLE_CLOSE',
        r'\!': 'E_EXCLAMATION',
        r'\\': 'E_BACKSLASH',
        #r'\+': 'E_PLUS',
        #r'\>': 'FIGURE_CLOSE',
        #r'\<': 'FIGURE_OPEN',
        r'--': 'HYPHEN',
        #r'#{': 'EMBEDDED_LILY',
        }

    with_predicates = {
        'EXPECT_MARKUP': 'markup?',
        'EXPECT_SCM': 'scheme?',
        'BACKUP': '(backed-up?)',
        'REPARSE': '(reparsed?)',
        'EXPECT_MARKUP_LIST': 'markup-list?',
        'EXPECT_OPTIONAL': 'optional?',
        }

    tokens = (
        #'BOOK_IDENTIFIER',
        #'CHORD_MODIFIER',
        'CHORD_REPETITION',
        'CONTEXT_MOD_IDENTIFIER',
        #'DRUM_PITCH',
        'DURATION_IDENTIFIER',
        'EVENT_FUNCTION',
        'EVENT_IDENTIFIER',
        'EXPECT_NO_MORE_ARGS',
        'E_UNSIGNED',
        'FRACTION',
        #'LYRIC_ELEMENT',
        'MARKUPLIST_IDENTIFIER',
        'MARKUP_FUNCTION',
        'MARKUP_IDENTIFIER',
        'MARKUP_LIST_FUNCTION',
        'MULTI_MEASURE_REST',
        'MUSIC_FUNCTION',
        'MUSIC_IDENTIFIER',
        'NOTENAME_PITCH',
        'NUMBER_IDENTIFIER',
        'PITCH_IDENTIFIER',
        'REAL',
        'RESTNAME',
        #'SCM_ARG',
        'SCM_FUNCTION',
        'SCM_IDENTIFIER',
        'SCM_TOKEN',
        'STRING',
        #'SYMBOL_LIST',
        'TONICNAME_PITCH',
        'UNSIGNED',
        )
    tokens += tuple(keywords.values())
    tokens += tuple(single_characters.values())
    tokens += tuple(double_characters.values())
    tokens += tuple(with_predicates)

    # These do not exist in 2.19.24, or have been renamed.
    in_deprecation = (
        'CONTEXT_DEF_IDENTIFIER',
        'EXPECT_DURATION',
        'EXPECT_PITCH',
        'EXTENDER',
        'E_ANGLE_CLOSE',
        'E_ANGLE_OPEN',
        'E_CLOSE',
        'E_OPEN',
        'SCORE_IDENTIFIER',
        'STRING_IDENTIFIER',
        'OUTPUT_DEF_IDENTIFIER',
        )

    tokens += in_deprecation

    ### LITERALS ###

    literals = (
        '!',
        "'",
        '(',
        ')',
        '*',
        '+',
        ',',
        '-',
        '.',
        '/',
        ':',
        '<',
        '=',
        '>',
        '?',
        '[',
        '\\',
        '^',
        '_',
        '{',
        '|',
        '}',
        '~',
        ']',
        )

    ### CLASS VARIABLES ###

    string_accumulator = ''

    ### INITIALIZER ###

    def __init__(self, client=None):
        self.client = client

    ### LEXICAL RULES ###

    # VERIFIED
    # SOURCE: lexer.ll +184
    # <*>\r
    def t_ANY_184(self, token):
        r'\r'
        pass

    # VERIFIED
    # SOURCE: lexer.ll +190
    # <INITIAL,chords,lyrics,figures,notes>{BOM_UTF8}/.*

    # VERIFIED
    # SOURCE: lexer.ll +200
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>"%{"
    def t_INITIAL_markup_notes_200(self, token):
        r'%{'
        token.lexer.push_state('longcomment')

    # VERIFIED
    # SOURCE: lexer.ll +203
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*[\n\r]?
    def t_INITIAL_markup_notes_203(self, token):
        r'%[^{\n\r][^\n\r]*[\n\r]?'
        pass

    # VERIFIED
    # SOURCE: lexer.ll:206
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[\n\r]?
    def t_INITIAL_markup_notes_206(self, token):
        r'%[\n\r]?'
        pass

    # VERIFIED
    # SOURCE: lexer.ll +208
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>{WHITE}+
    @lex.TOKEN('{WHITE}+'.format(WHITE=WHITE))
    def t_INITIAL_markup_notes_208(self, token):
        pass

    # VERIFIED
    # SOURCE: lexer.ll +213
    # <INITIAL,notes,figures,chords,markup>\"
    def t_INITIAL_markup_notes_213(self, token):
        r'\"'
        token.lexer.push_state('quote')
        #print("ENTERED QUOTE", token)
        self.string_accumulator = ''

    # VERIFIED
    # SOURCE: lexer.ll +219
    # <INITIAL,chords,lyrics,notes,figures>\\version{WHITE}*
    @lex.TOKEN(r'\\version{WHITE}*'.format(WHITE=WHITE))
    def t_INITIAL_notes_219(self, token):
        token.lexer.push_state('version')

    # VERIFIED
    # SOURCE: lexer.ll +222
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefilename{WHITE}*

    # VERIFIED
    # SOURCE: lexer.ll +225
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefileline{WHITE}*	{

    # VERIFIED
    # SOURCE: lexer.ll +228
    # <version>\"[^""]*\"
    def t_version_228(self, token):
        r'\"[^""]*\"'
        # We don't care whether the version is correct.
        token.lexer.pop_state()

    # VERIFIED
    # SOURCE: lexer.ll +242
    # <sourcefilename>\"[^""]*\"

    # VERIFIED
    # SOURCE: lexer.ll +256
    # <sourcefileline>{INT}

    # VERIFIED
    # SOURCE: lexer.ll +264
    # <version>{ANY_CHAR}
    @lex.TOKEN(ANY_CHAR)
    def t_version_264(self, token):
        message = 'LilyPondParser: Illegal character {!r}'
        message = message.format(token.value[0])
        raise LilyPondParserError(message)
        token.lexer.pop_state()

    # VERIFIED
    # SOURCE: lexer.ll +268
    # <sourcefilename>{ANY_CHAR}

    # VERIFIED
    # SOURCE: lexer.ll +272
    # <sourcefileline>{ANY_CHAR}

    # VERIFIED
    # SOURCE: lexer.ll +277
    # <longcomment>[^\%]*
    def t_longcomment_277(self, token):
        r'[^%]+'
        # This pattern has been adjusted.
        # The original matches the empty string.
        pass

    # VERIFIED
    # SOURCE: lexer.ll +280
    # <longcomment>%*[^}%]*
    def t_longcomment_280(self, token):
        r'%*[^}%]+'
        # This pattern has been adjusted.
        # The original matches the empty string.
        pass

    # VERIFIED
    # SOURCE: lexer.ll +283
    # <longcomment>"%"+"}"
    def t_longcomment_283(self, token):
        r'%}'
        token.lexer.pop_state()

    # VERIFIED
    # SOURCE: lexer.ll +289
    # <INITIAL,chords,lyrics,notes,figures>\\maininput

    # VERIFIED
    # SOURCE: lexer.ll +303
    # <INITIAL,chords,lyrics,figures,notes>\\include

    # VERIFIED
    # SOURCE: lexer.ll +306
    # <incl>\"[^""]*\"   { /* got the include file name */

    # VERIFIED
    # SOURCE: lexer.ll +313
    # <incl>\\{BLACK}*{WHITE}? { /* got the include identifier */

    # VERIFIED
    # SOURCE: lexer.ll +332
    # <incl>(\$|#) { // scm for the filename

    # VERIFIED
    # SOURCE: lexer.ll +358
    # <incl,version,sourcefilename>\"[^"]*
    def t_version_358(self, token):
        r'"[^"]*'
        message = 'end quote missing: {!r}.'
        message = message.format(token)
        raise LilyPondParserError(message)
        token.lexer.pop_state()

    # VERIFIED
    # SOURCE: lexer.ll +369
    # <chords,notes,figures>{RESTNAME}/[-_]|{RESTNAME}
    #@lex.TOKEN('{RESTNAME}(?=[-_])|{RESTNAME}'.format(RESTNAME=RESTNAME))
    @lex.TOKEN(RESTNAME)
    def t_notes_369(self, token):
        token.type = 'RESTNAME'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +375
    # <chords,notes,figures>q/[-_]|q
    #@lex.TOKEN(r'q(?=[-_])|q')
    @lex.TOKEN('q')
    def t_notes_375(self, token):
        token.type = 'CHORD_REPETITION'
        if self.client._last_chord is None:
            self.client._last_chord = scoretools.Chord(
                ['c', 'g', "c'"],
                (1, 4),
                )
        return token

    # VERIFIED
    # SOURCE: lexer.ll +381
    # <chords,notes,figures>R/[-_]|R
    #@lex.TOKEN(r'R(?=[-_])|R')
    @lex.TOKEN('R')
    def t_notes_381(self, token):
        token.type = 'MULTI_MEASURE_REST'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +386
    # <INITIAL,chords,figures,lyrics,markup,notes>#
    def t_INITIAL_markup_notes_386(self, token):
        '\#'
        from abjad.tools import lilypondparsertools
        #token.type = 'SCHEME_START'
        #token.lexer.push_state('INITIAL')
        scheme_parser = lilypondparsertools.SchemeParser(debug=False)
        input_string = token.lexer.lexdata[token.lexpos + 1:]
        #print 'PREPARSE'
        try:
            scheme_parser(input_string)
        except SchemeParserFinishedError:
            result = scheme_parser.result
            cursor_end = scheme_parser.cursor_end
            #print 'PARSED: {!r}'.format(input_string[:cursor_end])
            token.value = result
            token.type = 'SCM_TOKEN'
            #if isinstance(result, str):
            #    token.type = 'STRING'
            #    if token.value.find(' ') != -1:
            #        token.value = '"{}"'.format(token.value)
            #else:
            #    token.type = 'SCM_TOKEN'
            token.lexer.skip(cursor_end + 1)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +405
    # <INITIAL,chords,figures,lyrics,markup,notes>\$	{ //immediate scm

    # VERIFIED
    # SOURCE: lexer.ll +426
    # <INITIAL,notes,lyrics>\<\<
    def t_INITIAL_notes_426(self, token):
        r'\<\<'
        token.type = 'DOUBLE_ANGLE_OPEN'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +430
    # <INITIAL,notes,lyrics>\>\>
    def t_INITIAL_notes_430(self, token):
        r'\>\>'
        token.type = 'DOUBLE_ANGLE_CLOSE'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +437
    # <INITIAL,notes>\<
    def t_INITIAL_notes_437(self, token):
        r'\<'
        token.type = 'ANGLE_OPEN'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +441
    # <INITIAL,notes>\>
    def t_INITIAL_notes_441(self, token):
        r'\>'
        token.type = 'ANGLE_CLOSE'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +448
    # <figures>-

    # VERIFIED
    # SOURCE: lexer.ll +452
    # <figures>\>

    # VERIFIED
    # SOURCE: lexer.ll +456
    # <figures>\<

    # VERIFIED
    # SOURCE: lexer.ll +460
    # <figures>\\\+

    # VERIFIED
    # SOURCE: lexer.ll +464
    # <figures>\\!

    # VERIFIED
    # SOURCE: lexer.ll +468
    # <figures>\\\\

    # VERIFIED
    # SOURCE: lexer.ll +472
    # <figures>[][]

    # VERIFIED
    # SOURCE: lexer.ll +479
    # <notes,figures>{WORD}/[-_]|{WORD}
    #@lex.TOKEN('{WORD}(?=[-_])|{WORD}'.format(WORD=WORD))
    @lex.TOKEN(WORD)
    def t_notes_479(self, token):
        self.scan_bare_word(token)
        return token

    # SOURCE: lexer.ll +483
    # <notes,figures>\\\"
    def t_notes_483(self, token):
        r'\\\"'
        token.lexer.push_state('commandquote')
        self.string_accumulator = ''

    # VERIFIED
    # SOURCE: lexer.ll +486
    # <notes,figures>{COMMAND}/[-_]|{COMMAND}
    #@lex.TOKEN('{COMMAND}(?=[-_])|{COMMAND}'.format(COMMAND=COMMAND))
    @lex.TOKEN(COMMAND)
    def t_notes_486(self, token):
        token.type = self.scan_escaped_word(token)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +490
    # <notes,figures>{FRACTION}
    @lex.TOKEN(FRACTION)
    def t_notes_490(self, token):
        from abjad.tools import lilypondparsertools
        token.type = 'FRACTION'
        parts = token.value.split('/')
        token.value = lilypondparsertools.LilyPondFraction(
            int(parts[0]),
            int(parts[1]),
            )
        return token

    # VERIFIED
    # SOURCE: lexer.ll +494
    # <notes,figures>{STRICTREAL}
    @lex.TOKEN(STRICTREAL)
    def t_notes_494(self, token):
        token.type = 'REAL'
        token.value = float(token.value)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +498
    # <notes,figures>{UNSIGNED}/[/.]|{UNSIGNED}
    #@lex.TOKEN('{UNSIGNED}(?=[/.])|{UNSIGNED}'.format(UNSIGNED=UNSIGNED))
    @lex.TOKEN(UNSIGNED)
    def t_notes_498(self, token):
        token.type = 'UNSIGNED'
        token.value = int(token.value)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +503
    # <notes,figures>{E_UNSIGNED}
    @lex.TOKEN(E_UNSIGNED)
    def t_notes_503(self, token):
        token.type = 'E_UNSIGNED'
        token.value = int(token.value[1:])
        return token

    # VERIFIED
    # SOURCE: lexer.ll +510
    # <quote,commandquote>\\{ESCAPED}
    @lex.TOKEN('\\{ESCAPED}'.format(ESCAPED=ESCAPED))
    def t_quote_commandquote_510(self, token):
        self.string_accumulator += token.value

    # VERIFIED
    # SOURCE: lexer.ll +515
    # <quote,commandquote>[^\\""]+
    def t_quote_commandquote_515(self, token):
        r'[^\\""]+'
        self.string_accumulator += token.value

    # VERIFIED
    # SOURCE: lexer.ll +515
    # <quote,commandquote>[^\\""]+
    def t_quote_commandquote_515_b(self, token):
        r'\\"'
        # This catches quotation marks inside quotes.
        # Why doesn't the earlier rule at t_quote_commandquote_515() work?
        self.string_accumulator += token.value

    # VERIFIED
    # SOURCE: lexer.ll +519
    # <quote,commandquote>\"
    def t_quote_commandquote_519(self, token):
        r'\"'
        token.value = self.string_accumulator
        if token.lexer.current_state() == 'commandquote':
            token.type = self.scan_escaped_word(token)
        else:
            token.type = 'STRING'
        token.lexer.pop_state()
        #print("EXITED QUOTE", token)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +536
    # <quote,commandquote>\\
    def t_quote_commandquote_536(self, token):
        r'\\'
        self.string_accumulator += token.value

    # VERIFIED
    # SOURCE: lexer.ll +543
    # <lyrics>\"

    # VERIFIED
    # SOURCE: lexer.ll +546
    # <lyrics>{FRACTION}

    # VERIFIED
    # SOURCE: lexer.ll +550
    # <lyrics>{STRICTREAL}

    # VERIFIED
    # SOURCE: lexer.ll +554
    # <lyrics>{UNSIGNED}/[/.]|{UNSIGNED}

    # VERIFIED
    # SOURCE: lexer.ll +559
    # <lyrics>\\\"

    # VERIFIED
    # SOURCE: lexer.ll +562
    # <lyrics>{COMMAND}/[-_]|{COMMAND}

    # VERIFIED
    # SOURCE: lexer.ll +566
    # <lyrics>\\.|\|

    # VERIFIED
    # SOURCE: lexer.ll +571
    # <lyrics>[*.=]

    # VERIFIED
    # SOURCE: lexer.ll +575
    # <lyrics>[^|*.=$#{}\"\\ \t\n\r\f0-9][^$#{}\"\\ \t\n\r\f0-9]*

    # VERIFIED
    # SOURCE: lexer.ll +589
    # <lyrics>[{}]

    # VERIFIED
    # SOURCE: lexer.ll +595
    # <chords>{WORD}/[-_]|{WORD}

    # VERIFIED
    # SOURCE: lexer.ll +599
    # <chords>\\\"

    # VERIFIED
    # SOURCE: lexer.ll +602
    # <chords>{COMMAND}/[-_]|{COMMAND}

    # VERIFIED
    # SOURCE: lexer.ll +606
    # <chords>{FRACTION}

    # VERIFIED
    # SOURCE: lexer.ll +610
    # <chords>{UNSIGNED}/\/|{UNSIGNED}

    # VERIFIED
    # SOURCE: lexer.ll +615
    # <chords>-

    # VERIFIED
    # SOURCE: lexer.ll +619
    # <chords>:

    # VERIFIED
    # SOURCE: lexer.ll +623
    # <chords>\/\+

    # VERIFIED
    # SOURCE: lexer.ll +627
    # <chords>\/

    # VERIFIED
    # SOURCE: lexer.ll +631
    # <chords>\^

    # VERIFIED
    # SOURCE: lexer.ll +639
    # <markup>\\score
    def t_markup_639(self, token):
        r'\\score'
        token.type = 'SCORE'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +643
    # <markup>\\score-lines
    def t_markup_643(self, token):
        r'\\score-lines'
        token.type = 'SCORELINES'
        return token

    # VERIFIED
    # SOURCE: lexer.ll +647
    # <markup>\\\"
    def t_markup_647(self, token):
        r'\\\\"'
        token.lexer.push_state('commandquote')
        self.string_accumulator = ''

    # VERIFIED
    # SOURCE: lexer.ll +650
    # <markup>{COMMAND}/[-_]|{COMMAND}
    #@lex.TOKEN('{COMMAND}(?=[-_])|{COMMAND}'.format(COMMAND=COMMAND))
    @lex.TOKEN(COMMAND)
    def t_markup_650(self, token):
        value = token.value[1:]
        if (
            value in self.client._markup_functions or
            value in self.client._markup_list_functions
            ):
            if value in self.client._markup_functions:
                token.type = 'MARKUP_FUNCTION'
                signature = self.client._markup_functions[value]
            else:
                token.type = 'MARKUP_LIST_FUNCTION'
                signature = self.client._markup_list_functions[value]
            self.push_signature(signature, token)
        else:
            token.type = self.scan_escaped_word(token)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +701
    # <markup>[^$#{}\"\\ \t\n\r\f]+
    def t_markup_701(self, token):
        r'[^\$#{}\"\\ \t\n\r\f]+'
        token.type = 'STRING'
        return token

    # SOURCE: lexer.ll +707
    # <markup>[{}]
    def t_markup_707(self, token):
        r'[{}]'
        # Set token type equal to value when returning character literal.
        token.type = token.value
        return token

    # REVERIFY
    ## SOURCE: lexer.ll +713
    ## <longcomment><<EOF>>
    #def t_longcomment_713(self, token):
    #    r'$'
    #    message = 'EOF!'
    #    raise LilyPondParserError(message)
    #    token.lexer.pop_state()

    # REVERIFY
    ## SOURCE: lexer.ll +718
    ## <quote,commandquote><<EOF>>
    #def t_quote_commandquote_718(self, token):
    #    r'$'
    #    message = 'EOF!'
    #    raise LilyPondParserError(message)
    #    token.lexer.pop_state()

    # REVERIFY
    ## SOURCE: lexer.ll +723
    ## <<EOF>>
    #def t_INITIAL_723(self, token):
    #    r'$'
    #    message = 'EOF!'
    #    raise LilyPondParserError(message)
    #    token.lexer.pop_state()

    # VERIFIED
    # SOURCE: lexer.ll +751
    # <maininput>{ANY_CHAR}

    # VERIFIED
    # SOURCE: lexer.ll +759
    # <INITIAL>{WORD}/[-_]|{WORD}
    #@lex.TOKEN(r'{WORD}(?=[-_])|{WORD}'.format(WORD=WORD))
    @lex.TOKEN(WORD)
    def t_INITIAL_759(self, token):
        self.scan_bare_word(token)
        return token

    # VERIFIED
    # SOURCE: lexer.ll +763
    # <INITIAL>\\\"
    def t_INITIAL_763(self, token):
        r'\\\"'
        token.lexer.push_state('commandquote')
        self.string_accumulator = ''

    # VERIFIED
    # SOURCE: lexer.ll +766
    # <INITIAL>{COMMAND}/[-_]|{COMMAND}
    #@lex.TOKEN(r'{COMMAND}(?=[-_])|{COMMAND}'.format(COMMAND=COMMAND))
    @lex.TOKEN(COMMAND)
    def t_INITIAL_766(self, token):
        token.type = self.scan_escaped_word(token)
        return token

    ### IN PROGRESS ###

    # SOURCE: lexer.ll +772
    # {FRACTION}
    @lex.TOKEN(FRACTION)
    def t_772(self, token):
        from abjad.tools import lilypondparsertools
        token.type = 'FRACTION'
        parts = token.value.split('/')
        token.value = lilypondparsertools.LilyPondFraction(
            int(parts[0]),
            int(parts[1]),
            )
        return token

    # SOURCE: lexer.ll +777
    # -{UNSIGNED}|{REAL}
    @lex.TOKEN('-{UNSIGNED}|{REAL}'.format(UNSIGNED=UNSIGNED, REAL=REAL))
    def t_777(self, token):
        token.type = 'REAL'
        token.value = float(token.value)
        return token

    # SOURCE: lexer.ll +783
    # {UNSIGNED}/\/|{UNSIGNED}
    @lex.TOKEN(UNSIGNED)
    def t_783(self, token):
        token.type = 'UNSIGNED'
        token.value = int(token.value)
        return token

    # SOURCE: lexer.ll +790
    # -/\.
    @lex.TOKEN('-(?=[\.])')
    def t_790(self, token):
        token.type = token.value
        return token

    # SOURCE: lexer.ll +795
    # <INITIAL,chords,lyrics,figures,notes>{SPECIAL}
    @lex.TOKEN(SPECIAL)
    def t_INITIAL_note_795(self, token):
        token.type = token.value
        return token

    # SOURCE: lexer.ll +800
    # <INITIAL,chords,lyrics,figures,notes>{SHORTHAND}
    #@lex.TOKEN(SHORTHAND)
    @lex.TOKEN(r'\\.')
    def t_INITIAL_notes_800(self, token):
        # Why doesn't {SHORTHAND} work here?
        token.type = self.characters.get(token.value[1], 'E_CHAR')
        return token

    # SOURCE: lexer.ll +804
    # <*>.[\200-\277]*
    @lex.TOKEN('.[\200-\277]*')
    def t_804(self, token):
        # Is this even necessary under Python?
        pass

    ### DEFAULT RULES ###

    t_ignore = ''  # let the grammar handle ignoring things
    # t_extratoken_ignore = t_ignore
    # t_chords_ignore = t_ignore
    t_commandquote_ignore = t_ignore
    # t_figures_ignore = t_ignore
    # t_incl_ignore = t_ignore
    # t_lyrics_ignore = t_ignore
    # t_lyric_quote_ignore = t_ignore
    t_longcomment_ignore = t_ignore
    t_markup_ignore = t_ignore
    t_notes_ignore = t_ignore
    t_quote_ignore = t_ignore
    # t_sourcefileline_ignore = t_ignore
    # t_sourcefilename_ignore = t_ignore
    t_version_ignore = t_ignore
    t_scheme_ignore = t_ignore

    def t_newline(self, token):
        r'\n+'
        token.lexer.lineno += token.value.count("\n")

    def t_error(self, token):
        message = 'LilyPondParser: Illegal character {!r}'
        message = message.format(token.value[0])
        print(message)
        token.lexer.skip(1)

    # t_extratoken_error = t_error
    # t_chords_error = t_error
    t_commandquote_error = t_error
    # t_figures_error = t_error
    # t_incl_error = t_error
    # t_lyrics_error = t_error
    # t_lyric_quote_error = t_error
    t_longcomment_error = t_error
    t_markup_error = t_error
    t_notes_error = t_error
    t_quote_error = t_error
    # t_sourcefileline_error = t_error
    # t_sourcefilename_error = t_error
    t_version_error = t_error
    t_scheme_error = t_error

    ### PUBLIC METHODS ###

    def scan_bare_word(self, token):
        from abjad.ly import drums
        if token.lexer.current_state() in ('notes',):
            value = token.value
            pitch_names = self.client._pitch_names
            if value in pitch_names:
                token.type = 'NOTENAME_PITCH'
                token.value = pitch_names[value]
            elif value in drums:
                token.type = 'NOTENAME_PITCH'
                token.value = drums[value]
            elif value == 'q' and self.client._last_chord:
                token.type = 'CHORD_REPETITION'
            else:
                token.type = 'STRING'
        else:
            token.type = 'STRING'

    def scan_escaped_word(self, token):
        from abjad.tools import lilypondparsertools
        # first, check for it in the keyword list
        if token.value in self.keywords:
            value = self.keywords[token.value]
            if value == 'MARKUP':
                token.lexer.push_state('markup')
                if token.lexer.current_state() == 'lyrics':
                    return 'LYRIC_MARKUP'
            elif value == 'WITH':
                token.lexer.push_state('INITIAL')
            return value
        identifier = token.value[1:]
        # check for the identifier in the scope stack
        lookup = self.client._resolve_identifier(identifier)
        if lookup is not None:
            token.value = copy.deepcopy(lookup.value)
            return self.identifiers[lookup.type]
        # then, check for it in the "current_module" dictionary
        # which we've dumped out of LilyPond
        if identifier not in self.client._current_module:
            message = 'unknown escaped word: {!r}.'
            message = message.format(token.value)
            raise LilyPondParserError(message)
        lookup = self.client._current_module[identifier]
        # if the lookup resolves to a function definition,
        # we have to push artificial tokens onto the token stack.
        # the tokens are pushed in reverse order (LIFO).
        if isinstance(lookup, dict) and 'type' in lookup:
            if lookup['type'] == 'ly:music-function?':
                signature = lookup['signature']
                funtype = self.function_predicates.get(signature[0], 'SCM_FUNCTION')
                self.push_signature(signature[1:], token)
                return funtype
            elif lookup['type'] == 'ly:prob?' and 'event' in lookup['types']:
                return 'EVENT_IDENTIFIER'
        # we also check for other types, to handle \longa, \breve etc.
        elif isinstance(lookup, lilypondparsertools.LilyPondDuration):
            token.value = copy.copy(lookup)
            return 'DURATION_IDENTIFIER'
        # else...
        token.value = copy.copy(lookup)
        return 'SCM_IDENTIFIER'

    def push_signature(self, signature, token):
        artificial_token = lex.LexToken()
        artificial_token.type = 'EXPECT_NO_MORE_ARGS'
        artificial_token.value = None
        artificial_token.lineno = token.lineno
        artificial_token.lexpos = token.lexpos
        self.client._push_extra_token(artificial_token)
        optional = False
        for predicate in signature:
            if predicate == 'optional?':
                optional = True
                continue
            artificial_token = lex.LexToken()
            artificial_token.value = predicate
            artificial_token.lineno = token.lineno
            artificial_token.lexpos = token.lexpos
            artificial_token.type = self.predicates.get(predicate, 'EXPECT_SCM')
            self.client._push_extra_token(artificial_token)
            if optional:
                optional_token = lex.LexToken()
                optional_token.value = 'optional?'
                optional_token.lineno = token.lineno
                optional_token.lexpos = token.lexpos
                optional_token.type = 'EXPECT_OPTIONAL'
                self.client._push_extra_token(optional_token)
                optional = False