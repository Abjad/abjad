from abjad.tools.abctools import Parser


class RhythmTreeParser(Parser):
    '''Parses RTM-style rhythm syntax:

    ::

        >>> parser = rhythmtreetools.RhythmTreeParser()

    ::

        >>> rtm = '(1 (1 (2 (1 -1 1)) -2))'
        >>> result = parser(rtm)[0]
        >>> result
        RhythmTreeContainer(
            children=(
                RhythmTreeLeaf(
                    duration=1,
                    is_pitched=True,
                    ),
                RhythmTreeContainer(
                    children=(
                        RhythmTreeLeaf(
                            duration=1,
                            is_pitched=True,
                            ),
                        RhythmTreeLeaf(
                            duration=1,
                            is_pitched=False,
                            ),
                        RhythmTreeLeaf(
                            duration=1,
                            is_pitched=True,
                            ),
                    ),
                    duration=2
                    ),
                RhythmTreeLeaf(
                    duration=2,
                    is_pitched=False,
                    ),
            ),
            duration=1
            )

    ::

        >>> result.rtm_format
        '(1 (1 (2 (1 -1 1)) -2))'

    Returns `RhythmTreeParser` instance.
    '''

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### LEX SETUP ###

    tokens = (
        'LPAREN',
        'INTEGER',
        'RPAREN'
    )

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \n\t\r'

    ### YACC SETUP ###

    start = 'toplevel'

    ### LEX METHODS ###

    def t_INTEGER(self, t):
        r'(-?[1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ### YACC METHODS ###

    def p_container__LPAREN__INTEGER__node_list_closed__RPAREN(self, p):
        '''container : LPAREN INTEGER node_list_closed RPAREN'''
        from abjad.tools import rhythmtreetools
        p[0] = rhythmtreetools.RhythmTreeContainer(p[2], p[3])

    def p_leaf__INTEGER(self, p):
        '''leaf : INTEGER'''
        from abjad.tools import rhythmtreetools
        p[0] = rhythmtreetools.RhythmTreeLeaf(abs(p[1]), 0 < p[1])

    def p_node__container(self, p):
        '''node : container'''
        p[0] = p[1]

    def p_node__leaf(self, p):
        '''node : leaf'''
        p[0] = p[1]

    def p_node_list_closed__LPAREN__node_list__RPAREN(self, p):
        '''node_list_closed : LPAREN node_list RPAREN'''
        p[0] = p[2]

    def p_node_list__node_list_item(self, p):
        '''node_list : node_list_item'''
        p[0] = [p[1]]

    def p_node_list__node_list__node_list_item(self, p):
        '''node_list : node_list node_list_item'''
        p[0] = p[1] + [p[2]]

    def p_node_list_item__node(self, p):
        '''node_list_item : node'''
        p[0] = p[1]

    def p_toplevel__EMPTY(self, p):
        '''toplevel : '''
        p[0] = []

    def p_toplevel__toplevel__container(self, p):
        '''toplevel : toplevel container'''
        p[0] = p[1] + [p[2]]

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
