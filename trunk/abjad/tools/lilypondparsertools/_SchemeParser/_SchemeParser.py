import inspect
import logging
import os

from ply import lex
from ply import yacc

from abjad.tools import schemetools
from abjad.tools.lilypondparsertools._NullHandler._NullHandler import _NullHandler
from abjad.tools.lilypondparsertools._SchemeParserFinishedException import _SchemeParserFinishedException


class _SchemeParser(object):

    ### INITIALIZER ###

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
        self.cursor = 0

        #if os.path.exists(self.logger_path):
        #    os.remove(self.logger_path)

        if self.debug:
            result = self.parser.parsedebug(
                input_string,
                lexer=self.lexer,
                debug=self.logger,
                tracking=True,
                )
        else:
            result = self.parser.parse(
                input_string,
                lexer=self.lexer,
                tracking=True,
                )

        if hasattr(self, 'cleanup'):
            result = self.cleanup(result)
        return result

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
        r'''\\[nt\\'"]'''
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
        t.lexer.pop_state( )
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
            t.lexer.skip(1)
            pass

    def t_error(self, t):
        if self.debug:
            print("_SchemeParser-{}: Illegal character {!r}".format(id(self), t.value[0]))
        t.lexer.skip(1)

    t_quote_error = t_error
    t_quote_ignore = t_ignore

    ### YACC SETUP ###

    start = 'program'

    ### YACC METHODS ###

    ### program ###

    '''<program> : <form>*'''

    def p_program__forms(self, p):
        '''program : forms'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_forms__EMPTY(self, p):
        '''forms : '''
        p[0] = []

    def p_forms__forms__form(self, p):
        '''forms : forms form'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1] + [p[2]]

    ### form ###

    '''<form> : <definition> | <expression>'''

    def p_form__expression(self, p):
        '''form : expression'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]
        self.result = p[0]
        self.cursor_end = p.slice[0].cursor_end
        raise _SchemeParserFinishedException

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

    def p_expression__QUOTE__datum(self, p):
        '''expression : QUOTE datum'''
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
        '''expression : constant'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### constant ###

    '''<constant> : <boolean> | <number> | <character> | <string>'''

    def p_constant__boolean(self, p):
        '''constant : boolean'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]
        if self.expression_depth < 1:
            self.result = p[0]
            self.cursor_end = p.slice[0].cursor_end
            raise _SchemeParserFinishedException

    def p_constant__number(self, p):
        '''constant : number'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1] 
        if self.expression_depth < 1:
            self.result = p[0]
            self.cursor_end = p.slice[0].cursor_end
            raise _SchemeParserFinishedException

    def p_constant__string(self, p):
        '''constant : string'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1] 
        if self.expression_depth < 1:
            self.result = p[0]
            self.cursor_end = p.slice[0].cursor_end
            raise _SchemeParserFinishedException

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

    def p_datum__constant(self, p):
        '''datum : constant'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    #def p_datum__boolean(self, p):
    #    '''datum : boolean'''
    #    p[0] = p[1]

    #def p_datum__number(self, p):
    #    '''datum : number'''
    #    p[0] = p[1]

    #def p_datum__string(self, p):
    #    '''datum : string'''
    #    p[0] = p[1]

    def p_datum__list(self, p):
        '''datum : list'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_datum__vector(self, p):
        '''datum : vector'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_data__EMPTY(self, p):
        '''data : '''
        p[0] = []

    def p_data__data__datum(self, p):
        '''data : data datum'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1] + [p[2]]

    ### boolean ###

    '''<boolean> : #t | #f'''

    def p_boolean__BOOLEAN(self, p):
        '''boolean : BOOLEAN'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### number ###
    
    '''<number> : <num 2> | <num 8> | <num 10> | <num 16>'''

    def p_number__DECIMAL(self, p):
        '''number : DECIMAL'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    def p_number__INTEGER(self, p):
        '''number : INTEGER'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### character ###

    '''<character> : #\ <any character> | #\newline | #\space'''

    ### string ###

    '''<string> : " <string character>* "'''

    def p_string__STRING(self, p):
        '''string : STRING'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[1]

    ### string character ###

    '''<string character> : \" | \\ | <any character other than " or \>'''

    ### symbol ###

    '''<symbol> : <identifier>'''

    ### vector ###

    '''<vector> : #(<datum>*)'''

    def p_vector__HASH__L_PAREN__data__R_PAREN(self, p):
        '''vector : HASH L_PAREN data R_PAREN'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[3]
        self.expression_depth -= 1

    ### list ###

    '''<list> : (<datum>*) | (<datum>+ . <datum>) | <abbreviation>'''

    def p_list__L_PAREN__data__R_PAREN(self, p):
        '''list : L_PAREN data R_PAREN'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        p[0] = p[2]
        self.expression_depth -= 1

    def p_list__L_PAREN__data__datum__PERIOD__datum__R_PAREN(self, p):
        '''list : L_PAREN data datum PERIOD datum R_PAREN'''
        p.slice[0].cursor_end = p.slice[-1].cursor_end
        result = p[2] + [p[3]] + [p[5]]
        if len(result) == 2:
            p[0] = schemetools.SchemePair(*result)
        else:
            p[0] = schemetools.Scheme(*result)
        self.expression_depth -= 1

    ### abbreviation ###

    '''<abbreviation> : ' <datum> | ` <datum> | , <datum> | ,@ <datum>'''

    ### error ###

    def p_error(self, p):
        if p:
            if self.debug:
                print("_SchemeParser-{}: Syntax error at {!r}".format(id(self), p.value))
            yacc.errok()
        else:
            if self.debug:
                print("_SchemeParser-{}: Syntax error at EOF".format(id(self)))
