import inspect
import logging
import os
from ply import lex
from ply import yacc
from abjad.tools.abctools import AbjadObject
from abjad.tools.lilypondparsertools._NullHandler._NullHandler import _NullHandler


class _Parser(AbjadObject):

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
        parsed = self.parser.parse(input_string, lexer=self.lexer)
        if hasattr(self, 'cleanup'):
            parsed = self.cleanup(parsed)
        return parsed

    ### PUBLIC METHODS ###

    def tokenize(self, input_string):
        self.lexer.input(input_string)
        for token in self.lexer:
            print token
