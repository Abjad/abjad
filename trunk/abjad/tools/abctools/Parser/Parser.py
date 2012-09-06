import abc
import inspect
import logging
import os
from ply import lex
from ply import yacc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Parser(AbjadObject):
    '''Abstract base class for Abjad parsers.

    Rules objects for lexing and parsing must be defined by overriding the
    abstract properties `lexer_rules_object` and `parser_rules_object`.

    For most parsers these properties should simply return `self`.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_debug', '_lexer', '_logger', '_parser')

    ### INITIALIZER ###

    def __init__(self, debug=False):

        self._debug = bool(debug)
        self._lexer = None
        self._parser = None

        if self.debug:
            logging.basicConfig(
                level = logging.DEBUG,
                filename = self.logger_path,
                filemode = 'w',
                format = '%(filename)10s:%(lineno)8d:%(message)s'
                )
            self._logger = logging.getLogger()
        else:
            self._logger = logging.getLogger()
            self._logger.addHandler(logging.NullHandler())

        self._lexer = lex.lex(
            debug=self.debug,
            debuglog=self.logger,
            object=self.lexer_rules_object
            )

        self._parser = yacc.yacc(
            debug=self.debug,
            debuglog=self.logger,
            module=self.parser_rules_object,
            outputdir=self.output_path,
            picklefile=self.pickle_path,
            )

    ### SPECIAL METHODS ###

    def __call__(self, input_string):
        '''Parse `input_string` and return result.'''

        if hasattr(self, '_setup'):
            self._setup()

        if self.debug:
            result = self.parser.parse_debug(
                input_string,
                lexer=self.lexer,
                debug=self.logger)
        else:
            result = self.parser.parse(
                input_string,
                lexer=self.lexer)

        if hasattr(self, '_cleanup'):
            result = self._cleanup(result)

        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def debug(self):
        '''True if the parser runs in debugging mode.'''
        return self._debug

    @property
    def lexer(self):
        '''The parser's PLY Lexer instance.'''
        return self._lexer

    @abc.abstractproperty
    def lexer_rules_object(self):
        '''The object containing the parser's lexical rule definitions.'''
        raise NotImplemented

    @property
    def logger(self):
        '''The parser's Logger instance.'''
        return self._logger

    @property
    def logger_path(self):
        '''The output path for the parser's logfile.'''
        return os.path.join(self.output_path, 'parselog.txt')

    @property
    def output_path(self):
        '''The output path for files associated with the parser.'''
        klass_path = inspect.getfile(self.__class__)
        return klass_path.rpartition(os.path.sep)[0]

    @property
    def parser(self):
        '''The parser's PLY LRParser instance.'''
        return self._parser

    @abc.abstractproperty
    def parser_rules_object(self):
        '''The object containing the parser's syntactical rule definitions.'''
        raise NotImplemented

    @property
    def pickle_path(self):
        '''The output path for the parser's pickled parsing tables.'''
        return os.path.join(self.output_path, '_parsetab.pkl')

    ### PUBLIC METHODS ###

    def tokenize(self, input_string):
        '''Tokenize `input string` and print results.'''
        self.lexer.input(input_string)
        for token in self.lexer:
            print token
