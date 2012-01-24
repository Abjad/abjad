from fractions import Fraction
from ply.lex import TOKEN
from ply.lex import LexToken
from abjad.tools.durationtools import Duration


class _LilyPondLexicalDefinition(object):

    def __init__(self, client):
        self.client = client

    states = (
        # lexer.ll:115
#        ('extratoken', 'exclusive'),
#        ('chords', 'exclusive'),
#        ('figures', 'exclusive'),
#        ('incl', 'exclusive'),
#        ('lyrics', 'exclusive'),
#        ('lyric_quote ', 'exclusive'),
        ('longcomment', 'exclusive'),
        ('markup', 'exclusive'),
        ('notes', 'exclusive'),
        ('quote', 'exclusive'),
#        ('sourcefileline', 'exclusive'),
#        ('sourcefilename', 'exclusive'),
        ('version', 'exclusive'),
        ('scheme', 'exclusive'),
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
    INT             = r'(-?%s)' % UNSIGNED
    REAL            = r'((%s\.%s*)|(-?\.%s+))' % (INT, N, N)
    E_UNSIGNED      = r'\\%s+' % N
    FRACTION        = r'%s+\/%s+' % (N, N)
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
        '\\header': 'HEADER',
        '\\version-error': 'INVALID',
        '\\layout': 'LAYOUT',
        '\\lyricmode': 'LYRICMODE',
        '\\lyrics': 'LYRICS',
        '\\lyricsto': 'LYRICSTO',
        '\\markup': 'MARKUP',
        '\\markuplist': 'MARKUPLIST',
        '\\midi': 'MIDI',
        '\\name': 'NAME',
        '\\notemode': 'NOTEMODE',
        '\\override': 'OVERRIDE',
        '\\paper': 'PAPER',
        '\\remove': 'REMOVE',
        '\\repeat': 'REPEAT',
        '\\rest': 'REST',
        '\\revert': 'REVERT',
        '\\score': 'SCORE',
        '\\sequential': 'SEQUENTIAL',
        '\\set': 'SET',
        '\\simultaneous': 'SIMULTANEOUS',
        '\\tempo': 'TEMPO',
        '\\type': 'TYPE',
        '\\unset': 'UNSET',
        '\\with': 'WITH',

        # parser.yy:233
        '\\new': 'NEWCONTEXT',

        # ???
#        '\\objectid': 'OBJECTID',
    }

    tokens = [
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

        'FIGURE_CLOSE', # "\\>"
        'FIGURE_OPEN', # "\\<"
        'FIGURE_SPACE', # "_"
        'HYPHEN', # "--"

        'LYRIC_MARKUP',
        'MULTI_MEASURE_REST',

        'E_UNSIGNED',
        'UNSIGNED',

        'EXPECT_MARKUP', # "markup?"
        'EXPECT_PITCH', # "ly:pitch?"
        'EXPECT_DURATION', # "ly:duration?"
        'EXPECT_SCM', # "scheme?"
        'BACKUP', # "(backed-up?)"
        'REPARSE', # "(reparsed?)"
        'EXPECT_MARKUP_LIST', # "markup-list?"
        'EXPECT_OPTIONAL', # "optional?"
        'EXPECT_NO_MORE_ARGS', #

        'EMBEDDED_LILY', # "#{"

        'BOOK_IDENTIFIER',
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
        'LYRIC_ELEMENT',
        'LYRIC_MARKUP_IDENTIFIER',
        'MARKUP_FUNCTION',
        'MARKUP_LIST_FUNCTION',
        'MARKUP_IDENTIFIER',
        'MARKUPLIST_IDENTIFIER',
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

        # for abjad scheme parsing
        'SCHEME_START',

    ] + keywords.values( )

    literals = (
        '!', "'", '(', ')', '*', '+', ',', '-', 
        '.', '/', ':', '<', '=', '>', '?', '[',
        '\\', '^', '_', '{', '|', '}', '~', ']',
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
    def t_INITIAL_notes_210(self, t):
        r'%{'
        t.lexer.push_state('longcomment')
        pass

    # lexer.ll:214
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*[\n\r]
    def t_INITIAL_notes_214(self, t):
        r'%[^{\n\r][^\n\r]*[\n\r]'
        pass

    #lexer.ll:216
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r]
    def t_INITIAL_notes_216(self, t):
        r'%[^{\n\r]'
        pass

    #lexer.ll:218
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[\n\r]
    def t_INITIAL_notes_218(self, t):
        r'%[\n\r]'
        pass

    # lexer.ll:220
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>%[^{\n\r][^\n\r]*
    def t_INITIAL_notes_220(self, t):
        r'%[^{\n\r][^\n\r]*'
        pass

    # lexer.ll:222
    # <INITIAL,chords,figures,incl,lyrics,markup,notes>{WHITE}+
    def t_INITIAL_notes_222(self, t):
        '[ \n\t\f\r]'
        pass

    # lexer.ll:227
    # <INITIAL,notes,figures,chords,markup>\"
    def t_INITIAL_notes_227(self, t):
        r'\"'
        t.lexer.push_state('quote')
        self.string_accumulator = ''
        pass

    # lexer.ll:233
    # <INITIAL,chords,lyrics,notes,figures>\\version{WHITE}*
    @TOKEN('\\version%s*' % WHITE)
    def t_INITIAL_notes_233(self, t):
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

    def t_INITIAL_markup_notes_353_boolean(self, t):
        '\#\#(t|f)'
        t.type = 'SCM_TOKEN'
        if t.value[2] == 't':
            t.value = True
        else:
            t.value = False
        return t

    @TOKEN("\#'%s" % DASHED_WORD)
    def t_INITIAL_markup_notes_353_identifier(self, t):
        t.type = 'SCM_IDENTIFIER'
        t.value = t.value[2:]
        return t

    # lexer.ll:353
    # <INITIAL,chords,figures,lyrics,markup,notes>#
    def t_INITIAL_markup_notes_353(self, t):
        '\#'
        t.type = 'SCHEME_START'
        t.lexer.push_state('INITIAL')
        return t

    # lexer.ll:387
    # <INITIAL,notes,lyrics>\<\<
    def t_INITIAL_notes_387(self, t):
        r'\<\<'
        t.type = 'DOUBLE_ANGLE_OPEN'
        return t

    # lexer.ll:390
    # <INITIAL,notes,lyrics>\>\>
    def t_INITIAL_notes_390(self, t):
        r'\>\>'
        t.type = 'DOUBLE_ANGLE_CLOSE'
        return t

    # lexer.ll:396
    # <INITIAL,notes>\<
    def t_INITIAL_notes_396(self, t):
        r'\<'
        t.type = 'ANGLE_OPEN'
        return t

    # lexer.ll:399
    # <INITIAL,notes>\>
    def t_INITIAL_notes_399(self, t):
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
        language = self.client._parser_variables['language']
        pitch_names = self.client._language_pitch_names[language]
        if t.value in pitch_names:
            t.type = 'NOTENAME_PITCH'
            t.value = pitch_names[t.value]
        elif t.value == 'q' and self.client._parser_variables['last_chord']:
            t.type = 'CHORD_REPETITION'
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
    def t_markup_545(self, t):
        r'\\score'
        t.type = 'SCORE'
        return t

    # lexer.ll:548
    # <markup>{MARKUPCOMMAND}
    @TOKEN(MARKUPCOMMAND)
    def t_markup_548(self, t):
        value = t.value[1:]

        if value in self.client._markup_functions or \
            value in self.client._markup_list_functions:
            if value in self.client._markup_functions:
                t.type = 'MARKUP_FUNCTION'
                signature = self.client._markup_functions[value]
            else:
                t.type = 'MARKUP_LIST_FUNCTION'
                signature = self.client._markup_list_functions[value]

            token = LexToken( )
            token.type = 'EXPECT_NO_MORE_ARGS'
            token.value = None
            self.client._push_extra_token(token)

            for predicate in reversed(signature):
                token = LexToken( )
                token.value = None
                token.lineno = t.lineno
                token.lexpos = t.lexpos
                if predicate in ['markup?', 'cheap-markup?']:
                    token.type = 'EXPECT_MARKUP'
                elif predicate == 'markup-list?':
                    token.type = 'EXPECT_MARKUP_LIST'
                else:
                    token.type = 'EXPECT_SCM'
                    token.value = predicate
                self.client._push_extra_token(token)

        else:
            t.type = self.scan_escaped_word(t)

        return t

    # lexer.ll:598
    # <markup>[{}]
#    def t_markup_598(self, t):
#        r'[{}]'
#        t.type = t.value
#        return t

    # lexer.ll:601
    # <markup>[^#{}\"\\ \t\n\r\f]+
    def t_markup_601(self, t):
        r'[^#{}\"\\ \t\n\r\f]+'
        t.type = 'STRING'
        return t

    # lexer.ll:614
    # <markup>.

    # lexer.ll:619
    # <longcomment><<EOF>>

    # lexer.ll:626
    # <<EOF>>

    # lexer.ll:643
    # <INITIAL>{DASHED_WORD}
    @TOKEN(DASHED_WORD)
    def t_INITIAL_643(self, t):
        t.type = self.scan_bare_word(t)
        return t        

    # lexer.ll:646
    # <INITIAL>{DASHED_KEY_WORD}
    @TOKEN(DASHED_KEY_WORD)
    def t_INITIAL_646(self, t):
        t.type = self.scan_escaped_word(t)
        return t

    # lexer.ll:651
    # -{UNSIGNED}|{REAL}
    @TOKEN(REAL)
    def t_651_a(self, t):
        t.type = 'REAL'
        t.value = float(t.value)
        return t

    @TOKEN('-%s' % UNSIGNED)
    def t_651_b(self, t):
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
    def t_INITIAL_notes_686(self, t):
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

    t_ignore = '' # let the grammar handle ignoring things

    #    t_extratoken_ignore = t_ignore
    #    t_chords_ignore = t_ignore
    #    t_figures_ignore = t_ignore
    #    t_incl_ignore = t_ignore
    #    t_lyrics_ignore = t_ignore
    #    t_lyric_quote_ignore = t_ignore
    t_longcomment_ignore = t_ignore
    t_markup_ignore = t_ignore
    t_notes_ignore = t_ignore
    t_quote_ignore = t_ignore
    #    t_sourcefileline_ignore = t_ignore
    #    t_sourcefilename_ignore = t_ignore
    t_version_ignore = t_ignore

    t_scheme_ignore = t_ignore

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    #    t_extratoken_error = t_error
    #    t_chords_error = t_error
    #    t_figures_error = t_error
    #    t_incl_error = t_error
    #    t_lyrics_error = t_error
    #    t_lyric_quote_error = t_error
    t_longcomment_error = t_error
    t_markup_error = t_error
    t_notes_error = t_error
    t_quote_error = t_error
    #    t_sourcefileline_error = t_error
    #    t_sourcefilename_error = t_error
    t_version_error = t_error

    t_scheme_error = t_error


    def scan_bare_word(self, t):
        if t.lexer.current_state( ) in ('notes',):
            language = self.client._parser_variables['language']
            pitch_names = self.client._language_pitch_names[language]
            if t.value in pitch_names:
                t.type = 'NOTENAME_PITCH'
            elif t.value == 'q' and self.client._parser_variables['last_chord']:
                t.type = 'CHORD_REPETITION'
        return 'STRING'        


    def scan_escaped_word(self, t):

        # first, check for it in the keyword list
        if t.value in self.keywords:
            value = self.keywords[t.value]

            if value == 'MARKUP':
                t.lexer.push_state('markup')
                if t.lexer.current_state( ) == 'lyrics':
                    return 'LYRIC_MARKUP'

            elif value == 'WITH':
                t.lexer.push_state('INITIAL')

            return value

        # then, check for it in the assignments list 
        # (anything assigned in the input string)
        if t.value[1:] in self.client._assignments:
            node = self.client._assignments[t.value[1:]]

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

        # then, check for it in the "current_module" dictionary
        # which we've dumped out of LilyPond
        if t.value[1:] not in self.client._current_module:
            raise Exception('Unknown escaped word "%s".' % t.value)

        lookup = self.client._current_module[t.value[1:]]

        # if the lookup resolves to a function definition,
        # we have to push artificial tokens onto the token stack.
        # the tokens are pushed in reverse order (LIFO).
        if isinstance(lookup, dict) and 'type' in lookup:

            if lookup['type'] == 'ly:music-function?':

                signature = lookup['signature']
                funtype = 'SCM_FUNCTION'
                if signature[0] == 'ly:music?':
                    funtype = 'MUSIC_FUNCTION'
                elif signature[0] == 'ly:event?':
                    funtype = 'EVENT_FUNCTION'

                token = LexToken( )
                token.type = 'EXPECT_NO_MORE_ARGS'
                token.value = None
                token.lineno = t.lineno
                token.lexpos = t.lexpos
                self.client._push_extra_token(token)

                optional = False
                for predicate in signature[1:]:

                    if predicate == 'optional?':
                        optional = True
                        continue

                    token = LexToken( )
                    token.value = predicate
                    token.lineno = t.lineno
                    token.lexpos = t.lexpos

                    if predicate == 'ly:music?':
                        token.type = 'EXPECT_SCM' # ?!?!
                    elif predicate == 'ly:pitch?':
                        token.type = 'EXPECT_PITCH'
                    elif predicate == 'ly:duration?':
                        token.type = 'EXPECT_DURATION'
                    elif predicate in ['markup?', 'cheap-markup?']:
                        token.type = 'EXPECT_MARKUP'
                    else:
                        token.type = 'EXPECT_SCM'

                    self.client._push_extra_token(token)

                    if optional:
                        optional_token = LexToken( )
                        optional_token.value = 'optional?'
                        optional_token.lineno = t.lineno
                        optional_token.lexpos = t.lexpos
                        optional_token.type = 'EXPECT_OPTIONAL'                        
                        self.client._push_extra_token(optional_token)
                        optional = False

                return funtype

            elif lookup['type'] == 'ly:prob?' and 'event' in lookup['types']:
                return 'EVENT_IDENTIFIER'

        # we also check for other types, to handle \longa, \breve etc.
        elif isinstance(lookup, Duration):
            return 'DURATION_IDENTIFIER'

        # what do we do with events?
        return 'SCM_IDENTIFIER'
