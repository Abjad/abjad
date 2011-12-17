import os
from ply import yacc
from abjad.tools.lilypondparsertools._LexerProxy._LexerProxy import _LexerProxy
from abjad.tools.lilypondparsertools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.lilypondparsertools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition


class LilyPondParser(object):

    def __init__(self):
        self.assignment = { }
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

    ### OVERRIDES ###

    def __call__(self, input_string):

        self.assignments = { }

        self.lexer.push_state('notes')

        concrete_syntax_tree = self.parser.parse(input_string, lexer=self.lexer)

        return concrete_syntax_tree
