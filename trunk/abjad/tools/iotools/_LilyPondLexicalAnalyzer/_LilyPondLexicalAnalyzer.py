from ply import lex
from ply.lex import TOKEN


class _LilyPondLexicalAnalyzer(object):

    states = (
        # lexer.ll:115
        # ('extratoken', 'exclusive'),
        # ('chords', 'exclusive'),
        # ('figures', 'exclusive'),
        # ('incl', 'exclusive'),
        # ('lyrics', 'exclusive'),
        # ('lyric_quote ', 'exclusive'),
        # ('longcomment', 'exclusive'),
        # ('markup', 'exclusive'),
        # ('notes', 'exclusive'),
        # ('quote', 'exclusive'),
        # ('sourcefileline', 'exclusive'),
        # ('sourcefilename', 'exclusive'),
        # ('version', 'exclusive'),
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
    INT             = r'-?%s' % UNSIGNED
    REAL            = r'(%s\.%s*)|(-?\.%s+)' % (INT, N, N)
    KEYWORD         = r'\\%s' % WORD
    WHITE           = r'[ \n\t\f\r]'
    HORIZONTALWHITE = r'[ \t]'
    BLACK           = r'[^ \n\t\f\r]'
    RESTNAME        = r'[rs]'
    NOTECOMMAND     = r'\\%s+' % A
    MARKUPCOMMAND   = r'\\(%s|[-_])+' % A
    LYRICS          = r'(%s|%s)[^0-9 \t\n\r\f]*' % (AA, TEX)
    ESCAPED         = r'''[nt\\'"]'''
    EXTENDER        = r'__'
    HYPHEN          = r'--'
    BOM_UTF8        = r'\357\273\277'

    reserved = {
        # parser.yy:182
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
        '\\invalid': 'INVALID',
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
        '\\octave': 'OCTAVE',
        '\\once': 'ONCE',
        '\\override': 'OVERRIDE',
        '\\paper': 'PAPER',
        '\\partial': 'PARTIAL',
        '\\relative': 'RELATIVE',
        '\\remove': 'REMOVE',
        '\\repeat': 'REPEAT',
        '\\rest': 'REST',
        '\\revert': 'REVERT',
        '\\score': 'SCORE',
        '\\sequential': 'SEQUENTIAL',
        '\\set': 'SET',
        '\\simultaneous': 'SIMULTANEOUS',
        '\\skip': 'SKIP',
        '\\tempo': 'TEMPO',
        '\\times': 'TIMES',
        '\\transpose': 'TRANSPOSE',
        '\\type': 'TYPE',
        '\\unset': 'UNSET',
        '\\with': 'WITH',
        # parser.yy:233
        '\\time': 'TIME_T',
        '\\new': 'NEWCONTEXT'
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

        # parser.yy:
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
    ] + reserved.values( )

    @TOKEN(KEYWORD)
    def t_KEYWORD(self, t):
        t.type = self.reserved.get(t.value, 'KEYWORD')
        return t
    
    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)

    def __call__(self, input):
        self._lexer.input(input)
        while True:
            token = self._lexer.token( )
            if not token:
                break
            yield token
        return


