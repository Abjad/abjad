from abjad.tools.rhythmtreetools._Parser import _Parser
from abjad.tools.rhythmtreetools._RTMNode import _RTMNode as Node


class _RTMParser(_Parser):

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

    start = 'nodes'

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

    def p_nodes__EMPTY(self, p):
        '''nodes : '''
        p[0] = []

    def p_nodes__nodes__node(self, p):
        '''nodes : nodes node'''
        p[0] = p[1] + [p[2]]

    def p_node__LPAREN__INTEGER__node_list_closed__RPAREN(self, p):
        '''node : LPAREN INTEGER node_list_closed RPAREN'''
        p[0] = Node(p[2], p[3])

    def p_node_list_closed__LPAREN__node_list__RPAREN(self, p):
        '''node_list_closed : LPAREN node_list RPAREN'''
        p[0] = p[2]

    def p_node_list__node_list_item(self, p):
        '''node_list : node_list_item'''
        p[0] = [p[1]]

    def p_node_list__node_list__node_list_item(self, p):
        '''node_list : node_list node_list_item'''
        p[0] = p[1] + [p[2]]

    def p_node_list_item__INTEGER(self, p):
        '''node_list_item : INTEGER'''
        p[0] = p[1]

    def p_node_list_item__node(self, p):
        '''node_list_item : node'''
        p[0] = p[1]

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
