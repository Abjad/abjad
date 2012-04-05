import logging
import os
from ply import lex
from ply import yacc
from abjad.tools import abctools
from abjad.tools.lilypondparsertools._NullHandler._NullHandler import _NullHandler
from abjad.tools.rhythmtreetools._RTMNode import _RTMNode as Node


class _RTMParser(object):

    ### LEX SETUP ###

    tokens = ('LPAREN', 'INTEGER', 'RPAREN')
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \n\t\r'

    ### YACC SETUP ###

    start = 'nodes'

    ### INITIALIZER ###

    def __init__(self, debug=False):
        self.output_path = os.path.dirname(__file__)
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
        return self.parser.parse(input_string, lexer=self.lexer)

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
