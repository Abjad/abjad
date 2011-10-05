from ply import lex
from ply.lex import TOKEN


class _LilyPondLexicalAnalyzer(object):

    A               = '[a-zA-Z\200-\377]'
    AA              = '%s|_' % A
    N               = '[0-9]'
    AN              = '%s|%s' % (AA, N)
    ANY_CHAR        = '(.|\n)'
    PUNCT           = "[?!:'`]"
    ACCENT          = '''\\[`'"^]'''
    NATIONAL        = '[\001-\006\021-\027\031\036]'
    TEX             = '%s|-|%s|%s|%s' % (AA, PUNCT, ACCENT, NATIONAL)
    WORD            = '%s%s*' % (A, AN)
    DASHED_WORD     = '%s(%s|-)*' % (A, AN)
    DASHED_KEY_WORD = '\\%s' % DASHED_WORD
    ALPHAWORD       = '%s+' % A
    DIGIT           = '%s' % N
    UNSIGNED        = '%s+' % N
    E_UNSIGNED      = '\\%s+' % N
    FRACTION        = '%s+\/%s+' % (N, N)
    INT             = '-?%s' % UNSIGNED
    REAL            = '(%s\.%s*)|(-?\.%s+)' % (INT, N, N)
    KEYWORD         = '\\%s' % WORD
    WHITE           = '[ \n\t\f\r]'
    HORIZONTALWHITE = '[ \t]'
    BLACK           = '[^ \n\t\f\r]'
    RESTNAME        = '[rs]'
    NOTECOMMAND     = '\\%s+' % A
    MARKUPCOMMAND   = '\\(%s|[-_])+' % A
    LYRICS          = '(%s|%s)[^0-9 \t\n\r\f]*' % (AA, TEX)
    ESCAPED         = '''[nt\\'"]'''
    EXTENDER        = '__'
    HYPHEN          = '--'
    BOM_UTF8        = '\357\273\277'

    reserved = {
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
        '\\time': 'TIME_T',
        '\\new': 'NEWCONTEXT'
    }

    tokens = ['NOTECOMMAND'] + reserved.values( )

#%token ACCEPTS "\\accepts"
#%token ADDLYRICS "\\addlyrics"
#%token ALIAS "\\alias"
#%token ALTERNATIVE "\\alternative"
#%token BOOK "\\book"
#%token BOOKPART "\\bookpart"
#%token CHANGE "\\change"
#%token CHORDMODE "\\chordmode"
#%token CHORDS "\\chords"
#%token CONSISTS "\\consists"
#%token CONTEXT "\\context"
#%token DEFAULT "\\default"
#%token DEFAULTCHILD "\\defaultchild"
#%token DENIES "\\denies"
#%token DESCRIPTION "\\description"
#%token DRUMMODE "\\drummode"
#%token DRUMS "\\drums"
#%token FIGUREMODE "\\figuremode"
#%token FIGURES "\\figures"
#%token GROBDESCRIPTIONS "\\grobdescriptions"
#%token HEADER "\\header"
#%token INVALID "\\invalid"
#%token KEY "\\key"
#%token LAYOUT "\\layout"
#%token LYRICMODE "\\lyricmode"
#%token LYRICS "\\lyrics"
#%token LYRICSTO "\\lyricsto"
#%token MARK "\\mark"
#%token MARKUP "\\markup"
#%token MARKUPLINES "\\markuplines"
#%token MIDI "\\midi"
#%token NAME "\\name"
#%token NOTEMODE "\\notemode"
#%token OCTAVE "\\octave"
#%token ONCE "\\once"
#%token OVERRIDE "\\override"
#%token PAPER "\\paper"
#%token PARTIAL "\\partial"
#%token RELATIVE "\\relative"
#%token REMOVE "\\remove"
#%token REPEAT "\\repeat"
#%token REST "\\rest"
#%token REVERT "\\revert"
#%token SCORE "\\score"
#%token SEQUENTIAL "\\sequential"
#%token SET "\\set"
#%token SIMULTANEOUS "\\simultaneous"
#%token SKIP "\\skip"
#%token TEMPO "\\tempo"
#%token TIMES "\\times"
#%token TRANSPOSE "\\transpose"
#%token TYPE "\\type"
#%token UNSET "\\unset"
#%token WITH "\\with"

