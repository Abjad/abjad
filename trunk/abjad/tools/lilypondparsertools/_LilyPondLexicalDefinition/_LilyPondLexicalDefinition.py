from fractions import Fraction
from ply.lex import TOKEN
import re


class _LilyPondLexicalDefinition(object):

    def __init__(self, client):
        self.client = client

    states = (
        # lexer.ll:115
        # ('extratoken', 'exclusive'),
        # ('chords', 'exclusive'),
        # ('figures', 'exclusive'),
        # ('incl', 'exclusive'),
        # ('lyrics', 'exclusive'),
        # ('lyric_quote ', 'exclusive'),
        ('longcomment', 'exclusive'),
        # ('markup', 'exclusive'),
        ('notes', 'exclusive'),
        ('quote', 'exclusive'),
        # ('sourcefileline', 'exclusive'),
        # ('sourcefilename', 'exclusive'),
        ('version', 'exclusive'),
        # not in lexer.ll (using abj crude scheme parsing)
        # ('scheme', 'exclusive'),
    )

    # lexer.ll:129
    A               = r'[a-zA-Z\200-\377]'
    AA              = r'(%s|_)' % A
    N               = r'[0-9]'
    AN              = r'(%s|%s)' % (AA, N)
    ANY_CHAR        = r'(.|\n)'
    PUNCT           = r"[?!:'`]"
    ACCENT          = r'''\\[`'"^]'''
    NATIONAL        = r'[\001-\006\021-\027\031\036]'
    TEX             = r'%s|-|%s|%s|%s' % (AA, PUNCT, ACCENT, NATIONAL)
    WORD            = r'%s%s*' % (A, AN)
    DASHED_WORD     = r'%s(%s|-)*' % (A, AN)
    DASHED_KEY_WORD = r'\\%s' % DASHED_WORD

    # lexer.ll:144
    ALPHAWORD       = r'%s+' % A
    DIGIT           = r'%s' % N
    UNSIGNED        = r'%s+' % N
    E_UNSIGNED      = r'\\%s+' % N
    FRACTION        = r'%s+\/%s+' % (N, N)
    INT             = r'(-?%s)' % UNSIGNED
    REAL            = r'((%s\.%s*)|(-?\.%s+))' % (INT, N, N)
    KEYWORD         = r'\\%s' % WORD
    WHITE           = r'[ \n\t\f\r]' # only whitespace
    HORIZONTALWHITE = r'[ \t]' # only non-line-breaking whitespace
    BLACK           = r'[^ \n\t\f\r]' # only non-whitespace
    RESTNAME        = r'[rs]'
    NOTECOMMAND     = r'\\%s+' % A
    MARKUPCOMMAND   = r'\\(%s|[-_])+' % A
    LYRICS          = r'(%s|%s)[^0-9 \t\n\r\f]*' % (AA, TEX)
    ESCAPED         = r'''[nt\\'"]'''
    EXTENDER        = r'__'
    HYPHEN          = r'--'
    BOM_UTF8        = r'\357\273\277'

    note_names = {
        'english': re.compile('^[a-g](ss|s|ff|f|qf|qs)?$'),
    }

    keywords = {
        # parser.yy:182, lily-lexer.cc:39
        '\\accepts': 'ACCEPTS',
        '\\addlyrics': 'ADDLYRICS',
        '\\alias': 'ALIAS',
        '\\alternative': 'ALTERNATIVE',
        '\\book': 'BOOK',
        '\\bookpart': 'BOOKPART',
        '\\change': 'CHANGE',
        '\\chordmode': 'CHORDMODE',
        '\\chords': 'CHORDS',
        '\\consists': 'CONSISTS',
        '\\context': 'CONTEXT',
        '\\default': 'DEFAULT',
        '\\defaultchild': 'DEFAULTCHILD',
        '\\denies': 'DENIES',
        '\\description': 'DESCRIPTION',
        '\\drummode': 'DRUMMODE',
        '\\drums': 'DRUMS',
        '\\figuremode': 'FIGUREMODE',
        '\\figures': 'FIGURES',
        '\\grobdescriptions': 'GROBDESCRIPTIONS',
        '\\header': 'HEADER',
        '\\version-error': 'INVALID',
        '\\key': 'KEY',
        '\\layout': 'LAYOUT',
        '\\lyricmode': 'LYRICMODE',
        '\\lyrics': 'LYRICS',
        '\\lyricsto': 'LYRICSTO',
        '\\mark': 'MARK',
        '\\markup': 'MARKUP',
        '\\markuplines': 'MARKUPLINES',
        '\\midi': 'MIDI',
        '\\name': 'NAME',
        '\\notemode': 'NOTEMODE',
        '\\once': 'ONCE',
        '\\override': 'OVERRIDE',
        '\\paper': 'PAPER',
        '\\partial': 'PARTIAL',
        '\\remove': 'REMOVE',
        '\\repeat': 'REPEAT',
        '\\rest': 'REST',
        '\\revert': 'REVERT',
        '\\score': 'SCORE',
        '\\sequential': 'SEQUENTIAL',
        '\\set': 'SET',
        '\\simultaneous': 'SIMULTANEOUS',
        '\\tempo': 'TEMPO',
        '\\times': 'TIMES',
        '\\type': 'TYPE',
        '\\unset': 'UNSET',
        '\\with': 'WITH',

        # parser.yy:233
        '\\time': 'TIME_T',
        '\\new': 'NEWCONTEXT',

        # ???
#        '\\objectid': 'OBJECTID',
    }

    tokens = [
        # parser.yy:240
        'CHORD_BASS', # "/+"
        'CHORD_CARET', # "^"
        'CHORD_COLON', # ":"
        'CHORD_MINUS', # "-"
        'CHORD_SLASH', # "/"
        'ANGLE_OPEN', # "<"
        'ANGLE_CLOSE', # ">"
        'DOUBLE_ANGLE_OPEN', # "<<"
        'DOUBLE_ANGLE_CLOSE', # ">>"
        'E_BACKSLASH', # "\\"
        'E_ANGLE_CLOSE', # "\\>"
        'E_CHAR', # "\\C[haracter]"
        'E_CLOSE', # "\\)"
        'E_EXCLAMATION', # "\\!"
        'E_BRACKET_OPEN', # "\\["
        'E_OPEN', # "\\("
        'E_BRACKET_CLOSE', # "\\]"
        'E_ANGLE_OPEN', # "\\<"
        'E_PLUS', # "\\+"
        'E_TILDE', # "\\~"
        'EXTENDER', # "__"

        # parser.yy:265
        'FIGURE_CLOSE', # "\\>"
        'FIGURE_OPEN', # "\\<"
        'FIGURE_SPACE', # "_"
        'HYPHEN', # "--"

        # parser.yy:270
        'CHORDMODIFIERS',
        'LYRIC_MARKUP',
        'MULTI_MEASURE_REST',

        # parser.yy:275
        'E_UNSIGNED',
        'UNSIGNED',

        # parser.yy:278
        'EXPECT_MARKUP', # "markup?"
        'EXPECT_MUSIC', # "ly:music?"
        'EXPECT_PITCH', # "ly:pitch?"
        'EXPECT_DURATION', # "ly:duration?"
        'EXPECT_SCM', # "scheme?"
        'EXPECT_MARKUP_LIST', # "markup-list?"
        'EXPECT_OPTIONAL', # "optional?"
        'EXPECT_NO_MORE_ARGS',

        # parser.yy:289
        'EMBEDDED_LILY',

        # parser.yy:292
        'BOOK_IDENTIFIER',
        'CHORDMODIFIER_PITCH',
        'CHORD_MODIFIER',
        'CHORD_REPETITION',
        'CONTEXT_DEF_IDENTIFIER',
        'CONTEXT_MOD_IDENTIFIER',
        'DRUM_PITCH',
        'PITCH_IDENTIFIER',
        'DURATION_IDENTIFIER',
        'EVENT_IDENTIFIER',
        'EVENT_FUNCTION',
        'FRACTION',
        'LYRICS_STRING',
        'LYRIC_MARKUP_IDENTIFIER',
        'MARKUP_FUNCTION',
        'MARKUP_LIST_FUNCTION',
        'MARKUP_IDENTIFIER',
        'MARKUPLINES_IDENTIFIER',
        'MUSIC_FUNCTION',
        'MUSIC_IDENTIFIER',
        'NOTENAME_PITCH',
        'NUMBER_IDENTIFIER',
        'OUTPUT_DEF_IDENTIFIER',
        'REAL',
        'RESTNAME',
        'SCM_FUNCTION',
        'SCM_IDENTIFIER',
        'SCM_TOKEN',
        'SCORE_IDENTIFIER',
        'STRING',
        'STRING_IDENTIFIER',
        'TONICNAME_PITCH',
    ] + keywords.values( )

    literals = (
        '!', "'", '(', ')', '*', '+', ',', '-', 
        '.', '/', ':', '<', '=', '>', '?', '[', 
        '\\', ']', '^', '_', '{', '|', '}', '~'
    )

    string_accumulator = ''

    ### LEXICAL RULES ###

    # lexer.ll:165
    # <*>\r
    def t_ANY_165(self, t):
        r'\r'
        pass

    # lexer.ll:169
    # <extratoken>{ANY_CHAR}

    # lexer.ll:186
    # <extratoken><<EOF>>

    # lexer.ll:201
    # <INITIAL,chords,lyrics,figures,notes>{BOM_UTF8}/.*

    # lexer.ll:210
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>"%{"
    def t_notes_210(self, t):
        r'%{'
        t.lexer.push_state('longcomment')
        pass

    # lexer.ll:214
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*[\n\r]
    def t_notes_214(self, t):
        r'%[^{\n\r][^\n\r]*[\n\r]'
        pass

    #lexer.ll:216
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r]
    def t_notes_216(self, t):
        r'%[^{\n\r]'
        pass

    #lexer.ll:218
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[\n\r]
    def t_notes_218(self, t):
        r'%[\n\r]'
        pass

    # lexer.ll:220
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*
    def t_notes_220(self, t):
        r'%[^{\n\r][^\n\r]*'
        pass

    # lexer.ll:222
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>{WHITE}+
    def t_notes_222(self, t):
        '[ \n\t\f\r]'
        pass

    # lexer.ll:227
    # <INITIAL,notes,figures,chords,markup>\"
    def t_notes_227(self, t):
        r'\"'
        t.lexer.push_state('quote')
        self.string_accumulator = ''
        pass

    # lexer.ll:233
    # <INITIAL,chords,lyrics,notes,figures>\\version{WHITE}*
    def t_notes_233(self, t):
        r'\\version'
        t.lexer.push_state('version')

    # lexer.ll:236
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefilename{WHITE}*

    # lexer.ll:239
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefileline{WHITE}*

    # lexer.ll:242
    # <version>\"[^"]*\"
    def t_version_242(self, t):
        r'\"[^"]*\"'
        t.lexer.pop_state( )
        t.type = 'STRING'
        t.value = '\\version ' + t.value
        return t

    # lexer.ll:256
    # <sourcefilename>\"[^"]*\"

    # lexer.ll:270
    # <sourcefileline>{INT}

    # lexer.ll:278
    # <version>{ANY_CHAR}
    @TOKEN(ANY_CHAR)
    def t_version_278(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # lexer.ll:282
    # <sourcefilename>{ANY_CHAR}

    # lexer.ll:286
    # <sourcefileline>{ANY_CHAR}

    # lexer.ll:291
    # <longcomment>[^\%]*
    def t_longcomment_291(self, t):
        r'[^\%]+'
        pass

    # lexer.ll:293
    # <longcomment>\%*[^}%]*
    def t_longcomment_293(self, t):
        r'\%+[^}%]*'
        pass

    # lexer.ll:296
    # <longcomment>"%"+"}"
    def t_longcomment_296(self, t):
        r'%}'
        t.lexer.pop_state( )

    # lexer.ll:302
    # <INITIAL,chords,lyrics,notes,figures>\\maininput

    # lexer.ll:312
    # <INITIAL,chords,lyrics,figures,notes>\\include

    # lexer.ll:315
    # <incl>\"[^"]*\"

    # lexer.ll:322
    # <incl>\\{BLACK}*{WHITE}?

    # lexer.ll:341
    # <incl,version,sourcefilename>\"[^"]*
    def t_version_341(self, t):
        r'"[^"]*'
        raise Exception('End quote missing.')

    # lexer.ll:345
    # <chords,notes,figures>{RESTNAME}
    @TOKEN(RESTNAME)
    def t_notes_345(self, t):
        t.type = 'RESTNAME'
        return t

    # lexer.ll:350
    # <chords,notes,figures>R
    def t_notes_350(self, t):
        'R'
        t.type = 'MULTI_MEASURE_REST'
        return t

    # lexer.ll:353
    # <INITIAL,chords,figures,lyrics,markup,notes>#

    # lexer.ll:387
    # <INITIAL,notes,lyrics>\<\<
    def t_notes_387(self, t):
        r'\<\<'
        t.type = 'DOUBLE_ANGLE_OPEN'
        return t

    # lexer.ll:390
    # <INITIAL,notes,lyrics>\>\>
    def t_notes_390(self, t):
        r'\>\>'
        t.type = 'DOUBLE_ANGLE_CLOSE'
        return t

    # lexer.ll:396
    # <INITIAL,notes>\<
    def t_notes_396(self, t):
        r'\<'
        t.type = 'ANGLE_OPEN'
        return t

    # lexer.ll:399
    # <INITIAL,notes>\>
    def t_notes_399(self, t):
        r'\>'
        t.type = 'ANGLE_CLOSE'
        return t
        
    # lexer.ll:405
    # <figures>_

    # lexer.ll:408
    # <figures>\>

    # lexer.ll:411
    # <figures>\<

    # lexer.ll:417
    # <notes,figures>{ALPHAWORD}
    @TOKEN(ALPHAWORD)
    def t_notes_417(self, t):
        if self.note_names['english'].match(t.value) is not None:
            t.type = 'NOTENAME_PITCH'
        else:
            t.type = 'STRING'
        return t

    # lexer.ll:421
    # <notes,figures>{NOTECOMMAND}
    @TOKEN(NOTECOMMAND)
    def t_notes_421(self, t):
        lookup = self.scan_escaped_word(t)
        t.type = lookup
        return t

    # lexer.ll:424
    # <notes,figures>{FRACTION}
    @TOKEN(FRACTION)
    def t_notes_424(self, t):
        t.type = 'FRACTION'
        parts = t.value.split('/')
        t.value = Fraction(int(parts[0]), int(parts[1]))
        return t

    # lexer.ll:428
    # <notes,figures>{UNSIGNED}/\/|{UNSIGNED}
    @TOKEN('%s/\/|%s' % (UNSIGNED, UNSIGNED))
    def t_notes_428(self, t):
        t.type = 'UNSIGNED'
        t.value = int(t.value)
        return t

    # lexer.ll:433
    # <notes,figures>{E_UNSIGNED}
    @TOKEN(E_UNSIGNED)
    def t_notes_433(self, t):
        t.type = 'E_UNSIGNED'
        t.value = int(t.value[1:])
        return t

    # lexer.ll:440
    # <quote,lyric_quote>\\{ESCAPED}
    @TOKEN('\\%s' % ESCAPED)
    def t_quote_440(self, t):
        self.string_accumulator += t.value
        pass

    # lexer.ll:443
    # <quote,lyric_quote>[^\\""]+
    def t_quote_443(self, t):
        r'[^\\""]+'
        self.string_accumulator += t.value
        pass

    # lexer.ll:446
    # <quote,lyric_quote>\"
    def t_quote_446(self, t):
        r'\"'
        t.lexer.pop_state( )
        t.type = 'STRING'
        t.value = self.string_accumulator
        return t

    # lexer.ll:456
    # <quote,lyric_quote>.
    def t_quote_456(self, t):
        r'.'
        self.string_accumulator += t.value
        pass

    # lexer.ll:462
    # <lyrics>\"

    # lexer.ll:465
    # <lyrics>{FRACTION}

    # lexer.ll:469
    # <lyrics>{UNSIGNED}/\/[^0-9]

    # lexer.ll:473
    # <lyrics>{UNSIGNED}/\/|{UNSIGNED}

    # lexer.ll:478
    # <lyrics>{NOTECOMMAND}

    # lexer.ll:481
    # <lyrics>{LYRICS}

    # lexer.ll:499
    # <lyrics>.

    # lexer.ll:504
    # <chords>{ALPHAWORD}

    # lexer.ll:507
    # <chords>{NOTECOMMAND}

    # lexer.ll:510
    # <chords>{FRACTION}

    # lexer.ll:514
    # <chords>{UNSIGNED}/\/[^0-9]

    # lexer.ll:518
    # <chords>{UNSIGNED}/\/|{UNSIGNED}

    # lexer.ll:523
    # <chords>-

    # lexer.ll:526
    # <chords>:

    # lexer.ll:529
    # <chords>\/\+

    # lexer.ll:532
    # <chords>\/

    # lexer.ll:535
    # <chords>\^

    # lexer.ll:538
    # <chords>.

    # lexer.ll:545
    # <markup>\\score

    # lexer.ll:548
    # <markup>{MARKUPCOMMAND}

    # lexer.ll:598
    # <markup>[{}]

    # lexer.ll:601
    # <markup>[^#{}\"\\ \t\n\r\f]+

    # lexer.ll:614
    # <markup>.

    # lexer.ll:619
    # <longcomment><<EOF>>

    # lexer.ll:626
    # <<EOF>>

    # lexer.ll:643
    # <INITIAL>{DASHED_WORD}

    # lexer.ll:646
    # <INITIAL>{DASHED_KEY_WORD}

    # lexer.ll:651
    # -{UNSIGNED}|{REAL}
    @TOKEN('%s|-%s' % (REAL, UNSIGNED))
    def t_651(self, t):
        t.type = 'REAL'
        t.value = float(t.value)
        return t

    # lexer.ll:661
    # -\.
    def t_661(self, t):
        '-\.'
        t.type = 'REAL'
        t.value = 0.0
        return t

    # lexer.ll:666
    # {UNSIGNED}
    @TOKEN(UNSIGNED)
    def t_666(self, t):
        t.type = 'UNSIGNED'
        t.value = float(t.value)
        return t

    # lexer.ll:672
    # [{}]

    # lexer.ll:676
    # [*:=]

    # lexer.ll:682
    # <INITIAL,notes,figures>.

    # lexer.ll:686
    # <INITIAL,lyrics,notes,figures>\\. 
    def t_notes_686(self, t):
        r'\\.'
        if t.value[1] == '>':
            t.type = 'E_ANGLE_CLOSE'
        elif t.value[1] == '<':
            t.type = 'E_ANGLE_OPEN'
        elif t.value[1] == '!':
            t.type = 'E_EXCLAMATION'
        elif t.value[1] == '(':
            t.type = 'E_OPEN'
        elif t.value[1] == ')':
            t.type = 'E_CLOSE'
        elif t.value[1] == '[':
            t.type = 'E_BRACKET_OPEN'
        elif t.value[1] == '+':
            t.type = 'E_PLUS'
        elif t.value[1] == ']':
            t.type = 'E_BRACKET_CLOSE'
        elif t.value[1] == '~':
            t.type = 'E_TILDE'
        elif t.value[1] == '\\':
            t.type = 'E_BACKSLASH'
        else:
            t.type = 'E_CHAR'
        return t

    # lexer.ll:
    # <*>.716
#    def t_ANY_716(self, t):
#        r'.'
#        raise Exception        

    ### DEFAULT RULES ###

    t_ignore = '[ \n\t\f\r]'

#   t_extratoken_ignore = t_ignore
#   t_chords_ignore = t_ignore
#   t_figures_ignore = t_ignore
#   t_incl_ignore = t_ignore
#   t_lyrics_ignore = t_ignore
#   t_lyric_quote_ignore = t_ignore
    t_longcomment_ignore = t_ignore
#   t_markup_ignore = t_ignore
    t_notes_ignore = t_ignore
    t_quote_ignore = t_ignore
#   t_sourcefileline_ignore = t_ignore
#   t_sourcefilename_ignore = t_ignore
    t_version_ignore = t_ignore
#   t_scheme_ignore = t_ignore

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

#   t_extratoken_error = t_error
#   t_chords_error = t_error
#   t_figures_error = t_error
#   t_incl_error = t_error
#   t_lyrics_error = t_error
#   t_lyric_quote_error = t_error
    t_longcomment_error = t_error
#   t_markup_error = t_error
    t_notes_error = t_error
    t_quote_error = t_error
#   t_sourcefileline_error = t_error
#   t_sourcefilename_error = t_error
    t_version_error = t_error
#   t_scheme_error = t_error

    def scan_bare_word(self, t):
        if t.lexer.current_state( ) in ('notes',):
            if self.note_names['english'].match(t.value) is not None:
                return 'NOTENAME_PITCH'
        return 'STRING'        

    def scan_escaped_word(self, t):
        if t.value in self.keywords:
            value = self.keywords[t.value]
            if t.lexer.current_state( ) == 'lyrics' and value == 'MARKUP':
                return 'LYRIC_MARKUP'
            return value

        if t.value[1:] in self.client.assignments:
            node = self.client.assignments[t.value[1:]]

            identifier_lookup = {
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

            return identifier_lookup[node.type]

        raise Exception('Unknown escaped word "%s".' % t.value)
