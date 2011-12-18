import os
from ply import yacc
from abjad.tools.durationtools import Duration

from abjad.ly.py.current_module import current_module
from abjad.ly.py.language_pitch_names import language_pitch_names
from abjad.ly.py.markup_functions import markup_functions
from abjad.ly.py.markup_functions import markup_list_functions

from abjad.tools.lilypondparsertools._LexerProxy._LexerProxy import _LexerProxy
from abjad.tools.lilypondparsertools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition


class LilyPondParser(object):

    def __init__(self):
        self.lexdef = _LilyPondLexicalDefinition(self)
        self.syndef = _LilyPondSyntacticalDefinition(self)
        self.output_path = os.path.dirname(__file__)
        self.pickle_path = os.path.join(self.output_path, '_parsetab.pkl')

        self.lexer = _LexerProxy(object=self.lexdef)
        self.parser = yacc.yacc(
            debug=0,
            module=self.syndef,
            outputdir=self.output_path,
            picklefile=self.pickle_path)

        self.current_module = current_module
        self.language_pitch_names = language_pitch_names
        self.markup_functions = markup_functions
        self.markup_list_functions = markup_list_functions

        self.assignments = { }
        self.parser_variables = {
            'default_duration': Duration(1, 4),
            'language': 'english',
        }

    ### OVERRIDES ###

    def __call__(self, input_string):
        self._reset( )
        concrete_syntax_tree = self.parser.parse(input_string, lexer=self.lexer)
        return concrete_syntax_tree

    ### PRIVATE METHODS ###

    def _reset(self):
        try:
            self.parser.restart( )
        except:
            pass

        self.assignments = { }
        self.lexer.push_state('notes')
        self.parser_variables = {
            'default_duration': Duration(1, 4),
            'language': 'english',
        }
