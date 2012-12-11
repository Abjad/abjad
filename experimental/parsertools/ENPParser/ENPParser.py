from abjad.tools.abctools import Parser


class ENPParser(Parser):
    '''Parses a subset of PWGL's ENP syntax:

    ::

        ((:instrument "alto saxophone"
          :staff :treble-staff
          (((2
             ((1 :notes (52) :expressions ((:slur/1 :slope -6.0) :pp/1))))
            (1
             ((1.0
               :notes (52) :expressions (:slur/1))
              (1 :notes ((58 :enharmonic 1)) :expressions (:slur/1))
              (1 :notes (59) :expressions (:slur/1))
              (1 :notes (62) :expressions (:slur/1))))
            (1
             ((1 :notes ((63 :enharmonic 1)) :expressions  (:slur/1 :crescendo/1))
              (1 :notes (65)  :expressions  (:crescendo/1))
              (1 :notes ((66 :enharmonic 1)) :expressions  (:crescendo/1))
              (1  :notes ((68 :enharmonic 1))  :expressions  (:crescendo/1))
              (1   :notes (69) :expressions  (:crescendo/1))))
            (1
             ((1  :notes (72)  :expressions  (:slur/1 :f/1))
              (1 :x-offset 1.0  :notes  ((73 :enharmonic 1)) :expressions (:slur/1 :f/1))
              (6  :x-offset 2.0 :notes (79) :expressions (:f/1))))))))

    Return `ENPParser` instance.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### PRIVATE METHODS ###

    def _setup(self):
        self._lexer.push_state('INITIAL')

    ### LEX SETUP ###

    states = (
        ('quote', 'exclusive'),
        )

    tokens = (
        'FLOAT',
        'INTEGER',
        'KEYWORD',
        'PAREN_L',
        'PAREN_R',
        'STRING',
        )

    t_PAREN_L = r'\('
    t_PAREN_R = r'\)'
    t_ignore = ' \n\t\r'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    t_quote_ignore = t_ignore
    t_quote_error = t_error

    ### LEX METHODS ###

    def t_INITIAL_FLOAT(self, t):
        r'(-?\d*\.\d*)'
        t.value = float(t.value)
        return t

    def t_INITIAL_INTEGER(self, t):
        r'(-?\d+)'
        t.value = int(t.value)
        return t

    def t_INITIAL_KEYWORD(self, t):
        r':[A-Za-z0-9-/]+'
        class Keyword(object):
            def __init__(self, string):
                self.value = string[1:]
        t.value = Keyword(t.value)
        return t

    def t_INITIAL_start_quote(self, t):
        r'\"'
        t.lexer.push_state('quote')
        self.string_accumulator = ''
        pass

    def t_quote_440(self, t):
        r'\[nt\'"]'
        self.string_accumulator += t.value
        pass

    def t_quote_XXX(self, t):
        r'\\"'
        self.string_accumulator += t.value
        pass

    def t_quote_443(self, t):
        r'[^\\""]+'
        self.string_accumulator += t.value
        pass

    def t_quote_446(self, t):
        r'\"'
        t.lexer.pop_state()
        t.type = 'STRING'
        t.value = self.string_accumulator
        return t

    ### YACC SETUP ###

    start = 'toplevel'

    ### YACC METHODS ###

    def p_list__PAREN_L__list_body__PAREN_R(self, p):
        '''list : PAREN_L list_body PAREN_R'''
        p[0] = p[2]

    def p_list_body__list_body_element(self, p):
        '''list_body : list_body_element'''
        p[0] = [p[1]]

    def p_list_body__list_body__list_body_element(self, p):
        '''list_body : list_body list_body_element'''
        p[0] = p[1] + [p[2]]

    def p_list_body_element__FLOAT(self, p):
        '''list_body_element : FLOAT'''
        p[0] = p[1]

    def p_list_body_element__INTEGER(self, p):
        '''list_body_element : INTEGER'''
        p[0] = p[1]

    def p_list_body_element__KEYWORD(self, p):
        '''list_body_element : KEYWORD'''
        p[0] = p[1]

    def p_list_body_element__STRING(self, p):
        '''list_body_element : STRING'''
        p[0] = p[1]

    def p_list_body_element__list(self, p):
        '''list_body_element : list'''
        p[0] = p[1]

    def p_toplevel__EMPTY(self, p):
        '''toplevel : '''
        p[0] = []

    def p_toplevel__list(self, p):
        '''toplevel : toplevel list'''
        p[0] = p[1] + [p[2]]

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")

