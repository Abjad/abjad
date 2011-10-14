import os
from ply import lex
from ply import yacc
from abjad.tools.iotools._LilyPondLexicalDefinition._LilyPondLexicalDefinition \
    import _LilyPondLexicalDefinition
from abjad.tools.iotools._LilyPondSyntacticalDefinition._LilyPondSyntacticalDefinition \
    import _LilyPondSyntacticalDefinition


class _LilyPondParser(object):

    def __init__(self):
        self.assignment = { }
        self.lexdef = _LilyPondLexicalDefinition(self)
        self.syndef = _LilyPondSyntacticalDefinition(self)
        self.output_path = os.path.dirname(__file__)
        self.pickle_path = os.path.join(self.output_path, '_parsetab.pkl')

    ### OVERRIDES ###

    def __call__(self, input_string):

        self.assignments = { }

        lexer = lex.lex(
            object=self.lexdef)

        parser = yacc.yacc(
            debug=0,
            module=self.syndef,
            outputdir=self.output_path,
            picklefile=self.pickle_path)

        lexer.push_state('notes')

        concrete_syntax_tree = parser.parse(input_string, lexer=lexer)

        return concrete_syntax_tree
