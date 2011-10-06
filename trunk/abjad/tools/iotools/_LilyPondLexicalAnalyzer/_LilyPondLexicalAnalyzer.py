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

    ### LEXICAL RULES ###

    # lexer.ll:165
    # <*>\r

    # lexer.ll:169
    # <extratoken>{ANY_CHAR}

    # lexer.ll:186
    # <extratoken><<EOF>>

    # lexer.ll:201
    # <INITIAL,chords,lyrics,figures,notes>{BOM_UTF8}/.*

    # lexer.ll:210
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>"%{"

    # lexer.ll:214
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*[\n\r]

    #lexer.ll:216
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r]

    #lexer.ll:218
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[\n\r]

    # lexer.ll:220
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*

    # lexer.ll:222
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>{WHITE}+

    # lexer.ll:227
    # <INITIAL,notes,figures,chords,markup>\"

    # lexer.ll:233
    # <INITIAL,chords,lyrics,notes,figures>\\version{WHITE}*

    # lexer.ll:236
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefilename{WHITE}*

    # lexer.ll:239
    # <INITIAL,chords,lyrics,notes,figures>\\sourcefileline{WHITE}*

    # lexer.ll:242
    # <version>\"[^"]*\"

    # lexer.ll:256
    # <sourcefilename>\"[^"]*\"

    # lexer.ll:270
    # <sourcefileline>{INT}

    # lexer.ll:278
    # <version>{ANY_CHAR}

    # lexer.ll:282
    # <sourcefilename>{ANY_CHAR}

    # lexer.ll:286
    # <sourcefileline>{ANY_CHAR}

    # lexer.ll:291
    # <longcomment>[^\%]*

    # lexer.ll:293
    # <longcomment>\%*[^}%]*

    # lexer.ll:296
    # <longcomment>"%"+"}"

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

    # lexer.ll:345
    # <chords,notes,figures>{RESTNAME}

    # lexer.ll:350
    # <chords,notes,figures>R

    # lexer.ll:353
    # <INITIAL,chords,figures,lyrics,markup,notes>#

    # lexer.ll:387
    # <INITIAL,notes,lyrics>\<\<

    # lexer.ll:390
    # <INITIAL,notes,lyrics>\>\>

    # lexer.ll:396
    # <INITIAL,notes>\<

    # lexer.ll:399
    # <INITIAL,notes>\>

    # lexer.ll:405
    # <figures>_

    # lexer.ll:408
    # <figures>\>

    # lexer.ll:411
    # <figures>\<

    # lexer.ll:417
    # <notes,figures>{ALPHAWORD}

    # lexer.ll:421
    # <notes,figures>{NOTECOMMAND}

    # lexer.ll:424
    # <notes,figures>{FRACTION}

    # lexer.ll:428
    # <notes,figures>{UNSIGNED}/\/|{UNSIGNED}

    # lexer.ll:433
    # <notes,figures>{E_UNSIGNED}

    # lexer.ll:440
    # <quote,lyric_quote>\\{ESCAPED}

    # lexer.ll:443
    # <quote,lyric_quote>[^\\""]+

    # lexer.ll:446
    # <quote,lyric_quote>\"

    # lexer.ll:456
    # <quote,lyric_quote>.

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

    # lexer.ll:661
    # -\.

    # lexer.ll:666
    # {UNSIGNED}

    # lexer.ll:672
    # [{}]

    # lexer.ll:676
    # [*:=]

    # lexer.ll:682
    # <INITIAL,notes,figures>.

    # lexer.ll:686
    # <INITIAL,lyrics,notes,figures>\\. 

    # lexer.ll:
    # <*>.716

    @TOKEN(KEYWORD)
    def t_KEYWORD(self, t):
        t.type = self.keywords.get(t.value, 'KEYWORD')
        return t
    
    ### DEFAULT RULES ###

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def __init__(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)

    ### OVERRIDES ###

    def __call__(self, input):
        self._lexer.input(input)
        while True:
            token = self._lexer.token( )
            if not token:
                break
            yield token
        return