#%token TIME_T "\\time"
#%token NEWCONTEXT "\\new"

#%token CHORD_BASS "/+"
#%token CHORD_CARET "^"
#%token CHORD_COLON ":"
#%token CHORD_MINUS "-"
#%token CHORD_SLASH "/"

#%token ANGLE_OPEN "<"
#%token ANGLE_CLOSE ">"
#%token DOUBLE_ANGLE_OPEN "<<"
#%token DOUBLE_ANGLE_CLOSE ">>"
#%token E_BACKSLASH "\\"
#%token E_ANGLE_CLOSE "\\>"
#%token E_CHAR "\\C[haracter]"
#%token E_CLOSE "\\)"
#%token E_EXCLAMATION "\\!"
#%token E_BRACKET_OPEN "\\["
#%token E_OPEN "\\("
#%token E_BRACKET_CLOSE "\\]"
#%token E_ANGLE_OPEN "\\<"
#%token E_PLUS "\\+"
#%token E_TILDE "\\~"
#%token EXTENDER "__"

#%token FIGURE_CLOSE /* "\\>" */
#%token FIGURE_OPEN /* "\\<" */
#%token FIGURE_SPACE "_"
#%token HYPHEN "--"

#%token CHORDMODIFIERS
#%token LYRIC_MARKUP
#%token MULTI_MEASURE_REST

#%token <i> DIGIT
#%token <i> E_UNSIGNED
#%token <i> UNSIGNED

#/* Artificial tokens, for more generic function syntax */
#%token <i> EXPECT_MARKUP;
#%token <i> EXPECT_MUSIC;
#%token <i> EXPECT_SCM;
#%token <i> EXPECT_MARKUP_LIST
#/* After the last argument. */
#%token <i> EXPECT_NO_MORE_ARGS;

#%token <scm> BOOK_IDENTIFIER
#%token <scm> CHORDMODIFIER_PITCH
#%token <scm> CHORD_MODIFIER
#%token <scm> CHORD_REPETITION
#%token <scm> CONTEXT_DEF_IDENTIFIER
#%token <scm> CONTEXT_MOD_IDENTIFIER
#%token <scm> DRUM_PITCH
#%token <scm> DURATION_IDENTIFIER
#%token <scm> EVENT_IDENTIFIER
#%token <scm> FRACTION
#%token <scm> LYRICS_STRING
#%token <scm> LYRIC_MARKUP_IDENTIFIER
#%token <scm> MARKUP_FUNCTION
#%token <scm> MARKUP_LIST_FUNCTION
#%token <scm> MARKUP_IDENTIFIER
#%token <scm> MARKUPLINES_IDENTIFIER
#%token <scm> MUSIC_FUNCTION
#%token <scm> MUSIC_IDENTIFIER
#%token <scm> NOTENAME_PITCH
#%token <scm> NUMBER_IDENTIFIER
#%token <scm> OUTPUT_DEF_IDENTIFIER
#%token <scm> REAL
#%token <scm> RESTNAME
#%token <scm> SCM_IDENTIFIER
#%token <scm> SCM_TOKEN
#%token <scm> SCORE_IDENTIFIER
#%token <scm> STRING
#%token <scm> STRING_IDENTIFIER
#%token <scm> TONICNAME_PITCH

#    @TOKEN(NOTECOMMAND)
    def t_NOTECOMMAND(self, t):
        r'''\\[a-zA-Z\200-\377]+'''
        t.type = self.reserved.get(t.value, 'NOTECOMMAND')
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


