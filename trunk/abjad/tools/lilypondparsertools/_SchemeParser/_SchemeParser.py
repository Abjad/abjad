import inspect
import logging
import os

from ply import lex
from ply import yacc

from abjad.tools.abctools import AbjadObject
from abjad.tools.lilypondparsertools._NullHandler._NullHandler import _NullHandler


class _SchemeParser(AbjadObject):

    def __init__(self, debug=False):
        class_path = inspect.getfile(self.__class__)
        self.output_path = class_path.rpartition(os.path.sep)[0]
        self.pickle_path = os.path.join(self.output_path, '_parsetab.pkl')
        self.logger_path = os.path.join(self.output_path, 'parselog.txt')

        self.debug = bool(debug)

        # setup a logging
        if self.debug:
            logging.basicConfig(
                level = logging.DEBUG,
                filename = self.logger_path,
                filemode = 'w',
                format = '%(filename)10s:%(lineno)8d:%(message)s'
            )
            self.logger = logging.getLogger()
        else:
            self.logger = logging.getLogger()
            self.logger.addHandler(_NullHandler()) # use custom NullHandler for 2.6 compatibility

        # setup PLY objects
        self.lexer = lex.lex(
            debug=True,
            debuglog=self.logger,
            object=self,
        )
        self.parser = yacc.yacc(
            debug=True,
            debuglog=self.logger,
            module=self,
            outputdir=self.output_path,
            picklefile=self.pickle_path,
        )

    ### SPECIAL METHODS ###

    def __call__(self, input_string):
        #self.lexer.input(input_string)
        #for token in self.lexer:
        #    print token
        self.expression_depth = 0
        parsed = self.parser.parse(input_string, lexer=self.lexer)
        if hasattr(self, 'cleanup'):
            parsed = self.cleanup(parsed)
        return parsed

    ### PUBLIC METHODS ###

    def tokenize(self, input_string):
        self.lexer.input(input_string)
        for token in self.lexer:
            print token

    ### LEX SETUP ###

    N               = r'[0-9]'
    DIGIT           = r'%s' % N
    UNSIGNED        = r'%s+' % N
    INT             = r'(-?%s)' % UNSIGNED
    REAL            = r'((%s\.%s*)|(-?\.%s+))' % (INT, N, N)

    states = (
        ('quote', 'exclusive'),
    )

    tokens = (
        'BOOLEAN',
        'DECIMAL',
        'ELLIPSIS',
        'INTEGER',
        'STRING',
    )

    literals = (
        '&', # AMPERSAND
        '*', # ASTERISK
        '^', # CARAT
        ':', # COLON
        '$', # DOLLAR
        '=', # EQUALS
        '!', # EXCLAMATION
        '<', # L_CARAT
        '(', # L_PAREN
        '-', # MINUS
        '%', # PERCENT
        '+', # PLUS
        '?', # QUESTION
        '>', # R_CARAT
        ')', # R_PAREN
        '/', # SLASH
        '~', # TILDE
        '_', # UNDERSCORE
    )

    t_ELLIPSIS = '\.\.\.'

    t_ignore = ' \t\r'

    ### YACC SETUP ###

    start = 'start'

    ### LEX METHODS ###

    def t_BOOLEAN(self, t):
        r'\#[tf]'
        if t.value == '\#t':
            t.value = True
        else:
            t.value = False
        return t

    @lex.TOKEN(REAL)
    def t_DECIMAL(self, t):
        t.value = float(t.value)
        return t

    @lex.TOKEN(INT)
    def t_INTEGER(self, t):
        t.value = int(t.value)
        return t

    def t_L_PAREN(self, t):
        r'\('
        self.depth += 1
        return t

    def t_R_PAREN(self, t):
        r'\)'
        self.depth -= 1
        return t

    def t_quote(self, t):
        r'\"'
        t.lexer.push_state('quote')
        self.string_accumulator = ''
        pass

    def t_quote_440(self, t):
        r'''\\[nt\\'"]'''
        self.string_accumulator += t.value
        pass

    def t_quote_443(self, t):
        r'[^\\""]+'
        self.string_accumulator += t.value
        pass

    def t_quote_446(self, t):
        r'\"'
        t.lexer.pop_state( )
        t.type = 'STRING'
        t.value = self.string_accumulator
        self.string_accumulator = ''
        return t

    def t_quote_456(self, t):
        r'.'
        self.string_accumulator += t.value
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_quote_error = t_error
    t_quote_ignore = t_ignore

    ### YACC METHODS ###

    def p_start__ELLIPSIS(self, p):
        'start : ELLIPSIS'
        p[0] = 'DONE!'

    ### program ###

    '''<program> : <form>*'''

    ### form ###

    '''<form> : <definition> | <expression>'''

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

    '''<variable> : <identifier>'''

    ### body ###

    '''<body> : <definition>* <expression>+'''

    ### syntax definition ###

    '''<syntax definition> : (define-syntax <keyword> <transformer expression>)'''

    ### keyword ###

    '''<keyword> : <identifier>'''

    ### syntax binding ###

    '''<syntax binding> : (<keyword> <transformer expression>)'''

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

    ### constant ###

    '''<constant> : <boolean> | <number> | <character> | <string>'''

    ### formals ###

    '''<formals> : <variable> | (<variable>*) | (<variable>+ . <variable>)'''

    ### application ###

    '''<application> : (<expression> <expression>*)'''

    ### identifier ###

    '''<identifier> : <initial> <subsequent>* | + | - | ...'''

    ### initial ###

    '''<initial> : <letter> | ! | $ | % | & | * | / | : | < | = | > | ? | ~ | _ | ^'''

    ### subsequent ###

    '''<subsequent> : <initial> | <digit> | . | + | -'''

    ### letter ###

    '''<letter> : a | b | ... | z'''

    ### digit ###

    '''<digit> : 0 | 1 | ... | 9'''

    ### datum ###

    '''<datum> : <boolean> | <number> | <character> | <string> | <symbol> | <list> | <vector>'''

    ### boolean ###

    '''<boolean> : #t | #f'''

    ### number ###
    
    '''<number> : <num 2> | <num 8> | <num 10> | <num 16>'''

    ### character ###

    '''<character> : #\ <any character> | #\newline | #\space'''

    ### string ###

    '''<string> : " <string character>* "'''

    ### string character ###

    '''<string character> : \" | \\ | <any character other than " or \>'''

    ### symbol ###

    '''<symbol> : <identifier>'''

    ### list ###

    '''<list> : (<datum>*) | (<datum>+ . <datum>) | <abbreviation>'''

    ### abbreviation ###

    '''<abbreviation> : ' <datum> | ` <datum> | , <datum> | ,@ <datum>'''

    ### vector

    '''<vector> : #(<datum>*)'''

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
