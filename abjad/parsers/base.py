import logging
import os
import pickle
import sys
import traceback

import ply
from ply import yacc

from ..configuration import Configuration

configuration = Configuration()


class Parser:
    """
    Abstract base class for Abjad parsers.

    Rules objects for lexing and parsing must be defined by overriding the
    abstract properties ``lexer_rules_object`` and ``parser_rules_object``.

    For most parsers these properties should simply return ``self``.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_debug", "_lexer", "_logger", "_parser")

    _is_abstract = True

    ### INITIALIZER ###

    def __init__(self, debug=False):
        self._debug = bool(debug)
        self._lexer = None
        self._parser = None

        if self.debug:
            logging.basicConfig(
                level=logging.DEBUG,
                filename=self.logger_path,
                filemode="w",
                format="%(filename)10s:%(lineno)8d:%(message)s",
            )
            self._logger = logging.getLogger()
        else:
            self._logger = yacc.NullLogger()

        self._lexer = ply.lex.lex(
            debug=self.debug,
            debuglog=self.logger,
            object=self.lexer_rules_object,
        )

        if self.pickle_path and not os.path.exists(self.pickle_path):
            try:
                directory, _ = os.path.split(self.pickle_path)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                string = pickle.dumps(None)
                with open(self.pickle_path, "wb") as file_pointer:
                    file_pointer.write(string)
            except (IOError, OSError):
                traceback.print_exc()

        self._parser = ply.yacc.yacc(
            debug=self.debug,
            debuglog=self.logger,
            module=self.parser_rules_object,
            outputdir=self.output_path,
            picklefile=self.pickle_path,
        )

    ### SPECIAL METHODS ###

    def __call__(self, string):
        """
        Parses ``string`` and returns result.
        """
        if hasattr(self, "_setup"):
            self._setup()
        if self.debug:
            result = self.parser.parse_debug(
                string, lexer=self.lexer, debug=self.logger
            )
        else:
            result = self.parser.parse(string, lexer=self.lexer)
        if hasattr(self, "_cleanup"):
            result = self._cleanup(result)
        return result

    ### PUBLIC METHODS ###

    def tokenize(self, string):
        """
        Tokenizes ``string`` and print results.
        """
        self.lexer.input(string)
        for token in self.lexer:
            print(token)

    ### PUBLIC PROPERTIES ###

    @property
    def debug(self):
        """
        Is true when parser runs in debugging mode.
        """
        return self._debug

    @property
    def lexer(self):
        """
        Gets parser's PLY Lexer instance.
        """
        return self._lexer

    @property
    def logger(self):
        """
        Gets parser's logger.
        """
        return self._logger

    @property
    def logger_path(self):
        """
        Gets parser's logfile output path.
        """
        if self.output_path is None:
            return None
        string = "-".join(str(x) for x in sys.version_info)
        file_name = f"parselog_{type(self).__name__}_{string}.txt"
        return os.path.join(self.output_path, file_name)

    @property
    def output_path(self):
        """
        Gets output path for files associated with the parser.
        """
        output_path = configuration.configuration_directory / "parsers"
        if not output_path.is_dir():
            try:
                os.makedirs(output_path)
            except (IOError, OSError):
                return None
        return output_path

    @property
    def parser(self):
        """
        Gets parser's PLY LRParser instance.
        """
        return self._parser

    @property
    def pickle_path(self):
        """
        Gets output path for the parser's pickled parsing tables.
        """
        if self.output_path is None:
            return None
        string = "-".join(str(x) for x in sys.version_info)
        file_name = f"parse_tables_{type(self).__name__}_{string}.pkl"
        return os.path.join(self.output_path, file_name)
