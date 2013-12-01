# -*- encoding: utf-8 -*-
from ply import lex
from ply import yacc
from abjad.tools import abctools
from abjad.tools import schemetools


class SchemeParser(abctools.Parser):
    '''`SchemeParser` mimics how LilyPond's embedded Scheme parser behaves.

    It parses a single Scheme expression and then stops,
    by raising a `SchemeParserFinishedError`.

    The parsed expression and its exact length in characters
    are cached on the `SchemeParser` instance.

    It is intended to be used only in conjunction with `LilyPondParser`.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        r'''Lexer rules object of Scheme parser.
        '''
        return self

    @property
    def parser_rules_object(self):
        r'''Parser rules object of Scheme parser.
        '''
        return self

    ### PRIVATE METHODS ###

    def _setup(self):
        self.expression_depth = 0
        self.cursor = 0

    ### LEX SETUP ###

    A               = r'[A-Za-z]'
    N               = r'[0-9]'
    DIGIT           = r'{}'.format(N)
    UNSIGNED        = r'{}+'.format(N)
    HEX             = r'(X|x)[A-Fa-f0-9]+'
    INT             = r'(-?{})'.format(UNSIGNED)
    REAL            = r'(({}\.{}*)|(-?\.{}+))'.format(INT, N, N)
    INITIAL         = r'({}|!|\$|%|&|\*|/|<|>|\?|~|_|\^|:|=)'.format(A)
    SUBSEQUENT      = r'({}|{}|\.|\+|-)'.format(INITIAL, N)
    #IDENTIFIER      = r'({}{}*|\+|-|\.\.\.)'.format(INITIAL, SUBSEQUENT)

    # this has been rewritten to prevent Sphinx from complaining that it looks like bad ReST
    IDENTIFIER      = r'([A-Za-z!\$%&\*/<>\?~_\^:=][A-Za-z0-9!\$%&\*/<>\?~_\^:=\.\+-]*|[\+-]|\.\.\.)'

    states = (
        ('quote', 'exclusive'),
    )

    tokens = (
        'AMPERSAND',
        'ASTERISK',
        'BOOLEAN',
        'CARAT',
        'COLON',
        'DECIMAL',
        'DOLLAR',
        'EQUALS',
        'EXCLAMATION',
        'HASH',
        'HEXADECIMAL',
        'IDENTIFIER',
        'INTEGER',
        'L_CARAT',
        'L_PAREN',
        'MINUS',
        'PERCENT',
        'PERIOD',
        'PLUS',
        'QUESTION',
        'QUOTE',
        'R_CARAT',
        'R_PAREN',
        'SLASH',
        'STRING',
        'TILDE',
        'UNDERSCORE',
    )

    ### LEX METHODS ###

    t_ignore = ''

    def t_whitespace(self, t):
        r'[ \t\r]+'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        pass

    def t_BOOLEAN(self, t):
        r'\#(T|F|t|f)'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        if t.value[-1].lower() == 't':
            t.value = True
        else:
            t.value = False
        return t

    @lex.TOKEN(HEX)
    def t_HEXADECIMAL(self, t):
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        t.value = int(t.value[2:], 16)
        return t

    @lex.TOKEN(REAL)
    def t_DECIMAL(self, t):
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        t.value = float(t.value)
        return t

    def t_HASH(self, t):
        r'\#'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        return t

    @lex.TOKEN(INT)
    def t_INTEGER(self, t):
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        t.value = int(t.value)
        return t

    def t_L_PAREN(self, t):
        r'\('
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        self.expression_depth += 1
        return t

    def t_R_PAREN(self, t):
        r'\)'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        return t

    def t_quote(self, t):
        r'\"'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        t.lexer.push_state('quote')
        self.string_accumulator = ''
        pass

    def t_quote_440(self, t):
        r'''\\[nt\\'"]
        '''
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        self.string_accumulator += t.value
        pass

    def t_quote_443(self, t):
        r'[^\\""]+'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        self.string_accumulator += t.value
        pass

    def t_quote_446(self, t):
        r'\"'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        t.lexer.pop_state()
        t.type = 'STRING'
        t.value = self.string_accumulator
        self.string_accumulator = ''
        return t

    def t_quote_456(self, t):
        r'.'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        self.string_accumulator += t.value
        pass

    @lex.TOKEN(IDENTIFIER)
    def t_IDENTIFIER(self, t):
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        return t

    def t_newline(self, t):
        r'\n+'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        t.lexer.lineno += t.value.count('\n')

    def t_anything(self, t):
        r'.'
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        types = {
            '&': 'AMPERSAND',
            '*': 'ASTERISK',
            '^': 'CARAT',
            ':': 'COLON',
            '$': 'DOLLAR',
            '=': 'EQUALS',
            '!': 'EXCLAMATION',
            '<': 'L_CARAT',
            '-': 'MINUS',
            '%': 'PERCENT',
            '.': 'PERIOD',
            '+': 'PLUS',
            '?': 'QUESTION',
            "'": 'QUOTE',
            '>': 'R_CARAT',
            ')': 'R_PAREN',
            '/': 'SLASH',
            '~': 'TILDE',
            '_': 'UNDERSCORE',
        }
        if t.value in types:
            t.type = types[t.value]
            return t
        else:
            #t.lexer.skip(1)
            pass

    def t_error(self, t):
        self.cursor += len(t.value)
        t.cursor_end = self.cursor
        if self.debug:
            print("SchemeParser-{}: Illegal character {!r}".format(
                id(self), t.value[0]))
        #t.lexer.skip(1)

    t_quote_error = t_error
    t_quote_ignore = t_ignore

    ### YACC SETUP ###

    start = 'program'

    ### YACC METHODS ###

    ### program ###

    '''<program> : <form>*
    '''

    def p_program__forms(self, p):
        r'''program : forms
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_forms__EMPTY(self, p):
        r'''forms : 
        '''
        p[0] = []

    def p_forms__forms__form(self, p):
        r'''forms : forms form
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1] + [p[2]]

    ### form ###

    '''<form> : <definition> | <expression>
    '''

    def p_form__expression(self, p):
        r'''form : expression
        '''
        #print 'form : expression'
        #print p[1]
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]
        self.result = p[0]
        self.cursor_end = p.slice[0].cursor_end
        if self.debug:
            print 'PARSED {!r}'.format(self.lexer.lexdata[:self.cursor_end])
        raise SchemeParserFinishedError

    ### definition ###

    '''<definition> : <variable definition>
    |   <syntax definition>
    |   (begin <definition>*)
    |   (let-syntax (<syntax binding>*) <definition>*)
    |   (letrec-syntax (<syntax binding>*) <definition>*)
    |   <derived definition>
    '''

    ### variable definition ###

    '''<variable definition> : (define <variable> <expression>)
    |   (define (<variable> <variable>*) <body>)
    |   (define (<variable> <variable>* . <variable>) <body>)
    '''

    ### variable ###

    '''<variable> : <identifier>
    '''

    def p_variable__IDENTIFIER(self, p):
        r'''variable : IDENTIFIER
        '''
        #print 'variable : IDENTIFIER'
        #print p[1]
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = schemetools.Scheme(p[1])

    ### body ###

    '''<body> : <definition>* <expression>+
    '''

    ### syntax definition ###

    '''<syntax definition> : (define-syntax <keyword> <transformer expression>)
    '''

    ### keyword ###

    '''<keyword> : <identifier>
    '''

    ### syntax binding ###

    '''<syntax binding> : (<keyword> <transformer expression>)
    '''

    ### expression ###

    '''<expression> : <constant>
    |   <variable>
    |   (quote <datum>) | ' <datum>
    |   (lambda <formals> <body>)
    |   (if <expression> <expression> <expression>) | (if <expression> <expression>)
    |   (set! <variable> <expression>)
    |   <application>
    |   (let-syntax (<syntax binding>*) <expression>+)
    |   (letrec-syntax (<syntax binding>*) <expression>+)
    |   <derived expression>
    '''

    def p_expression__variable(self, p):
        r'''expression : variable
        '''
        #print 'expression : variable'
        #print p[1]
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_expression__QUOTE__datum(self, p):
        r'''expression : QUOTE datum
        '''
        #print 'expression : QUOTE datum'
        #print p[2]
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        datum = p[2]
        if isinstance(datum, schemetools.Scheme):
            if datum._quoting:
                datum._quoting = "'" + datum._quoting
            else:
                datum._quoting = "'"
            p[0] = datum
        else:
            p[0] = schemetools.Scheme(datum, quoting="'")

    def p_expression__constant(self, p):
        r'''expression : constant
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### constant ###

    '''<constant> : <boolean> | <number> | <character> | <string>
    '''

    def p_constant__boolean(self, p):
        r'''constant : boolean
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]
        if self.expression_depth < 1:
            #print 'constant : boolean'
            #print p[1]
            self.result = p[0]
            self.cursor_end = p.slice[0].cursor_end
            raise SchemeParserFinishedError

    def p_constant__number(self, p):
        r'''constant : number
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]
        if self.expression_depth < 1:
            #print 'constant : number'
            #print p[1]
            self.result = p[0]
            self.cursor_end = p.slice[0].cursor_end
            raise SchemeParserFinishedError

    def p_constant__string(self, p):
        r'''constant : string
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]
        if self.expression_depth < 1:
            #print 'constant : string'
            #print p[1]
            self.result = p[0]
            self.cursor_end = p.slice[0].cursor_end
            raise SchemeParserFinishedError

    ### formals ###

    '''<formals> : <variable> | (<variable>*) | (<variable>+ . <variable>)
    '''

    ### application ###

    '''<application> : (<expression> <expression>*)
    '''

    ### identifier ###

    '''<identifier> : <initial> <subsequent>* | + | - | ...
    '''

    ### initial ###

    '''<initial> : <letter> | ! | $ | % | & | * | / | : | < | = | > | ? | ~ | _ | ^
    '''

    ### subsequent ###

    '''<subsequent> : <initial> | <digit> | . | + | -
    '''

    ### letter ###

    '''<letter> : a | b | ... | z
    '''

    ### digit ###

    '''<digit> : 0 | 1 | ... | 9
    '''

    ### datum ###

    '''<datum> : <boolean> | <number> | <character> | <string> | <symbol> | <list> | <vector>
    '''

    def p_datum__constant(self, p):
        r'''datum : constant
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_datum__symbol(self, p):
        r'''datum : symbol
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    #def p_datum__boolean(self, p):
    #    r'''datum : boolean'''
    #    p[0] = p[1]

    #def p_datum__number(self, p):
    #    r'''datum : number'''
    #    p[0] = p[1]

    #def p_datum__string(self, p):
    #    r'''datum : string'''
    #    p[0] = p[1]

    def p_datum__list(self, p):
        r'''datum : list
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_datum__vector(self, p):
        r'''datum : vector
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_data__EMPTY(self, p):
        r'''data : 
        '''
        p[0] = []

    def p_data__data__datum(self, p):
        r'''data : data datum
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1] + [p[2]]

    ### boolean ###

    '''<boolean> : #t | #f
    '''

    def p_boolean__BOOLEAN(self, p):
        r'''boolean : BOOLEAN
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### number ###

    '''<number> : <num 2> | <num 8> | <num 10> | <num 16>
    '''

    def p_number__DECIMAL(self, p):
        r'''number : DECIMAL
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_number__HEXADECIMAL(self, p):
        r'''number : HEXADECIMAL
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_number__INTEGER(self, p):
        r'''number : INTEGER
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### character ###

    '''<character> : #\ <any character> | #\newline | #\space
    '''

    ### string ###

    '''<string> : " <string character>* "
    '''

    def p_string__STRING(self, p):
        r'''string : STRING
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### string character ###

    '''<string character> : \" | \\ | <any character other than " or \>
    '''

    ### symbol ###

    '''<symbol> : <identifier>
    '''

    def p_symbol__IDENTIFIER(self, p):
        r'''symbol : IDENTIFIER
        '''
        #print 'symbol : IDENTIFIER'
        #print p[1]
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### vector ###

    '''<vector> : #(<datum>*)
    '''

    def p_vector__HASH__L_PAREN__data__R_PAREN(self, p):
        r'''vector : HASH L_PAREN data R_PAREN
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[3]
        self.expression_depth -= 1

    ### list ###

    '''<list> : (<datum>*) | (<datum>+ . <datum>) | <abbreviation>
    '''

    def p_list__L_PAREN__data__R_PAREN(self, p):
        r'''list : L_PAREN data R_PAREN
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[2]
        self.expression_depth -= 1

    def p_list__L_PAREN__data__datum__PERIOD__datum__R_PAREN(self, p):
        r'''list : L_PAREN data datum PERIOD datum R_PAREN
        '''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        result = p[2] + [p[3]] + [p[5]]
        if len(result) == 2:
            p[0] = schemetools.SchemePair(*result)
        else:
            p[0] = schemetools.Scheme(*result)
        self.expression_depth -= 1

    ### abbreviation ###

    '''<abbreviation> : ' <datum> | ` <datum> | , <datum> | ,@ <datum>
    '''

    ### error ###

    def p_error(self, p):
        if p:
            if self.debug:
                print("SchemeParser-{}: Syntax error at {!r}".format(
                    id(self), p.value))
            yacc.errok()
        else:
            if self.debug:
                print("SchemeParser-{}: Syntax error at EOF".format(id(self)))
